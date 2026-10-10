"""Financial cases use explicit test data, never production ledger entries."""
import copy
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import billing


class BillingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'evidence.md').write_text('Explicitly fictional test evidence.\n')
        self.ledger = {
            'schema_version': 1, 'currency': 'USD', 'timezone': 'America/Chicago',
            'default_rate_cents': 3000, 'billing_increment_cents': 50000,
            'opening_balance': {'as_of': None, 'amount_cents': None,
                                'confirmed_by': None, 'evidence_paths': []},
            'time_entries': [], 'payments': [], 'invoices': [],
            'historical_references': [], 'coverage_note': 'Test fixture only.'}

    def tearDown(self):
        self.temp.cleanup()

    def time(self, id='TEST-T1', **changes):
        entry = {'id': id, 'date': '2026-10-10', 'area': 'website',
                 'description': 'Fictional test task', 'minutes': 90,
                 'rate_cents': 3000, 'basis': 'logged', 'status': 'confirmed',
                 'confirmed_by': 'Test Craig', 'evidence_paths': ['evidence.md']}
        entry.update(changes)
        self.ledger['time_entries'].append(entry)
        return entry

    def payment(self, id='TEST-P1', **changes):
        entry = {'id': id, 'date': '2026-10-10', 'amount_cents': 2000,
                 'scope': 'current_work', 'status': 'confirmed',
                 'confirmed_by': 'Test Craig', 'description': 'Fictional receipt',
                 'evidence_paths': ['evidence.md'], 'invoice_id': None}
        entry.update(changes)
        self.ledger['payments'].append(entry)
        return entry

    def reconcile(self, amount=20000, as_of='2026-10-09'):
        self.ledger['opening_balance'] = {'as_of': as_of, 'amount_cents': amount,
            'confirmed_by': 'Test Craig', 'evidence_paths': ['evidence.md']}

    def summary(self):
        return billing.summarize(self.ledger, self.root)

    def test_balance_is_unknown_until_opening_is_confirmed(self):
        self.time()
        self.payment()
        s = self.summary()
        self.assertIsNone(s['outstanding_balance_cents'])
        self.assertEqual(s['recorded_net_change_cents'], 2500)

    def test_confirmed_opening_plus_time_minus_paid(self):
        self.reconcile()
        self.time()
        self.payment()
        self.assertEqual(self.summary()['outstanding_balance_cents'], 22500)

    def test_estimates_and_pending_hours_are_not_earned(self):
        self.time(basis='estimated')
        self.time('TEST-T2', status='pending', confirmed_by=None, description='Different fictional task')
        s = self.summary()
        self.assertEqual(s['earned_cents'], 0)
        self.assertEqual(s['estimated_minutes'], 90)
        self.assertEqual(s['pending_logged_minutes'], 90)

    def test_initial_paid_artwork_and_pending_receipts_are_separate(self):
        self.payment(scope='initial_paid_artwork', amount_cents=30000, date=None)
        self.payment('TEST-P2', status='pending', confirmed_by=None)
        self.assertEqual(self.summary()['confirmed_payments_cents'], 0)
        self.assertEqual(self.summary()['initial_paid_artwork_cents'], 30000)

    def test_historical_documents_are_not_added_to_new_time(self):
        self.ledger['historical_references'] = [
            {'id': 'TEST-H1', 'kind': 'invoice_stated', 'minutes': 1000,
             'amount_cents': 50000, 'description': 'Invoice fixture',
             'evidence_paths': ['evidence.md']},
            {'id': 'TEST-H2', 'kind': 'retrospective_estimate', 'minutes': 3450,
             'amount_cents': None, 'description': 'Overlapping estimate fixture',
             'evidence_paths': ['evidence.md']}]
        self.assertEqual(self.summary()['earned_cents'], 0)
        self.assertIsNone(self.summary()['outstanding_balance_cents'])

    def test_opening_covers_its_date_and_all_earlier_entries(self):
        self.reconcile()
        self.time(date='2026-10-09')
        self.payment(date='2026-10-08')
        self.assertEqual(self.summary()['outstanding_balance_cents'], 20000)
        self.assertEqual(self.summary()['covered_by_opening_minutes'], 90)

    def test_each_entry_is_rounded_in_cents_without_float_drift(self):
        self.time(minutes=1, rate_cents=3101)
        self.assertEqual(self.summary()['earned_cents'], 52)
        self.assertEqual(billing.money_to_cents('123.05'), 12305)

    def test_duplicate_ids_and_repeated_identical_time_fail(self):
        self.time()
        self.time()
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.summary()
        self.ledger['time_entries'][1]['id'] = 'TEST-T2'
        with self.assertRaisesRegex(ValueError, 'repeated time'):
            self.summary()

    def test_reused_receipt_evidence_requires_distinct_record(self):
        self.payment()
        self.payment('TEST-P2')
        with self.assertRaisesRegex(ValueError, 'repeated payment'):
            self.summary()

    def test_negative_boolean_and_fractional_minutes_fail(self):
        for bad in [-1, True, 1.5]:
            self.ledger['time_entries'] = []
            self.time(minutes=bad)
            with self.assertRaises(ValueError):
                self.summary()

    def test_unknown_status_invalid_date_and_missing_evidence_fail(self):
        for change in [{'status': 'paid'}, {'date': '2026-02-30'},
                       {'evidence_paths': []}, {'evidence_paths': ['../escape.md']},
                       {'evidence_paths': ['missing.md']}, {'confirmed_by': None}]:
            self.ledger['time_entries'] = []
            self.time(**change)
            with self.assertRaises(ValueError):
                self.summary()

    def test_invoice_does_not_add_the_same_hours_again(self):
        self.reconcile(0)
        self.time()
        self.ledger['invoices'] = [{'id': 'TEST-I1', 'date': '2026-10-10',
            'status': 'issued', 'time_entry_ids': ['TEST-T1'], 'amount_cents': 4500,
            'confirmed_by': 'Test Craig', 'evidence_paths': ['evidence.md']}]
        s = self.summary()
        self.assertEqual(s['outstanding_balance_cents'], 4500)
        self.assertEqual(s['uninvoiced_earned_cents'], 0)

    def test_time_cannot_be_in_two_invoices(self):
        self.time()
        inv = {'id': 'TEST-I1', 'date': '2026-10-10', 'status': 'draft',
            'time_entry_ids': ['TEST-T1'], 'amount_cents': 4500,
            'confirmed_by': None, 'evidence_paths': ['evidence.md']}
        self.ledger['invoices'] = [inv, dict(inv, id='TEST-I2')]
        with self.assertRaisesRegex(ValueError, 'already reserved'):
            self.summary()

    def test_unconfirmed_or_estimated_time_cannot_be_invoiced(self):
        self.time(basis='estimated')
        self.ledger['invoices'] = [{'id': 'TEST-I1', 'date': '2026-10-10',
            'status': 'draft', 'time_entry_ids': ['TEST-T1'], 'amount_cents': 4500,
            'confirmed_by': None, 'evidence_paths': ['evidence.md']}]
        with self.assertRaisesRegex(ValueError, 'confirmed logged time'):
            self.summary()

    def test_wrong_invoice_amount_and_excess_allocation_fail(self):
        self.time()
        inv = {'id': 'TEST-I1', 'date': '2026-10-10', 'status': 'issued',
            'time_entry_ids': ['TEST-T1'], 'amount_cents': 4501,
            'confirmed_by': 'Test Craig', 'evidence_paths': ['evidence.md']}
        self.ledger['invoices'] = [inv]
        with self.assertRaisesRegex(ValueError, 'invoice amount'):
            self.summary()
        inv['amount_cents'] = 4500
        self.payment(amount_cents=5000, invoice_id='TEST-I1')
        with self.assertRaisesRegex(ValueError, 'exceeds invoice'):
            self.summary()

    def test_overpayment_is_a_credit_and_voids_are_excluded(self):
        self.reconcile(0)
        self.time(minutes=10)
        self.payment(amount_cents=2000)
        self.assertEqual(self.summary()['outstanding_balance_cents'], -1500)
        self.ledger['payments'][0].update(status='void', void_reason='Test correction',
                                        voided_by='Test Craig')
        self.assertEqual(self.summary()['outstanding_balance_cents'], 500)

    def test_500_increment_uses_exact_minutes(self):
        self.time(minutes=1000)
        s = self.summary()
        self.assertEqual(s['earned_cents'], 50000)
        self.assertEqual(s['complete_uninvoiced_increments'], 1)
        self.assertEqual(s['toward_next_increment_cents'], 0)

    def test_nonfinite_exponents_and_subcent_money_fail(self):
        for value in ['NaN', 'Infinity', '-1', '1e3', '0.001']:
            with self.assertRaises(ValueError):
                billing.money_to_cents(value)

    def itemized_bills(self):
        self.time('TEST-WEB', date='2026-10-09', minutes=300)
        self.payment(amount_cents=56000, date='2026-10-09')
        self.reconcile(31000)
        self.ledger['reconciliation'] = {
            'as_of': '2026-10-09', 'confirmed_by': 'Test Craig',
            'payment_id': 'TEST-P1', 'evidence_paths': ['evidence.md'],
            'paid_bill_invoice_date': '2026-10-07',
            'current_accrual_start_date': '2026-10-07',
            'paid_work_items': [{'description': 'Fictional paid work', 'minutes': 1120}],
            'current_work_items': [
                {'description': 'Fictional current work', 'minutes': 320},
                {'description': 'Fictional website work', 'minutes': 300,
                 'time_entry_id': 'TEST-WEB'}]}

    def test_itemized_bills_match_receipt_and_current_balance(self):
        self.itemized_bills()
        s = self.summary()
        self.assertEqual(s['all_confirmed_payments_cents'], 56000)
        self.assertEqual(s['outstanding_balance_cents'], 31000)
        self.assertEqual(s['reconciliation']['paid_work_minutes'], 1120)
        self.assertEqual(s['reconciliation']['current_accrued_minutes'], 620)
        self.assertEqual(s['toward_next_increment_cents'], 31000)
        self.assertEqual(len(s['payments']), 1)
        statement = billing.render_markdown(s)
        self.assertIn('18h 40m', statement)
        self.assertIn('10h 20m', statement)
        self.assertIn('$560.00', statement)
        self.assertIn('$310.00', statement)
        for unwanted in ['corrected', 'reissued', 'transfer', 'removed tasks']:
            self.assertNotIn(unwanted, statement.lower())

    def test_itemized_opening_does_not_repeat_covered_time_or_payment(self):
        self.itemized_bills()
        self.time('TEST-NEXT', date='2026-10-10', minutes=60, description='Fictional next task')
        self.assertEqual(self.summary()['outstanding_balance_cents'], 34000)
        self.payment('TEST-NEXT-PAY', amount_cents=3000, date='2026-10-10')
        self.assertEqual(self.summary()['outstanding_balance_cents'], 31000)

    def test_itemized_paid_amount_must_match_payment(self):
        self.itemized_bills()
        self.ledger['reconciliation']['paid_work_items'][0]['minutes'] -= 1
        with self.assertRaisesRegex(ValueError, 'paid work'):
            self.summary()

    def test_itemized_current_amount_must_match_opening(self):
        self.itemized_bills()
        self.ledger['opening_balance']['amount_cents'] = 30000
        with self.assertRaisesRegex(ValueError, 'opening balance'):
            self.summary()

    def test_itemized_dates_must_cover_work_and_payment(self):
        self.itemized_bills()
        self.ledger['reconciliation']['paid_bill_invoice_date'] = '2026-10-10'
        with self.assertRaisesRegex(ValueError, 'invoice date'):
            self.summary()
        self.ledger['reconciliation']['paid_bill_invoice_date'] = '2026-10-07'
        self.ledger['reconciliation']['current_accrual_start_date'] = '2026-10-10'
        with self.assertRaisesRegex(ValueError, 'accrual period'):
            self.summary()

    def test_itemized_linked_time_must_match_confirmed_entry(self):
        self.itemized_bills()
        self.ledger['time_entries'][0]['status'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'confirmed logged time'):
            self.summary()
        self.ledger['time_entries'][0]['status'] = 'confirmed'
        self.ledger['time_entries'][0]['minutes'] = 299
        with self.assertRaisesRegex(ValueError, 'linked time'):
            self.summary()

    def test_itemized_work_must_be_distinct_and_nonempty(self):
        self.itemized_bills()
        current = self.ledger['reconciliation']['current_work_items']
        current.append(dict(current[0]))
        with self.assertRaisesRegex(ValueError, 'distinct'):
            self.summary()
        current.pop()
        current[0]['minutes'] = 0
        with self.assertRaisesRegex(ValueError, 'minutes'):
            self.summary()
        self.ledger['reconciliation']['paid_work_items'] = []
        with self.assertRaises(ValueError):
            self.summary()


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'records-trial'
        source = Path(__file__).resolve().parents[1]
        shutil.copytree(source, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules'))
        self.proof = 'records/billing/evidence/TEST-ONLY-FICTIONAL.md'
        ledger_path = self.root / 'records/billing/ledger.json'
        ledger = json.loads(ledger_path.read_text())
        ledger['opening_balance'] = {'as_of': None, 'amount_cents': None, 'confirmed_by': None, 'evidence_paths': []}
        for group in ['time_entries', 'payments', 'invoices', 'historical_references']:
            ledger[group] = []
        ledger.pop('reconciliation', None)
        ledger['coverage_note'] = 'Fictional workflow fixture; not Craig’s actual ledger.'
        ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, str(self.root / 'scripts/billing.py'), *args],
                                cwd=self.root, capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def summary(self):
        return json.loads((self.root / 'records/billing/summary.json').read_text())

    def test_complete_time_invoice_payment_flow_without_double_counting(self):
        (self.root / self.proof).write_text('Fictional test inputs only; not Craig’s actual work or receipts.\n')
        self.run_cli('set-opening', '--date', '2026-10-09', '--amount', '200', '--by', 'Fictional test user', '--evidence', self.proof)
        self.run_cli('add-time', '--id', 'TEST-T1', '--date', '2026-10-10', '--minutes', '90', '--area', 'website', '--description', 'Fictional task', '--evidence', self.proof)
        self.assertEqual(self.summary()['outstanding_balance_cents'], 20000)
        self.run_cli('confirm', '--id', 'TEST-T1', '--by', 'Fictional test user', '--evidence', self.proof)
        self.assertEqual(self.summary()['outstanding_balance_cents'], 24500)
        self.run_cli('draft-invoice', '--id', 'TEST-I1', '--date', '2026-10-10', '--time-id', 'TEST-T1', '--evidence', self.proof)
        self.run_cli('confirm', '--id', 'TEST-I1', '--by', 'Fictional test user', '--evidence', self.proof)
        self.assertEqual(self.summary()['outstanding_balance_cents'], 24500)
        self.assertEqual(self.summary()['uninvoiced_earned_cents'], 0)
        self.run_cli('add-payment', '--id', 'TEST-P1', '--date', '2026-10-10', '--amount', '20', '--description', 'Fictional receipt', '--invoice-id', 'TEST-I1', '--evidence', self.proof)
        self.assertEqual(self.summary()['outstanding_balance_cents'], 24500)
        self.run_cli('confirm', '--id', 'TEST-P1', '--by', 'Fictional test user', '--evidence', self.proof)
        self.assertEqual(self.summary()['outstanding_balance_cents'], 22500)
        self.run_cli('refresh', '--check')
        original = (self.root / 'records/billing/ledger.json').read_bytes()
        self.run_cli('void', '--id', 'TEST-T1', '--by', 'Fictional test user', '--reason', 'Test invalid correction', success=False)
        self.assertEqual((self.root / 'records/billing/ledger.json').read_bytes(), original)

    def test_refresh_is_idempotent_and_checks_stale_reports(self):
        self.run_cli('refresh')
        activity = (self.root / 'records/activity.jsonl').read_bytes()
        self.run_cli('refresh')
        self.assertEqual((self.root / 'records/activity.jsonl').read_bytes(), activity)
        ledger_path = self.root / 'records/billing/ledger.json'
        ledger = json.loads(ledger_path.read_text())
        ledger['coverage_note'] += ' Fictional freshness test.'
        ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')
        self.run_cli('refresh', '--check', success=False)
        self.run_cli('refresh')
        self.run_cli('refresh', '--check')
        self.assertEqual(self.summary()['all_confirmed_payments_cents'], 0)
        self.assertIsNone(self.summary()['outstanding_balance_cents'])

    def test_source_edits_invalidate_the_evidence_snapshot(self):
        (self.root / self.proof).write_text('Fictional test evidence.\n')
        self.run_cli('add-time', '--id', 'TEST-FRESH', '--date', '2026-10-10', '--minutes', '15', '--area', 'website', '--description', 'Fictional freshness task', '--evidence', self.proof)
        self.run_cli('refresh')
        proof = self.root / self.proof
        proof.write_text(proof.read_text() + '\nFictional test-only evidence revision.\n')
        self.run_cli('refresh', '--check', success=False)
        self.run_cli('refresh')
        self.run_cli('refresh', '--check')


if __name__ == '__main__':
    unittest.main()
