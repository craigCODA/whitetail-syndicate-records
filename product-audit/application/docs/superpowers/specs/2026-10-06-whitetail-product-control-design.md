# Whitetail Product Control — Design Specification

**Date:** 2026-10-06  
**Project:** Whitetail Syndicate  
**Primary users:** Kraig (owner/decision maker), Craig (catalog/brand operator), Lori (context/contributor as assigned)

## 1. Purpose

Build a simple internal review application that turns the completed October 1 storefront audit plus a fresh read-only Shopify inventory snapshot into a controlled product-decision workflow.

The application will show every current Whitetail Syndicate product discovered from Shopify, where it appears on the storefront, the product's current title/description/collections/design/vendor/variants, and the audit flags already discovered. Kraig can make structured decisions without editing Shopify directly. Craig receives an exact action queue from those decisions.

The first version is a **decision and change-control tool**, not a live Shopify editor.

## 2. Why this exists

The October 1 audit established a public catalog baseline of 108 products and 1,265 variants and identified catalog, collection, artwork, navigation, description, SKU, and provider-verification issues. A fresh read-only Shopify inventory check on October 6 established the current baseline at 125 active products and 1,722 variants. The current catalog contains 18 handles not present in the October 1 audit and is missing one handle that was present then (`cotton-blend-cap`). The launch plan already requires each listing to receive an intentional keep/merge/repair/draft/retire decision before the catalog is treated as controlled.

The current gap is not discovery. The gap is converting the audit into owner decisions that can be executed safely and traced later.

## 3. Success criteria

Version 1 is successful when:

1. All 125 products in the October 6 live Shopify baseline are represented once in the app.
2. Kraig can review products one-by-one or filter to flagged products.
3. Each product clearly shows its **current state** before a decision is made.
4. Each product can receive explicit decisions for collection placement, launch status, naming, description, and design.
5. A design can be globally rejected once, and every product using that design becomes flagged for action.
6. Duplicate/merge candidates can be reviewed side-by-side without automatically merging anything.
7. The app distinguishes **owner decisions** from **provider facts that still require verification**.
8. No action in Version 1 can modify the live Shopify store.
9. Decisions persist locally and can be exported in a machine-readable form.
10. Craig can export a prioritized action queue that says exactly what to change and why.

## 4. Non-goals for Version 1

Version 1 will not:

- write changes to Shopify;
- delete, publish, archive, or merge live products;
- modify POD/provider mappings;
- approve a provider route based only on public vendor labels;
- calculate final margins without verified private provider costs;
- replace the launch project board;
- become a general CRM, ERP, warehouse system, or customer service platform.

These constraints are intentional safety boundaries.

## 5. Source of truth

### Current live baseline

The current catalog source of truth is the read-only Shopify inventory snapshot captured October 6, 2026. At capture time it contained:

- 125 active products;
- 1,722 variants;
- 31 Apliiq-labeled products;
- 54 WHITETAIL SYNDICATE-labeled products;
- 40 Yoycol-labeled products;
- 8 collections;
- 18 product handles added since the October 1 audit;
- 1 October 1 product handle no longer present;
- 28 current products updated on or after October 1.

The eight current collections are Home page, The Buck Collection, The Doe Collection, The Yearling Collection, The Fawn Collection, Hats & Beanies, Gear & Accessories, and Rutline. Rutline currently contains zero products.

### Historical audit baseline

The October 1, 2026 Whitetail Syndicate site audit remains the historical evidence source for:

- 108 public products;
- 1,265 variants;
- current titles and handles;
- public vendor labels;
- public prices;
- product types;
- option/variant data;
- descriptions;
- image references/previews;
- observed collection placement where captured;
- audit findings and priority flags;
- duplicate-title groups;
- repeated SKU findings;
- known broken-description links;
- collection-merchandising flags.

### Private verification fields

Private provider and business facts are stored separately as `unknown`, `verified`, or `not_applicable` until the business confirms them. Examples:

- actual POD route;
- provider product ID;
- provider variant ID;
- decorated cost;
- shipping cost;
- provider tax;
- stock/substitution behavior;
- current open-order dependency;
- sample status.

The app must never infer these private facts from a public vendor label.

## 6. Users and decision rights

### Kraig — owner decision maker

