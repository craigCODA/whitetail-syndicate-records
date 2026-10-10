#!/usr/bin/env python3
"""Maintain an evidence-backed time/payment ledger and regenerate its reports."""
import argparse
import copy
from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER = 'records/billing/ledger.json'
SUMMARY_JSON = 'records/billing/summary.json'
SUMMARY_MD = 'records/billing/summary.md'


def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{label} must be an integer >= {minimum}')
    return value


def iso_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('date must be YYYY-MM-DD')
    date.fromisoformat(value)
    return value


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} is required')
    return value


def evidence(paths, root):
    if not isinstance(paths, list) or not paths:
        raise ValueError('at least one evidence path is required')
    for name in paths:
        text(name, 'evidence path')
        path = Path(name)
        target = (root / path).resolve()
        if path.is_absolute() or '..' in path.parts or not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f'missing or unsafe evidence path: {name}')


def money_to_cents(value):
    value = str(value).strip()
    if not re.fullmatch(r'\d+(?:\.\d{1,2})?', value):
        raise ValueError('money must be a nonnegative decimal with at most two decimal places')
    return int(Decimal(value) * 100)


def entry_value(entry):
    return int((Decimal(entry['minutes']) * entry['rate_cents'] / 60).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def reconciliation_details(ledger):
    r = ledger.get('reconciliation')
    if not r:
        return None
    times = {t['id']: t for t in ledger['time_entries']}
    payments = {p['id']: p for p in ledger['payments']}
    payment = payments.get(r.get('payment_id'))
    if payment is None:
        raise ValueError('bill references a missing payment record')
    if payment['status'] != 'confirmed' or payment['scope'] != 'current_work':
        raise ValueError('paid bill requires a confirmed current-work payment')
    as_of = iso_date(r['as_of'])
    invoice_date = iso_date(r['paid_bill_invoice_date'])
    accrual_start = iso_date(r['current_accrual_start_date'])
    if invoice_date > payment['date']:
        raise ValueError('paid bill invoice date must be on or before its payment date')
    if payment['date'] > as_of:
        raise ValueError('bill period must cover its payment date')
    if accrual_start > as_of:
        raise ValueError('current accrual period must begin on or before its end date')
    totals = {}
    linked_ids = set()
    for name in ['paid_work_items', 'current_work_items']:
        items = r.get(name)
        if not isinstance(items, list) or not items:
            raise ValueError('bill requires nonempty itemized work')
        descriptions = set()
        for item in items:
            description = text(item['description'], 'bill item description').strip().casefold()
            integer(item['minutes'], 'bill item minutes', 1)
            integer(item.get('rate_cents', ledger['default_rate_cents']), 'bill item rate', 1)
            if description in descriptions:
                raise ValueError('bill work items must be distinct')
            descriptions.add(description)
            ident = item.get('time_entry_id')
            if ident is not None:
                if ident in linked_ids:
                    raise ValueError('linked time must be distinct across bill items')
                linked_ids.add(ident)
                entry = times.get(ident)
                if entry is None or entry['status'] != 'confirmed' or entry['basis'] != 'logged':
                    raise ValueError('bill item requires confirmed logged time')
                if item['minutes'] != entry['minutes'] or item.get('rate_cents', ledger['default_rate_cents']) != entry['rate_cents']:
                    raise ValueError('bill item must match its linked time')
                if name == 'current_work_items' and not accrual_start <= entry['date'] <= as_of:
                    raise ValueError('current accrual period must cover its linked time')
                if name == 'paid_work_items' and entry['date'] > invoice_date:
                    raise ValueError('invoice date must cover its linked time')
        totals[name] = (sum(item['minutes'] for item in items),
                       sum(entry_value(dict(item, rate_cents=item.get('rate_cents', ledger['default_rate_cents']))) for item in items))
    paid_minutes, paid_value = totals['paid_work_items']
    current_minutes, current_value = totals['current_work_items']
    if paid_value != payment['amount_cents']:
        raise ValueError('itemized paid work must match the confirmed payment')
    opening = ledger['opening_balance']
    if opening['as_of'] != as_of or opening['amount_cents'] != current_value:
        raise ValueError('itemized current work must match the confirmed opening balance')
    return dict(r, paid_work_minutes=paid_minutes, paid_work_cents=paid_value,
                current_accrued_cents=current_value, current_accrued_minutes=current_minutes,
                total_reconciled_minutes=paid_minutes + current_minutes)


def validate_ledger(ledger, root):
    if ledger.get('schema_version') != 1 or ledger.get('currency') != 'USD' or ledger.get('timezone') != 'America/Chicago':
        raise ValueError('ledger requires schema 1, USD and America/Chicago')
    integer(ledger['default_rate_cents'], 'default rate', 1)
    integer(ledger['billing_increment_cents'], 'billing increment', 1)
    text(ledger['coverage_note'], 'coverage note')
    opening = ledger['opening_balance']
    if opening.get('amount_cents') is None:
        if opening.get('as_of') is not None or opening.get('confirmed_by') is not None:
            raise ValueError('unconfirmed opening balance must have no date or confirmer')
    else:
        integer(opening['amount_cents'], 'opening balance')
        iso_date(opening['as_of'])
        text(opening.get('confirmed_by'), 'opening confirmed_by')
        evidence(opening['evidence_paths'], root)
    ids = set()
    fingerprints = {'time_entries': set(), 'payments': set()}
    for group in ['time_entries', 'payments', 'invoices', 'historical_references']:
        if not isinstance(ledger[group], list):
            raise ValueError(f'{group} must be a list')
        for entry in ledger[group]:
            ident = text(entry.get('id'), 'entry id')
            if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,100}', ident):
                raise ValueError('invalid entry id')
            if ident in ids:
                raise ValueError(f'duplicate id: {ident}')
            ids.add(ident)
            evidence(entry['evidence_paths'], root)
            if group == 'historical_references':
                if entry['kind'] not in ['invoice_stated', 'accrual_stated', 'retrospective_estimate']:
                    raise ValueError('unknown historical reference kind')
                text(entry['description'], 'historical description')
                integer(entry['minutes'], 'historical minutes')
                if entry.get('amount_cents') is not None:
                    integer(entry['amount_cents'], 'historical amount')
                continue
            allowed = ['draft', 'issued', 'void'] if group == 'invoices' else ['pending', 'confirmed', 'void']
            if entry['status'] not in allowed:
                raise ValueError('unknown status')
            if entry['status'] in ['confirmed', 'issued']:
                text(entry.get('confirmed_by'), 'confirmed_by')
            if entry['status'] == 'void':
                text(entry.get('void_reason'), 'void reason')
                text(entry.get('voided_by'), 'voided_by')
            if group == 'payments' and entry.get('date') is None and entry['scope'] == 'initial_paid_artwork':
                pass  # Original artwork payment date was not supplied.
            else:
                iso_date(entry['date'])
            if group == 'time_entries':
                text(entry['description'], 'time description')
                text(entry['area'], 'time area')
                integer(entry['minutes'], 'minutes', 1)
                integer(entry['rate_cents'], 'rate', 1)
                if entry['basis'] not in ['logged', 'estimated']:
                    raise ValueError('time basis must be logged or estimated')
                fingerprint = (entry['date'], entry['area'], entry['description'].strip().casefold(), entry['minutes'], tuple(sorted(entry['evidence_paths'])))
            elif group == 'payments':
                text(entry['description'], 'payment description')
                integer(entry['amount_cents'], 'payment amount', 1)
                if entry['scope'] not in ['current_work', 'initial_paid_artwork']:
                    raise ValueError('unknown payment scope')
                fingerprint = (entry['date'], entry['amount_cents'], entry['scope'], tuple(sorted(entry['evidence_paths'])))
            else:
                integer(entry['amount_cents'], 'invoice amount', 1)
                continue
            if entry['status'] != 'void':
                if fingerprint in fingerprints[group]:
                    raise ValueError('repeated time' if group == 'time_entries' else 'repeated payment')
                fingerprints[group].add(fingerprint)
    times = {t['id']: t for t in ledger['time_entries']}
    invoices = {i['id']: i for i in ledger['invoices']}
    reserved = set()
    for inv in ledger['invoices']:
        if inv['status'] == 'void':
            continue
        entries = inv['time_entry_ids']
        if not entries or len(entries) != len(set(entries)):
            raise ValueError('invoice needs distinct time entry IDs')
        for ident in entries:
            t = times.get(ident)
            if t is None or t['basis'] != 'logged' or t['status'] != 'confirmed':
                raise ValueError('invoice requires confirmed logged time')
            if opening['as_of'] is not None and t['date'] <= opening['as_of']:
                raise ValueError('invoice time is already covered by opening balance')
            if t['date'] > inv['date']:
                raise ValueError('invoice date precedes its work')
            if ident in reserved:
                raise ValueError('time already reserved in another invoice')
            reserved.add(ident)
        if sum(entry_value(times[ident]) for ident in entries) != inv['amount_cents']:
            raise ValueError('invoice amount does not match its time entries')
    allocations = {}
    for p in ledger['payments']:
        ident = p.get('invoice_id')
        if p['status'] == 'void' or ident is None:
            continue
        inv = invoices.get(ident)
        if p['scope'] != 'current_work' or inv is None or inv['status'] != 'issued':
            raise ValueError('payment allocation requires an issued current-work invoice')
        if p['status'] == 'confirmed':
            allocations[ident] = allocations.get(ident, 0) + p['amount_cents']
            if allocations[ident] > inv['amount_cents']:
                raise ValueError('payment allocation exceeds invoice')
    references = {h['id']: h for h in ledger['historical_references']}
    historical_paid = {}
    historical_minutes = {}
    for payment in ledger['payments']:
        if payment['status'] == 'void':
            continue
        pieces = payment.get('allocations', [])
        if not pieces:
            continue
        if payment['scope'] != 'current_work' or payment.get('invoice_id') is not None:
            raise ValueError('historical allocations must be separate from an invoice allocation')
        seen = set()
        for piece in pieces:
            ident = piece['reference_id']
            ref = references.get(ident)
            if ident in seen or ref is None or ref['kind'] == 'retrospective_estimate':
                raise ValueError('historical allocations require distinct billed/accrued references')
            seen.add(ident)
            integer(piece['amount_cents'], 'allocated amount', 1)
            integer(piece['minutes'], 'allocated minutes', 1)
            value = entry_value({'minutes': piece['minutes'], 'rate_cents': ledger['default_rate_cents']})
            if value != piece['amount_cents']:
                raise ValueError('allocated minutes do not match the allocated amount')
            if payment['status'] == 'confirmed':
                historical_paid[ident] = historical_paid.get(ident, 0) + piece['amount_cents']
                historical_minutes[ident] = historical_minutes.get(ident, 0) + piece['minutes']
                if historical_paid[ident] > ref['amount_cents'] or historical_minutes[ident] > ref['minutes']:
                    raise ValueError('payment exceeds historical work reference')
        if sum(piece['amount_cents'] for piece in pieces) != payment['amount_cents']:
            raise ValueError('payment allocations must total the single receipt amount')
    if ledger.get('reconciliation'):
        text(ledger['reconciliation'].get('confirmed_by'), 'reconciliation confirmed_by')
        evidence(ledger['reconciliation']['evidence_paths'], root)
        reconciliation_details(ledger)


