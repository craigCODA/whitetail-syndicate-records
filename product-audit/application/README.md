# Whitetail Product Control

Internal product review and change-control app for Whitetail Syndicate.

## Hard boundary

**The live Shopify store is a read-only source for this project.** This application contains no Shopify credential, Admin API client, mutation, publish, inventory, collection-write, archive, delete, or product-update path. All owner decisions, proposed titles/descriptions, design decisions, launch selections, and action states are stored locally in the browser and exported as files.

A live store change only happens later through a separate, explicitly approved process outside Product Control.

## Current baseline

- Snapshot: October 6, 2026
- 125 active products
- 1,722 variants
- 8 collections
- 31 Apliiq public vendor labels
- 54 WHITETAIL SYNDICATE public vendor labels
- 40 Yoycol public vendor labels
- Historical reference: October 1 audit, 108 products / 1,265 variants / 46 findings

## Start on Windows

Double-click `start_product_control.bat`. It starts a local web server and opens `http://localhost:4173`.

Or from a terminal:

```bash
python -m http.server 4173
```

Then open `http://localhost:4173`.

## Main workflow

1. Open **Catalog** and choose **Review next product**.
2. Read the **CURRENT LIVE LISTING** panel. This is source evidence.
3. Use **OWNER DECISION** to choose audience/placement, disposition, title direction, proposed local title/description, design mapping/decision, and launch-candidate state.
4. Save. The browser writes only to local IndexedDB.
5. Use **Designs** to approve/review/hard-reject a design. A rejection only creates local blockers for products mapped to that design.
6. Use **Duplicates** for side-by-side review. Repeated title/shared-SKU signals never merge products automatically.
7. Use **Actions** for Craig/provider follow-up and to export the five control files.
8. Use **Launch** to see provider/sample/owner gates.

## Required exports

- `Whitetail_Product_Decisions.json`
- `Whitetail_Action_Queue.csv`
- `Whitetail_Design_Decisions.json`
- `Whitetail_Launch_Catalog.csv`
- `Whitetail_Unresolved_Verification.csv`

Decision JSON can be imported back into Product Control. Imports may overlay local decisions only; attempts to alter source product fields are rejected.

## Refreshing the baseline

1. Extract a fresh Shopify catalog using **read-only** product/collection queries.
2. Save the extraction as a new dated raw snapshot under `data/raw/`.
3. Compare Shopify GIDs first; handles are secondary historical identifiers.
4. Review additions, removals, handle changes, collection membership, and products updated since the prior snapshot.
5. Run the normalizer and tests.
6. Preserve existing local decisions only where the Shopify GID identity is unambiguous.
7. Never add a Shopify token or write call to this app.

## Development verification

```bash
npm test
npm run build
```

The final safety scan should return no Shopify write implementation:

```bash
rg -n "graphql_mutation|update_product|create_product|bulk_update|set_inventory|add_to_collection|publish|archive|delete.*product|admin/api" src public scripts
```
