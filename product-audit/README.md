# Product audit and owner review

## Evidence and tools

- [October 1 audit extraction](evidence/2026-10-01-site-audit-readable.md): 108-product / 1,265-variant historical baseline and 46 findings.
- [October 3 follow-up audit](evidence/2026-10-03-site-audit.pdf) and [readable extraction](evidence/2026-10-03-site-audit-readable.md).
- [Original Product Control application](application/README.md): October 6 baseline, 125 products, 1,722 variants and eight collections. Source, built files, raw data, normalized data and original tests were imported from the archive.
- [Kraig's offline review](review/kraig-offline-review.html), [compact print review](review/compact-printable-review.html) and [original printable review](review/original-printable-review.html).
- [Affordable 2x pricing proposal](pricing/affordable-2x-proposal.xlsx) and [earlier pricing proposal](pricing/earlier-tier-proposal.xlsx), with readable worksheet JSON under pricing/exports.

## How the work was done

The storefront and catalog were reviewed for collection placement, duplicate signals, naming, pricing, artwork, variants and shopping friction. Dated Shopify data were retained. The application separates the current listing from local owner decisions and exports the action queue; it has no live-store write path.

The review workbooks let the owner identify removals, colors to remove, proposed prices and notes. A repeated title is a review signal, not automatic proof of a duplicate. Saved spreadsheet values were extracted without recalculating or modifying their original formulas.

## How to use it

Follow application/README.md to start Product Control. Read the listing, save the owner's decision locally, export the decision files, and put the returned export in decisions/ with its date. Keep pricing alternatives separate until the owner selects one. The exported change list is the implementation handoff.

The imported application uses historical data. Refresh the read-only catalog and compare stable product IDs before applying decisions to the present store. No returned owner decision export or approved live change list has been found in the imported material.

Application runtime verification is recorded in records/verification.md; importing old tests does not itself mean they have passed today.