def summarize(ledger, root):
    validate_ledger(ledger, root)
    opening = ledger['opening_balance']
    def in_period(entry):
        return opening['as_of'] is None or (entry['date'] is not None and entry['date'] > opening['as_of'])
    active = [t for t in ledger['time_entries'] if t['status'] != 'void']
    confirmed = [t for t in active if t['basis'] == 'logged' and t['status'] == 'confirmed']
    billable = [t for t in confirmed if in_period(t)]
    all_paid = [p for p in ledger['payments'] if p['status'] == 'confirmed' and p['scope'] == 'current_work']
    paid = [p for p in all_paid if in_period(p)]
    issued_ids = {ident for inv in ledger['invoices'] if inv['status'] == 'issued' for ident in inv['time_entry_ids']}
    earned = sum(entry_value(t) for t in billable)
    payment_total = sum(p['amount_cents'] for p in paid)
    uninvoiced = sum(entry_value(t) for t in billable if t['id'] not in issued_ids)
    increment = ledger['billing_increment_cents']
    initial = sum(p['amount_cents'] for p in ledger['payments'] if p['status'] == 'confirmed' and p['scope'] == 'initial_paid_artwork')
    reconciliation = reconciliation_details(ledger)
    outstanding = None if opening['amount_cents'] is None else opening['amount_cents'] + earned - payment_total
    increment_basis = max(0, outstanding) if reconciliation is not None else uninvoiced
    return {
        'schema_version': 1, 'currency': 'USD', 'timezone': ledger['timezone'],
        'default_rate_cents': ledger['default_rate_cents'],
        'coverage_note': ledger['coverage_note'], 'opening_balance': copy.deepcopy(opening),
        'balance_status': 'needs_confirmation' if opening['amount_cents'] is None else 'reconciled_opening',
        'confirmed_logged_minutes': sum(t['minutes'] for t in confirmed),
        'billable_period_minutes': sum(t['minutes'] for t in billable),
        'covered_by_opening_minutes': sum(t['minutes'] for t in confirmed if not in_period(t)),
        'pending_logged_minutes': sum(t['minutes'] for t in active if t['basis'] == 'logged' and t['status'] == 'pending'),
        'estimated_minutes': sum(t['minutes'] for t in active if t['basis'] == 'estimated'),
        'earned_cents': earned, 'confirmed_payments_cents': payment_total,
        'all_current_payments_cents': sum(p['amount_cents'] for p in all_paid),
        'initial_paid_artwork_cents': initial,
        'all_confirmed_payments_cents': initial + sum(p['amount_cents'] for p in all_paid),
        'recorded_net_change_cents': earned - payment_total,
        'outstanding_balance_cents': outstanding,
        'uninvoiced_earned_cents': uninvoiced,
        'issued_invoice_cents': sum(i['amount_cents'] for i in ledger['invoices'] if i['status'] == 'issued'),
        'draft_invoice_cents': sum(i['amount_cents'] for i in ledger['invoices'] if i['status'] == 'draft'),
        'complete_uninvoiced_increments': increment_basis // increment,
        'toward_next_increment_cents': increment_basis % increment,
        'billing_increment_cents': increment,
        'time_entries': copy.deepcopy(ledger['time_entries']), 'payments': copy.deepcopy(ledger['payments']),
        'invoices': copy.deepcopy(ledger['invoices']), 'historical_references': copy.deepcopy(ledger['historical_references']),
        'reconciliation': reconciliation}