Kraig can:

- approve/hold/retire a product;
- choose intended audience/collection placement;
- accept or reject a design;
- globally reject a design;
- approve or reject title/description direction;
- request investigation;
- add decision notes.

### Craig — catalog and brand operator

Craig can:

- load/update audit data;
- map known designs to product placements;
- propose titles/descriptions;
- attach investigation results;
- resolve action items after owner decisions;
- mark execution status;
- export the final change manifest.

### Lori — optional contributor

Lori may add notes/context when assigned, but owner-level decisions remain clearly attributed to Kraig unless a different decision right is explicitly recorded.

## 7. Core application structure

The application has six primary views.

### 7.1 Dashboard

Shows immediately:

- total products;
- reviewed products;
- products waiting on Kraig;
- products waiting on Craig;
- products waiting on provider verification;
- keep / move / merge / hold / retire totals;
- approved / review / globally rejected design totals;
- launch blockers;
- current launch-catalog count.

Primary shortcuts:

- **Review next product**
- **Needs Kraig**
- **Needs Craig**
- **Provider check**
- **Duplicate candidates**
- **Design library**
- **Launch collection**

### 7.2 Product Review

One product at a time, with current state visually separated from proposed state.

Required current-state fields:

- product image;
- product title;
- handle/URL;
- public status;
- current public price/range;
- product type;
- public vendor label;
- current collections/observed placements;
- current design assignment(s), when mapped;
- colors/sizes/options;
- variant count;
- current description;
- public SKU information;
- audit flags;
- provider verification status;
- sample status;
- open-order dependency status, if known.

Decision controls:

**Audience / collection placement**
- Buck
- Doe
- Yearling
- Fawn
- Shared / Family
- Gear / Accessories
- Headwear
- The Rut apparel
- Does not belong in these collections
- Needs investigation

Multiple intentional placements are allowed only through an explicit **Cross-list intentionally** decision.

**Product disposition**
- Keep as-is
- Keep but repair
- Move / recategorize
- Cross-list intentionally
- Merge candidate
- Hold from launch
- Retire
- Needs investigation

**Title**
- Approved as-is
- Rewrite
- Craig proposes rewrite

**Description**
- Approved as-is
- Rewrite
- Too generic
- Technically incorrect
- Missing sizing/fit
- Missing care
- Missing delivery/printed-to-order information
- Contains broken/irrelevant links
- Needs provider fact verification

**Design**
- Keep current approved design
- Replace with D01
- Replace with D02
- Replace with D03
- Replace with D04
- Replace with D05
- No design / blank exception
- Needs design review
- Reject this design globally

Each save records decision maker, timestamp, optional reason, and resulting action owner.

### 7.3 Design Library

Every distinct artwork family or design treatment discovered in the audit can be represented as a design record.

Fields:

- design ID;
- preview;
- artwork/family name;
- master or variant relationship;
- current product count;
- current placement/image count when known;
- current storefront locations;
- source/provenance note;
- reproduction/production notes;
- status.

Statuses:

- Approved master
- Approved variant
- Review
- Hold
- Rejected globally

Approved launch masters use D01–D05.

A global rejection requires a confirmation step that shows the blast radius before saving:

- products affected;
- variants affected where count is known;
- images/placements affected where count is known;
- launch products affected;
- products needing replacement art;
- products that could instead be retired;
- mixed-design products requiring manual review.

Global rejection does not delete anything. It creates blocking actions.

### 7.4 Duplicate / Merge Review

The app groups products using **signals**, not automatic conclusions.

Signals may include:

- same or near-identical title;
- shared SKU values;
- same garment/product type;
- same vendor/provider label;
- overlapping option sets;
- similar imagery;
- same design mapping;
- audit-created duplicate group.

Side-by-side comparison shows:

- image;
- title/handle;
- product type;
- vendor;
- mapped design;
- price;
- colors/sizes;
- variant count;
- shared SKU count;
- collection placement;
- audit notes;
- provider verification state.

Allowed decisions:

- Keep both
- Merge after provider verification
- Keep A / retire B
- Keep B / retire A
- Hold both
- Not duplicates
- Needs provider verification

No merge is considered executable until provider/variant routing is verified.

### 7.5 Action Queue

Decisions generate explicit actions rather than silent state changes.

