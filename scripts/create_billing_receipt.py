#!/usr/bin/env python3
"""Rebuild the dated $560 receipt from its confirmed reconciliation.

Requires ReportLab (verified with 4.4.9). The live billing workflow uses only
the standard library and does not rewrite this historical payment receipt.
"""
from datetime import date
import json
from pathlib import Path

import reportlab
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from billing import ROOT, LEDGER, duration, entry_value, money, summarize


def date_label(value):
    return date.fromisoformat(value).strftime('%B %d, %Y').replace(' 0', ' ')


def main():
    ledger = json.loads((ROOT / LEDGER).read_text())
    details = summarize(ledger, ROOT)['reconciliation']
    if details is None:
        raise ValueError('A confirmed reconciliation is required for this receipt.')
    payment = next(p for p in ledger['payments'] if p['id'] == details['payment_id'])
    if payment['id'] != 'PAY-2026-10-09-560' or payment['amount_cents'] != 56000:
        raise ValueError('This builder is for the confirmed October 9 $560 receipt only.')
    output = ROOT / payment['receipt_path']
    if not output.resolve().is_relative_to(ROOT):
        raise ValueError('Receipt output must remain inside the repository.')
    output.parent.mkdir(parents=True, exist_ok=True)
    fonts = Path(reportlab.__file__).parent / 'fonts'
    pdfmetrics.registerFont(TTFont('ReceiptSans', str(fonts / 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('ReceiptSansBold', str(fonts / 'VeraBd.ttf')))
    canvas = Canvas(str(output), pagesize=letter, invariant=1)
    canvas.setTitle('Whitetail Syndicate - Payment Receipt WTS-R-2026-1009-560')
    canvas.setAuthor('Craig Ramos')
    ink = HexColor('#172C25')
    muted = HexColor('#596B63')
    green = HexColor('#245D47')
    pale = HexColor('#F0F5F2')
    line = HexColor('#D8E2DC')

    def label(x, y, text, size=10, bold=False, color=ink, right=False):
        canvas.setFont('ReceiptSansBold' if bold else 'ReceiptSans', size)
        canvas.setFillColor(color)
        if right:
            canvas.drawRightString(x, y, text)
        else:
            canvas.drawString(x, y, text)

    def rule(y):
        canvas.setStrokeColor(line)
        canvas.setLineWidth(0.7)
        canvas.line(48, y, 564, y)

    label(48, 746, 'WHITETAIL SYNDICATE', 11, True, green)
    label(48, 707, 'Bill and receipt', 26, True)
    label(48, 681, 'WTS-R-2026-1009-560', 10, color=muted)
    label(564, 707, 'PAID', 11, True, green, True)
    label(564, 677, money(payment['amount_cents']), 25, True, green, True)
    rule(655)

    label(48, 633, 'RECEIVED FROM', 8, True, muted)
    label(48, 615, 'Whitetail Syndicate', 11)
    label(310, 633, 'RECEIVED BY', 8, True, muted)
    label(310, 615, payment['confirmed_by'], 11)
    label(48, 595, 'Invoiced on ' + date_label(details['paid_bill_invoice_date']), 10, color=muted)
    label(48, 578, 'Paid on ' + date_label(payment['date']), 10, color=muted)
    label(564, 589, 'Rate: $30.00 per hour', 10, color=muted, right=True)

    label(48, 557, 'Bill 1 - paid in full', 14, True)
    canvas.setFillColor(pale)
    canvas.rect(48, 523, 516, 23, fill=1, stroke=0)
    label(60, 531, 'WORK PERFORMED', 8, True, muted)
    label(440, 531, 'HOURS', 8, True, muted, True)
    label(552, 531, 'AMOUNT', 8, True, muted, True)
    paid_items = details['paid_work_items']
    for i, item in enumerate(paid_items):
        y = 509 - i * 17
        label(60, y, item['description'], 8.7)
        label(440, y, duration(item['minutes']), 9, right=True)
        label(552, y, money(entry_value(dict(item, rate_cents=ledger['default_rate_cents']))),
              9, right=True)
    rule(294)
    paid_minutes = sum(item['minutes'] for item in paid_items)
    label(60, 276, 'Bill total', 10, True)
    label(440, 276, duration(paid_minutes), 10, True, right=True)
    label(552, 276, money(payment['amount_cents']), 11, True, right=True)
    label(60, 256, 'Paid', 10, True, green)
    label(552, 256, money(payment['amount_cents']), 11, True, green, True)
    label(60, 236, 'Balance on this bill', 10)
    label(552, 236, '$0.00', 10, right=True)

    canvas.setFillColor(green)
    canvas.roundRect(48, 170, 516, 42, 5, fill=1, stroke=0)
    label(60, 186, 'PAID IN FULL', 11, True, white)
    label(552, 185, money(payment['amount_cents']), 19, True, white, True)
    label(48, 142, 'Receipt for payment received ' + date_label(payment['date']) + '.',
          10, color=muted)
    label(48, 65, 'Craig Ramos | Whitetail Syndicate', 9, color=muted)
    label(564, 65, '1 / 2', 9, color=muted, right=True)
    canvas.showPage()

    label(48, 746, 'WHITETAIL SYNDICATE', 11, True, green)
    label(48, 707, 'Current accrued charges', 24, True)
    label(48, 681, 'Bill 2', 10, color=muted)
    label(564, 707, 'ACCRUED', 10, True, green, True)
    label(564, 677, money(details['current_accrued_cents']), 25, True, green, True)
    rule(655)
    label(48, 633, 'CLIENT', 8, True, muted)
    label(48, 615, 'Whitetail Syndicate', 11)
    label(310, 633, 'PREPARED BY', 8, True, muted)
    label(310, 615, payment['confirmed_by'], 11)
    label(48, 589, 'Accrued October 7 - October 9, 2026', 10, color=muted)
    label(564, 589, 'Rate: $30.00 per hour', 10, color=muted, right=True)
    label(48, 557, 'Itemized current work', 14, True)
    canvas.setFillColor(pale)
    canvas.rect(48, 523, 516, 23, fill=1, stroke=0)
    label(60, 531, 'WORK PERFORMED', 8, True, muted)
    label(440, 531, 'HOURS', 8, True, muted, True)
    label(552, 531, 'AMOUNT', 8, True, muted, True)
    for i, item in enumerate(details['current_work_items']):
        y = 509 - i * 20
        label(60, y, item['description'], 8.7)
        label(440, y, duration(item['minutes']), 9, right=True)
        label(552, y, money(entry_value(dict(item, rate_cents=ledger['default_rate_cents']))),
              9, right=True)
    current_table_bottom = 509 - (len(details['current_work_items']) - 1) * 20 - 15
    rule(current_table_bottom)
    label(60, current_table_bottom - 18, 'Current accrued total', 10, True)
    label(440, current_table_bottom - 18, duration(details['current_accrued_minutes']), 10, True, right=True)
    label(552, current_table_bottom - 18, money(details['current_accrued_cents']), 11, True, right=True)
    label(60, current_table_bottom - 38, 'Payments against these charges', 10)
    label(552, current_table_bottom - 38, '$0.00', 10, right=True)
    canvas.setFillColor(green)
    current_banner_bottom = current_table_bottom - 124
    canvas.roundRect(48, current_banner_bottom, 516, 42, 5, fill=1, stroke=0)
    label(60, current_banner_bottom + 16, 'CURRENT ACCRUED', 11, True, white)
    label(552, current_banner_bottom + 15, money(details['current_accrued_cents']), 19, True, white, True)
    label(48, current_banner_bottom - 28, 'Status: unpaid. Charges recorded through ' + date_label(details['as_of']) + '.',
          10, color=muted)
    label(48, 65, 'Craig Ramos | Whitetail Syndicate', 9, color=muted)
    label(564, 65, '2 / 2', 9, color=muted, right=True)
    canvas.showPage()
    canvas.save()
    print(output.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