def money(cents):
    if cents is None:
        return 'Needs confirmation'
    return ('-' if cents < 0 else '') + f'${abs(cents) // 100:,}.{abs(cents) % 100:02d}'


def duration(minutes):
    return f'{minutes // 60}h {minutes % 60:02d}m'


def safe(value):
    return str(value).replace('|', '/').replace('\n', ' ')


def render_markdown(s):
    if s['reconciliation']:
        return render_bill_statement(s)
    rows = ['# Hours and payments', '',
        'Trial report generated from [ledger.json](ledger.json). Updates when recorded evidence changes; it does not infer hours from commits or chat length.', '',
        '| Measure | Recorded value |', '| --- | --- |',
        f"| New logged time confirmed in this ledger | {duration(s['confirmed_logged_minutes'])} |",
        f"| Time awaiting confirmation | {duration(s['pending_logged_minutes'])} |",
        f"| New estimated time (excluded from earnings) | {duration(s['estimated_minutes'])} |",
        f"| Value of new confirmed time outside the opening balance | {money(s['earned_cents'])} |",
        f"| Confirmed payments for later Whitetail work, all recorded dates | {money(s['all_current_payments_cents'])} |",
        f"| Total confirmed payments recorded | {money(s['all_confirmed_payments_cents'])} |",
        f"| Current outstanding balance | {money(s['outstanding_balance_cents'])} |", '',
        s['coverage_note'], '']
    opening = s['opening_balance']
    if opening['amount_cents'] is None:
        rows += ['The starting balance and prior hours are not reconciled. A zero logged-time count means no exact entries have been added to this ledger; it does not mean no work was done. Recorded payments do not establish that all work is paid.', '']
    else:
        rows += [f"Opening balance: {money(opening['amount_cents'])}, confirmed by {safe(opening['confirmed_by'])}, covering work and payments through the end of {opening['as_of']} in America/Chicago. Older entries are displayed but do not alter that opening balance.", '']
        if s['outstanding_balance_cents'] < 0:
            rows += ['The negative outstanding amount is a recorded credit, not an amount due.', '']
    rows += ['## Invoice tracking', '',
        f"New confirmed time not yet included in an issued invoice: **{money(s['uninvoiced_earned_cents'])}**. Draft invoices in this ledger: {money(s['draft_invoice_cents'])}. Issued invoices in this ledger: {money(s['issued_invoice_cents'])}. Older invoice documents appear below as historical references.", '',
        f"At {money(s['billing_increment_cents'])} per billing increment: {s['complete_uninvoiced_increments']} complete increments and {money(s['toward_next_increment_cents'])} toward the next. This is a billing aid; no invoice is issued or sent automatically.", '',
        '## Payment record', '', '| Date | Payment | Applies to | Status | Evidence |', '| --- | --- | --- | --- | --- |']
    receipt_links = []
    for p in s['payments']:
        links = ', '.join(f'[{safe(Path(e).name)}](../../{e})' for e in p['evidence_paths'])
        rows.append(f"| {p['date'] or 'Date not supplied'} | {money(p['amount_cents'])} | {safe(p['scope'])} | {safe(p['status'])} | {links} |")
        if p.get('receipt_path'):
            receipt_links.append(f"[Payment receipt: {money(p['amount_cents'])}](../../{p['receipt_path']})")
    if not s['payments']:
        rows.append('| — | — | No receipts recorded | — | — |')
    if receipt_links:
        rows += ['', *receipt_links]
    rows += ['', '## Time record', '', '| ID / date | Work | Time | Basis / status | Value |', '| --- | --- | --- | --- | --- |']
    for t in s['time_entries']:
        rows.append(f"| {safe(t['id'])} / {t['date']} | {safe(t['description'])} | {duration(t['minutes'])} | {t['basis']} / {t['status']} | {money(entry_value(t))} |")
    if not s['time_entries']:
        rows.append('| — | Exact time entries not yet attached | — | — | — |')
    rows += ['', '## Historical references, kept outside new earnings', '', '| Reference | Hours stated | Amount stated | Evidence |', '| --- | --- | --- | --- |']
    for h in s['historical_references']:
        links = ', '.join(f'[{safe(Path(e).name)}](../../{e})' for e in h['evidence_paths'])
        rows.append(f"| {safe(h['description'])} | {duration(h['minutes'])} | {money(h['amount_cents']) if h['amount_cents'] is not None else 'Not a bill'} | {links} |")
    rows += ['', 'Historical billed/accrued hours and broader retrospective estimates may overlap. Only the explicitly confirmed reconciliation establishes the starting balance; historical references are not added to it again.', '',
        f"Ledger SHA-256: `{s.get('ledger_sha256', 'not attached')}`", '',
        'See [the workflow guide](README.md) for adding time, confirming payments and reconciling the opening balance.', '']
    return '\n'.join(rows)


