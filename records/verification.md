# Verification record

## Records import

Original source files were materialized from their current authorized versions. Imported binary files retain their source hashes. PDF text and worksheet JSON are labeled readable derivatives. Worksheet extraction preserved saved values/formula text and did not recalculate or edit original workbooks. Large HTML captures have readable extracts and source locators.

The original background call transcript contains credential discussion. That discussion was removed from the repository copy; the original source was not modified.

Run `python3 scripts/refresh_inventory.py` followed by `python3 scripts/validate_records.py` to check record structure, file hashes, source references, paths and local Markdown links.

On 2026-10-10 UTC, both commands passed for the initial import: 293 registered materials, 31 sources, 295 verified file hashes, and 13 authored Markdown link checks. The generated directory and inventory can be rebuilt from the editable material register.

## Product Control application

Source, build and original tests were imported unchanged from the dated archive. On 2026-10-10 UTC, `npm test` in `product-audit/application` passed: 38 tests passed, 0 failed, and 0 skipped. This checks the imported application locally; it does not confirm live Shopify operations or returned owner decisions. Run the application's documented `npm test` and `npm run build` when changing it.

## Hours/payments trial

Branch: `trial/hours-payments`. The billing workflow uses confirmed itemized bills and an opening balance through October 9.

All 28 tests pass. Coverage includes itemized paid/current totals, linked time evidence, date ordering, payment status, duplicate records, amount mismatches, estimates, rounding, invoice overlap, credits, later time/payments, report freshness and idempotent refresh. Test data stays in temporary directories.

The bill and receipt PDF has two pages. Page 1 is $560 for 18h40m, invoiced October 7 and paid October 9, with a zero balance. Page 2 is $310 accrued for 10h20m, October 7 through October 9. Its pages are checked by text extraction, item totals, word bounds and visual rendering.

Run `python3 scripts/billing.py refresh --check` and `python3 scripts/validate_records.py` to verify current reports, evidence, registered paths, local links and inventory hashes. The GitHub Actions workflow is restricted to the trial branch.

## External outcomes

No live Shopify changes, website deployment, new outreach email, Drive upload or form-delivery fix was performed by this import. The private repository is the record and handoff.

## Evidence and report confidence

On October 10, 2026, the 28 billing tests passed with the evidence note included in the generated report. A temporary in-memory future-hours check confirmed that the confidence note remains scoped to the October 9 opening balance while subsequent confirmed entries affect the calculated balance. No temporary verification entry was saved.

The financial ledger values, paid/current task splits and receipt PDF bytes match the confirmed billing record. The evidence note describes the itemization's support; it does not add work, charges or payment evidence. The evidence standards and billing provenance links are included in the record validator. Validation passed for 304 registered materials, 32 sources, 306 inventoried file hashes and 17 authored Markdown link checks.
