# Hours and payments trial

This trial is on `trial/hours-payments`. Read [the current summary](summary.md). Inputs live in [ledger.json](ledger.json); [summary.json](summary.json) provides the same results for agents.

**Bill 1: $560 for 18h40m, invoiced October 7 and paid October 9. Bill 2: $310 current accrued charges for 10h20m, October 7 through October 9.** See [the bill and receipt](receipts/WTS-Bills-2026-10-09.pdf), [current itemization](current-itemization.md), and [billing record](evidence/2026-10-09-billing-record.md). The documents present the itemized work, dates, amounts and payment status.

The $310 opening balance covers work and payments through the end of October 9. It includes the five website hours and the $560 receipt; neither is counted again. Future confirmed entries after October 9 adjust it. Earlier broader effort estimates remain historical references.

The generated summary includes a balance confidence note for the itemized opening balance. Its date comes from the confirmed itemization; the evidence note is recorded in `ledger.json` under `reconciliation.evidence_note`. Independent time logs for the current itemization are not present. If such material is attached, link it in the reconciliation evidence and update the evidence note from that source. Do not infer a stronger evidence class from the report's exact minute display. See [billing provenance](provenance.md) and [evidence standards](../evidence-standards.md).

## How it stays current

1. At the end of a task, record actual minutes only when Craig supplied or confirmed them. An agent's effort estimate is recorded with `basis: estimated` and cannot become earnings just by confirming it.
2. Link a saved note, source or receipt. New time and payment records start pending.
3. Confirm the record only from an explicit user statement or suitable payment/time evidence. Keep the confirmer and evidence attached.
4. Run `python3 scripts/billing.py refresh`. This regenerates the summary, records changed materials/activity and refreshes and validates the main inventory.
5. Review and commit the changes on the trial branch. The GitHub workflow tests calculations, regenerates reports and commits any updated reports to this same branch.

The workflow uses recorded inputs. It does not monitor every chat, infer elapsed hours from commits, read a bank account, or send invoices. If GitHub Actions is disabled or branch writes are blocked, the local refresh command performs the same work.

## Agent prompts Craig can use

- “Log the actual time I give you for this work, with the work date and supporting note, then update the hours report.”
- “I received this amount on this date. Record the payment against later Whitetail work and update the report.”
- “Show me the pending time entries so I can confirm or correct them.”

Do not infer an actual duration from a statement that work was completed. An invoice marked issued is distinct from a payment marked received.

## Commands

These are command templates, not additional work or payments. Replace every capitalized token with actual information and save the evidence note first.

```bash
python3 scripts/billing.py add-time --id UNIQUE-TIME-ID --date YYYY-MM-DD --minutes ACTUAL-MINUTES --area website --description "Actual task description" --evidence records/billing/evidence/ACTUAL-NOTE.md
python3 scripts/billing.py confirm --id UNIQUE-TIME-ID --by "Craig Ramos" --evidence records/billing/evidence/ACTUAL-CONFIRMATION.md

python3 scripts/billing.py add-payment --id UNIQUE-RECEIPT-ID --date YYYY-MM-DD --amount ACTUAL-USD-AMOUNT --description "Actual payment received" --evidence records/billing/evidence/ACTUAL-RECEIPT.md
python3 scripts/billing.py confirm --id UNIQUE-RECEIPT-ID --by "Craig Ramos" --evidence records/billing/evidence/ACTUAL-RECEIPT.md

python3 scripts/billing.py refresh
python3 scripts/billing.py refresh --check
python3 -m unittest discover -s tests -v
```

The helper registers newly linked evidence and refreshes the ledger and reports automatically after each successful mutation. Register other deliverables with `scripts/record_material.py` using the repository's ordinary instructions. Source hashes in summary.json record the exact evidence versions used by each report.

## Confirming the starting point

Before displaying an amount due, Craig must confirm a remaining balance **after accounting for all work and payments through the end of a stated date**. This amount covers the itemized accrued work and recorded payments through that date. New confirmed time and payments after that date change the balance. Earlier entries remain visible and do not change it again.

```bash
python3 scripts/billing.py set-opening --date YYYY-MM-DD --amount CONFIRMED-REMAINING-USD --by "Craig Ramos" --evidence records/billing/evidence/ACTUAL-RECONCILIATION.md
```

The confirmed opening balance is $310 through October 9. Historical effort estimates are not additional billable hours.

The single PDF contains the paid bill/receipt on page 1 and the itemized current accrued charges on page 2. The report stays current as new activity is recorded.

The [bill and receipt PDF](receipts/WTS-Bills-2026-10-09.pdf) can be reproduced with `python3 scripts/create_billing_receipt.py` after installing ReportLab (verified with version 4.4.9). This optional PDF builder is separate from the automated report workflow. Reproducing a historical receipt is not a new payment or charge.


## Invoice tracking

`draft-invoice --id ID --date YYYY-MM-DD --time-id CONFIRMED-TIME-ID --evidence PATH` reserves distinct confirmed logged time, using the recorded per-entry rate. Repeat `--time-id` for more entries. `confirm --id INVOICE-ID --by NAME --evidence PATH` marks a draft issued only when actual issuance evidence exists. Issuing an invoice does not add the hours to earnings twice.

Use `void --id ID --by NAME --reason "Reason"` to void an entry. Referenced time cannot be voided while an active invoice uses it. Review the Git diff; do not delete financial history or silently change a confirmed opening balance.

The configured rate is $30/hour. The ledger holds the billing increment used by the workflow. Rate changes are explicit per-entry data. Amounts use integer cents and round each time entry once to the nearest cent. Drafts and estimates do not become bills automatically.

## Trial verification and promotion

The tests use clearly fictional data in temporary directories. They cover balance reconciliation, estimates, pending entries, duplicate records, invoice overlap, payment allocation, rounding, credits, void entries and report freshness. No sample entries are added to Craig's ledger.

The Actions trigger and push destination are restricted to `trial/hours-payments`. Before adopting this on main, review the report, confirmed reconciliation and workflow, and deliberately change the branch trigger/destination as part of the merge. Manual workflow dispatch is not configured for this trial.

Workflow reference: [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [token behavior](https://docs.github.com/en/actions/concepts/security/github_token). Workflow-generated pushes use the repository token and do not recursively run the push workflow.