def render_bill_statement(s):
    r = s['reconciliation']
    payment = next(p for p in s['payments'] if p['id'] == r['payment_id'])
    paid_minutes = r['paid_work_minutes']
    rate = s['default_rate_cents']
    rows = ['# Bills and payments', '', f'Rate: {money(rate)} per hour.', '',
            '## Bill 1 - paid', '']
    if r.get('paid_bill_invoice_date'):
        rows += [f"Invoiced: **{r['paid_bill_invoice_date']}**. Paid: **{payment['date']}**.", '']
    rows += ['| Work performed | Hours | Amount |', '| --- | --- | --- |']
    for item in r.get('paid_work_items', [{'description': 'Whitetail Syndicate project work', 'minutes': paid_minutes}]):
        value = entry_value(dict(item, rate_cents=rate))
        rows.append(f"| {safe(item['description'])} | {duration(item['minutes'])} | {money(value)} |")
    rows += [f"| **Bill total** | **{duration(paid_minutes)}** | **{money(payment['amount_cents'])}** |", '',
             f"Paid on {payment['date']}: **{money(payment['amount_cents'])}**. Balance on this bill: **$0.00**.", '']
    if payment.get('receipt_path'):
        rows += [f"[Paid receipt](../../{payment['receipt_path']})", '']
    rows += ['## Bill 2 - current accrued charges', '']
    if r.get('current_accrual_start_date'):
        rows += [f"Accrued from **{r['current_accrual_start_date']}**, recorded through **{r['as_of']}**.", '']
    rows += ['| Work performed | Hours | Amount |', '| --- | --- | --- |']
    items = list(r.get('current_work_items', [{'description': 'Current project work', 'minutes': r['current_accrued_minutes']}]))
    for t in s['time_entries']:
        if t['status'] == 'confirmed' and t['basis'] == 'logged' and t['date'] > r['as_of']:
            items.append(t)
    for item in items:
        value = entry_value(dict(item, rate_cents=item.get('rate_cents', rate)))
        rows.append(f"| {safe(item['description'])} | {duration(item['minutes'])} | {money(value)} |")
    total_minutes = sum(i['minutes'] for i in items)
    total_value = r['current_accrued_cents'] + s['earned_cents']
    rows += [f"| **Accrued charges so far** | **{duration(total_minutes)}** | **{money(total_value)}** |", '',
             f"Payments toward these charges: {money(s['confirmed_payments_cents'])}.", '',
             f"**Current accrued balance: {money(s['outstanding_balance_cents'])}.**", '',
             'See [the workflow guide](README.md) for recording future hours and payments.', '']
    if r.get('current_itemization_path'):
        rows += [f"[Current task itemization](../../{r['current_itemization_path']})", '']
    return '\n'.join(rows)