Action classes:

- Craig — catalog edit
- Craig — copy rewrite
- Craig — design replacement
- Craig — collection correction
- Craig — site/navigation repair
- Provider/admin verification
- Sample required
- Kraig decision required
- Hold/retire execution
- Redirect/update links

Each action contains:

- action ID;
- product/design reference;
- current state;
- approved target state;
- reason;
- owner;
- blocker/dependency;
- priority;
- execution status;
- completion evidence/note.

Execution statuses:

- Not started
- Ready
- In progress
- Blocked
- Executed
- Verified

### 7.6 Launch Collection

A filtered view of only products currently approved for the first release.

A product cannot be marked **Launch Ready** unless required gates are satisfied or explicitly waived by the correct owner.

Default gates:

- owner disposition approved;
- intended collection approved;
- design approved;
- title/description approved;
- no unresolved P1 storefront defect tied to that product;
- provider route verified;
- pricing/economics verified;
- required sample evidence passed;
- live variant behavior verified;
- shipping/market eligibility verified.

## 8. Automatic flags

The app imports audit findings and also computes deterministic review flags where the source data supports them.

Initial flag types:

- Collection mismatch
- Audience/fit naming conflict
- Duplicate-title candidate
- Shared-SKU candidate
- Design not approved
- Globally rejected design used
- Broken description link
- Missing sizing/fit information
- Missing care information
- Missing production/delivery information
- Provider route unverified
- Sample unverified
- Launch blocker

Known examples from the audit that must appear as review cases include:

- baby onesies appearing in Yearling as well as Fawn;
- Fawn and Yearling leading with a duffle bag rather than a clear age-appropriate first row;
- products titled Men's Rash Guard and Men's Windbreaker appearing in Doe;
- repeated-title groups that are not automatically safe to merge;
- the two Ideal Crew listings sharing 56 SKU values;
- artwork placements that do not yet map to one of the five approved masters;
- malformed description links;
- products or routes that remain unverified from public data.

## 9. Data model

### ProductRecord

- `product_id`
- `shopify_product_id`
- `title_current`
- `handle`
- `public_url`
- `status_current`
- `product_type`
- `vendor_public`
- `price_min`
- `price_max`
- `variant_count`
- `options`
- `skus`
- `images`
- `description_current`
- `collections_observed`
- `design_ids_current`
- `audit_flags`
- `duplicate_group_ids`
- `provider_verification`
- `sample_status`
- `open_order_dependency`
- `decision_state`
- `execution_state`

### ProductDecision

- `product_id`
- `decision_id`
- `decision_maker`
- `decided_at`
- `disposition`
- `target_collections`
- `cross_list_intentional`
- `title_decision`
- `title_proposed`
- `description_decisions`
- `description_proposed`
- `design_decision`
- `target_design_id`
- `notes`

### DesignRecord

- `design_id`
- `name`
- `family`
- `parent_design_id`
- `preview_asset`
- `source_note`
- `status`
- `products_using`
- `placement_count`
- `production_notes`
- `decided_by`
- `decided_at`
- `decision_notes`

### ActionItem

- `action_id`
- `entity_type`
- `entity_id`
- `action_type`
- `current_state`
- `target_state`
- `reason`
- `owner`
- `priority`
- `dependencies`
- `status`
- `evidence`

### AuditFlag

- `flag_id`
- `product_id`
- `flag_type`
- `severity`
- `source_issue_id`
- `message`
- `resolution_status`

## 10. Persistence and exports

Version 1 is offline-first.

Primary persistence:

- browser local storage / IndexedDB for active decisions;
- explicit JSON export for backup and transfer.

Required exports:

1. `Whitetail_Product_Decisions.json`
2. `Whitetail_Action_Queue.csv`
3. `Whitetail_Design_Decisions.json`
4. `Whitetail_Launch_Catalog.csv`
5. `Whitetail_Unresolved_Verification.csv`

The app must also support importing its own previously exported decision JSON so a review session can resume on another device/browser.

## 11. Safety and change-control rules