def register_changed(root, paths):
    inventory = json.loads((root / 'records/file-inventory.json').read_text())
    hashes = {f['path']: f['sha256'] for f in inventory['files']}
    source_ids = {s['id'] for s in json.loads((root / 'records/sources.json').read_text())['sources']}
    source_args = ['--source-ref', 'craig-billing-record-2026-10-09'] if 'craig-billing-record-2026-10-09' in source_ids else []
    for path in paths:
        current = hashlib.sha256((root / path).read_bytes()).hexdigest()
        if current == hashes.get(path):
            continue
        subprocess.run([sys.executable, str(root / 'scripts/record_material.py'), path,
            '--area', 'billing', '--title', Path(path).name, '--status', 'current',
            '--how', 'Maintained by the hours/payments workflow from explicit evidence-backed records.',
            '--used-for', 'Tracking recorded time, payments and reconciliation without double-counting.',
            '--source', 'Billing ledger, linked source files, and explicit confirmation records.',
            *source_args], cwd=root, check=True)


def refresh(root=ROOT, check=False):
    raw = (root / LEDGER).read_bytes()
    ledger = json.loads(raw)
    summary = summarize(ledger, root)
    summary['ledger_sha256'] = hashlib.sha256(raw).hexdigest()
    proof_paths = set(ledger['opening_balance']['evidence_paths'])
    if ledger.get('reconciliation'):
        proof_paths.update(ledger['reconciliation']['evidence_paths'])
    for group in ['time_entries', 'payments', 'invoices', 'historical_references']:
        for entry in ledger[group]:
            proof_paths.update(entry['evidence_paths'])
    summary['evidence_sha256'] = {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in sorted(proof_paths)}
    outputs = {SUMMARY_JSON: json.dumps(summary, indent=2, ensure_ascii=False) + '\n',
               SUMMARY_MD: render_markdown(summary)}
    stale = [p for p, content in outputs.items() if not (root / p).exists() or (root / p).read_text() != content]
    if check:
        if stale:
            raise ValueError('stale billing reports; run billing.py refresh: ' + ', '.join(stale))
        print(json.dumps({'result': 'PASS', 'reports_current': True}))
        return summary
    for path, content in outputs.items():
        (root / path).write_text(content)
    register_changed(root, [LEDGER, SUMMARY_JSON, SUMMARY_MD] + sorted(proof_paths))
    subprocess.run([sys.executable, str(root / 'scripts/refresh_inventory.py')], cwd=root, check=True)
    subprocess.run([sys.executable, str(root / 'scripts/validate_records.py')], cwd=root, check=True)
    print(json.dumps({'result': 'PASS', 'balance_status': summary['balance_status'],
        'confirmed_current_payments_cents': summary['all_current_payments_cents']}))
    return summary


def save(ledger, root, action, actor=None):
    validate_ledger(ledger, root)
    ledger['last_change'] = {'timestamp': datetime.now(timezone.utc).isoformat(),
                             'action': action, 'actor': actor}
    path = root / LEDGER
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)
    refresh(root)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=ROOT, help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest='command', required=True)
    ref = sub.add_parser('refresh'); ref.add_argument('--check', action='store_true')
    for name in ['add-time', 'add-payment']:
        cmd = sub.add_parser(name)
        for field in ['id', 'date', 'description']:
            cmd.add_argument('--' + field, required=True)
        cmd.add_argument('--evidence', action='append', required=True)
        if name == 'add-time':
            cmd.add_argument('--minutes', type=int, required=True)
            cmd.add_argument('--area', required=True)
            cmd.add_argument('--rate', help='USD per hour; defaults to ledger rate')
            cmd.add_argument('--basis', choices=['logged', 'estimated'], default='logged')
        else:
            cmd.add_argument('--amount', required=True)
            cmd.add_argument('--scope', choices=['current_work', 'initial_paid_artwork'], default='current_work')
            cmd.add_argument('--invoice-id')
    confirm = sub.add_parser('confirm')
    confirm.add_argument('--id', required=True); confirm.add_argument('--by', required=True)
    confirm.add_argument('--evidence', action='append', required=True)
    opening = sub.add_parser('set-opening')
    for field in ['date', 'amount', 'by']:
        opening.add_argument('--' + field, required=True)
    opening.add_argument('--evidence', action='append', required=True)
    inv = sub.add_parser('draft-invoice')
    inv.add_argument('--id', required=True); inv.add_argument('--date', required=True)
    inv.add_argument('--time-id', action='append', required=True)
    inv.add_argument('--evidence', action='append', required=True)
    void = sub.add_parser('void')
    for field in ['id', 'by', 'reason']:
        void.add_argument('--' + field, required=True)
    args = p.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == 'refresh':
            refresh(root, check=args.check); return 0
        ledger = json.loads((root / LEDGER).read_text())
        validate_ledger(ledger, root)
        if args.command == 'add-time':
            ledger['time_entries'].append({'id': args.id, 'date': args.date, 'area': args.area,
                'description': args.description, 'minutes': args.minutes,
                'rate_cents': money_to_cents(args.rate) if args.rate else ledger['default_rate_cents'],
                'basis': args.basis, 'status': 'pending', 'confirmed_by': None,
                'evidence_paths': args.evidence})
        elif args.command == 'add-payment':
            ledger['payments'].append({'id': args.id, 'date': args.date,
                'amount_cents': money_to_cents(args.amount), 'scope': args.scope,
                'status': 'pending', 'confirmed_by': None, 'description': args.description,
                'invoice_id': args.invoice_id, 'evidence_paths': args.evidence})
        elif args.command == 'set-opening':
            if ledger['opening_balance']['amount_cents'] is not None:
                raise ValueError('opening balance is already confirmed; revise only after reviewing the reconciliation and Git diff')
            ledger['opening_balance'] = {'as_of': args.date, 'amount_cents': money_to_cents(args.amount),
                'confirmed_by': args.by, 'evidence_paths': args.evidence}
        elif args.command == 'draft-invoice':
            times = {t['id']: t for t in ledger['time_entries']}
            if any(ident not in times for ident in args.time_id):
                raise ValueError('unknown time ID')
            ledger['invoices'].append({'id': args.id, 'date': args.date, 'status': 'draft',
                'time_entry_ids': args.time_id, 'amount_cents': sum(entry_value(times[i]) for i in args.time_id),
                'confirmed_by': None, 'evidence_paths': args.evidence})
        else:
            matches = [e for group in ['time_entries', 'payments', 'invoices'] for e in ledger[group] if e['id'] == args.id]
            if not matches:
                raise ValueError('unknown entry ID')
            entry = matches[0]
            if args.command == 'confirm':
                if entry['status'] not in ['pending', 'draft']:
                    raise ValueError('only pending time/payments or draft invoices can be confirmed')
                evidence(args.evidence, root)
                entry['evidence_paths'] = list(dict.fromkeys(entry['evidence_paths'] + args.evidence))
                entry.update(status='issued' if entry['status'] == 'draft' else 'confirmed', confirmed_by=args.by)
            else:
                entry.update(status='void', void_reason=args.reason, voided_by=args.by)
        save(ledger, root, args.command, getattr(args, 'by', None))
        return 0
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        p.exit(2, f'ERROR: {exc}\n')


if __name__ == '__main__':
    sys.exit(main())