1. **Shopify is read-only by default for this project. No Shopify write, publish, delete, archive, collection edit, price change, inventory change, theme change, or other live-store mutation may occur unless Craig explicitly asks to push that specific change. Version 1 contains no Shopify write path at all.**
2. Public vendor label never equals verified provider mapping.
3. Same title never equals confirmed duplicate.
4. Shared SKU is a review signal, not automatic merge permission.
5. Global design rejection creates actions; it never deletes or edits products automatically.
6. Products tied to open orders cannot be retired operationally until that dependency is resolved.
7. Product decisions and execution status are separate. A decision marked `Retire` is not considered executed until Craig marks the corresponding action verified.
8. Every owner decision is attributable and timestamped.
9. Existing audit facts are visually distinguished from new owner decisions and Craig proposals.
10. Unknown values remain visibly unknown rather than being guessed.

## 12. User experience principles

- Phone and tablet friendly; Kraig should be able to review products without a desktop.
- One primary decision at a time; avoid spreadsheet-like overload in the default review flow.
- Always show the current live state before the proposed state.
- Use large product imagery and plain language.
- Make risky/global actions visually distinct and require confirmation.
- Preserve progress automatically.
- Allow "skip / come back later" without losing place.
- Keep filters powerful but secondary to the guided review flow.

## 13. Initial review order

Do not force Kraig to review all 125 current products in arbitrary catalog order.

Recommended order:

1. Products with P1 audit flags.
2. Collection mismatch cases (Yearling/Fawn/Doe issues).
3. Globally repeated or questionable designs.
4. Duplicate/SKU groups.
5. Proposed first-launch assortment.
6. Remaining published products.

This creates useful decisions early and reduces the amount of work Craig performs on products that may be held or retired.

## 14. Relationship to the launch plan

Whitetail Product Control becomes the working bridge between **completed audit** and **catalog execution**.

Revised catalog workstream:

1. October 1 baseline audit — complete.
2. October 6 read-only live Shopify inventory refresh — complete.
3. Build Product Control MVP.
4. Import the 125-product live baseline, historical audit findings, and live-vs-audit differences.
5. Kraig reviews product and design decisions.
6. Export approved change manifest/action queue.
7. Craig performs controlled catalog repairs locally or stages them for later execution.
8. Provider/admin verifies mappings and private fulfillment facts.
9. Samples/economics validate launch candidates.
10. Launch Collection reaches readiness gates.
11. Soft launch order testing.
12. Public release.

Any later live-store execution remains a separate explicit push step outside Product Control.

The formal launch plan remains the strategic document; this app becomes the catalog decision/control system beneath it.

## 15. Future Phase 2

Only after Version 1 proves useful:

- repeat the read-only Shopify refresh process;
- compare current Shopify state against the prior saved snapshot;
- detect newly added, removed, or changed products/descriptions/collections;
- optionally read through a dedicated Shopify Admin API integration with owner-approved credentials;
- stage proposed Shopify mutations;
- require a separate execution approval before any write-back;
- preserve a rollback/change manifest.

Direct write-back is not part of Version 1.

## 16. Acceptance scenarios

### Scenario A — Baby onesie in Yearling

The product displays current placement in Yearling/Fawn, an automatic collection-mismatch flag, and relevant product facts. Kraig selects `Fawn` and `Move / recategorize`. The app generates a Craig action without touching Shopify.

### Scenario B — Men's product in Doe

The product displays Doe placement and the naming/fit conflict. Kraig can move it, cross-list it intentionally, or request verification of actual fit.

### Scenario C — Global design rejection

Kraig opens a design, selects `Rejected globally`, sees the impact summary, confirms, and every affected product receives a design blocker/action. Nothing is deleted.

### Scenario D — Ideal Crew duplicate group

Both listings appear side-by-side with the 56 shared-SKU signal. The merge option is available but remains blocked until provider mapping is verified.

### Scenario E — Resume review

Kraig reviews 20 products, exports decisions, later imports the decision file on another device, and resumes at product 21 with all prior decisions intact.

### Scenario F — Launch readiness

A product marked for launch but lacking provider verification or required sample evidence is visibly `Not Ready`, with the missing gates listed.

## 17. First implementation boundary

The first shippable build should contain:

- dashboard;
- product review flow;
- audit flags;
- decision persistence;
- design library/global reject;
- duplicate review;
- action queue generation;
- JSON/CSV export and JSON re-import;
- launch readiness view.

Everything else waits until this workflow is proven useful.
