# Whitetail Product Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an installable, offline-first Whitetail Product Control PWA that loads the fresh 125-product Shopify baseline, carries forward October 1 audit evidence, lets Kraig make structured product/design decisions locally, and exports Craig's exact change queue without any live-store write path.

**Architecture:** A static Vite/vanilla-JavaScript PWA reads normalized local JSON snapshots and stores all review decisions in IndexedDB. Pure domain modules compute flags, duplicate signals, global-design blast radius, actions, and launch readiness; UI views consume those modules without embedding business rules. Shopify is only an extraction source used to produce baseline JSON outside the runtime app; the app has no Shopify credentials, Admin API client, mutation code, publish button, or write-capable connector.

**Tech Stack:** Vite, vanilla ES modules, HTML/CSS, native IndexedDB, Service Worker/PWA manifest, Vitest for unit tests, Playwright for mobile/offline smoke tests.

**Spec:** `docs/superpowers/specs/2026-10-06-whitetail-product-control-design.md`

## Global Constraints

- Shopify is read-only by default for this project. The V1 codebase contains **zero Shopify mutation/write paths**.
- Current source-of-truth snapshot: October 6, 2026; 125 active products; 1,722 variants; 8 collections.
- Historical evidence snapshot: October 1, 2026 audit; 108 products; 1,265 variants; 46 observations/decisions.
- Current-vs-audit delta already verified: 18 current handles absent from the October 1 audit; 1 October 1 handle (`cotton-blend-cap`) absent from the current store; 28 current products updated on/after October 1.
- Current vendor-label counts: Apliiq 31; WHITETAIL SYNDICATE 54; Yoycol 40. Vendor labels remain public metadata, not verified fulfillment routes.
- Current collection counts: Buck 44; Doe 33; Yearling 10; Fawn 7; Hats & Beanies 24; Gear & Accessories 16; Home page 1; Rutline 0.
- Kraig's owner decisions and Craig's execution state are separate records.
- Same title is only a duplicate signal. Shared SKU is only a duplicate/provider-verification signal.
- A globally rejected design creates blockers/actions only; it never alters a product outside the local app.
- Unknown private provider, sample, margin, and open-order facts stay visibly `unknown` until verified.
- Decision imports must never replace the bundled source baseline; they overlay local decisions only.
- Required exports retain these exact filenames: `Whitetail_Product_Decisions.json`, `Whitetail_Action_Queue.csv`, `Whitetail_Design_Decisions.json`, `Whitetail_Launch_Catalog.csv`, `Whitetail_Unresolved_Verification.csv`.
- Phone/tablet use is a first-class requirement. Primary review must remain usable at 360 px CSS width.

## Review Focus

1. **Catalog refresh drift:** a later snapshot can add/remove/change products; stable Shopify GID/handle matching must preserve decisions only where identity is unambiguous. Test in Task 2.
2. **Global design rejection blast radius:** mixed-design and unmapped products must become manual review blockers instead of being silently assigned a replacement. Test in Task 6.
3. **Duplicate false positives:** same titles or shared SKUs must never generate an executable merge automatically. Test in Task 4.
4. **Imported decision-file corruption/schema drift:** invalid, foreign-store, or newer-schema imports must be rejected without damaging existing IndexedDB decisions. Test in Task 3 and Task 8.
5. **Offline/storage failure:** the app must load the bundled catalog offline after first load and must give a visible recoverable error if persistence cannot initialize. Test in Task 9.

---

## File Structure

- `package.json` — Vite/Vitest/Playwright scripts and dependency versions.
- `vite.config.js` — static PWA build configuration and `/product-control/` base-safe asset handling.
- `index.html` — application shell only.
- `public/manifest.webmanifest` — install metadata.
- `public/sw.js` — cache app shell plus normalized baseline JSON; no network write behavior.
- `src/app.js` — application boot and top-level view routing.
- `src/styles.css` — Whitetail-specific responsive visual system.
- `src/config.js` — schema version, snapshot metadata, export filenames, review-status constants.
- `src/data/load-baseline.js` — immutable normalized snapshot loader.
- `src/data/validate-baseline.js` — validates bundled JSON counts, IDs, and required fields.
- `src/state/db.js` — IndexedDB wrapper and migrations.
- `src/state/repository.js` — read/write interface for local decisions, notes, and execution states only.
- `src/domain/flags.js` — deterministic audit/live-data flags.
- `src/domain/duplicates.js` — duplicate-signal grouping without merge authorization.
- `src/domain/design-impact.js` — global rejection blast-radius computation.
- `src/domain/actions.js` — decision-to-action generation.
- `src/domain/readiness.js` — launch-readiness gates and missing evidence.
- `src/domain/review-order.js` — priority order for guided Kraig review.
- `src/export/exporters.js` — required JSON/CSV exports.
- `src/export/import-decisions.js` — safe decision JSON re-import/merge.
- `src/views/dashboard.js` — summary counts and review shortcuts.
- `src/views/product-review.js` — guided current-vs-proposed review screen.
- `src/views/design-library.js` — D01–D05 and discovered design decisions.
- `src/views/duplicate-review.js` — side-by-side candidate review.
- `src/views/action-queue.js` — Craig/provider/sample/owner action queue.
- `src/views/launch-collection.js` — launch candidates and gate failures.
- `src/components/` — reusable product card, status chip, flag list, decision controls, confirmation dialog, filters.
- `data/raw/shopify-live-2026-10-06.json` — read-only Shopify extraction artifact.
- `data/raw/october-1-audit-reference.json` — parsed audit facts needed by the app; no base64 page images.
- `data/normalized/products.json` — one current `ProductRecord` per live Shopify product.
- `data/normalized/designs.json` — initial design records/mappings, including unknown/review states.
- `data/normalized/audit-flags.json` — normalized audit and deterministic live flags.
- `data/normalized/snapshot-meta.json` — counts, collection totals, source timestamps, and diff summary.
- `scripts/normalize-baseline.mjs` — deterministic raw-to-normalized build.
- `tests/data/normalize-baseline.test.js`
- `tests/state/repository.test.js`
- `tests/domain/flags.test.js`
- `tests/domain/duplicates.test.js`
- `tests/domain/design-impact.test.js`
- `tests/domain/actions.test.js`
- `tests/domain/readiness.test.js`
- `tests/export/exporters.test.js`
- `tests/export/import-decisions.test.js`
- `tests/e2e/product-review.spec.js`
- `tests/e2e/offline.spec.js`
- `README.md` — how to run, build, export, restore, and refresh the read-only baseline.

---

### Task 1: Capture and Normalize the October 6 Live Baseline

**Files:**
- Create: `data/raw/shopify-live-2026-10-06.json`
- Create: `data/raw/october-1-audit-reference.json`
- Create: `scripts/normalize-baseline.mjs`
- Create: `data/normalized/products.json`
- Create: `data/normalized/designs.json`
- Create: `data/normalized/audit-flags.json`
- Create: `data/normalized/snapshot-meta.json`
- Test: `tests/data/normalize-baseline.test.js`

**Interfaces:**
- Consumes: Shopify read-only product/collection extraction and `/mnt/data/Whitetail_Syndicate_Current_Site_Audit-1.html`.
- Produces: `normalizeBaseline({ liveProducts, liveCollections, audit }) -> { products, designs, flags, meta }` and immutable normalized JSON files used by every later task.

- [ ] **Step 1: Finish the read-only Shopify extraction into `data/raw/shopify-live-2026-10-06.json`.**

Capture all 125 current products with Shopify GID, title, handle, status, vendor, product type, current description, option names/values, variant count, public SKU data when available, current price range, representative image URLs, updated timestamp, and current collection memberships. Include the 8 collection records and collection/product relationships. Use only Shopify read tools/queries.

- [ ] **Step 2: Parse the October 1 audit into `data/raw/october-1-audit-reference.json`.**

Keep historical product IDs/handles, audit issue IDs/priorities/messages, duplicate groups, the 56-shared-SKU Ideal Crew evidence, broken-link flags, design observations, and collection-placement findings. Exclude embedded base64 screenshots from the normalized app data.

- [ ] **Step 3: Write the failing normalization tests.**

Assert:
```js
expect(result.meta.liveProductCount).toBe(125)
expect(result.meta.liveVariantCount).toBe(1722)
expect(result.meta.collectionCount).toBe(8)
expect(result.meta.addedSinceAudit).toHaveLength(18)
expect(result.meta.removedSinceAudit).toEqual(['cotton-blend-cap'])
expect(result.products).toHaveLength(125)
expect(new Set(result.products.map(p => p.shopify_product_id)).size).toBe(125)
```

Also assert current Yearling membership contains the three `baby-short-sleeve-one-piece*` handles and current Doe membership contains `mens-rash-guard`, `men-s-windbreaker`, and `men-s-windbreaker-1`.

- [ ] **Step 4: Run the test and verify it fails before the normalizer exists.**

Run: `npm test -- tests/data/normalize-baseline.test.js`
Expected: FAIL because `normalizeBaseline`/normalized files do not yet exist.

- [ ] **Step 5: Implement `normalizeBaseline(input) -> NormalizedBaseline` in `scripts/normalize-baseline.mjs`.**

Identity priority: Shopify product GID, then handle only for historical matching. Preserve live values as `*_current`; preserve audit evidence separately. Never turn vendor labels into provider verification.

- [ ] **Step 6: Generate the normalized JSON files and run the tests.**

Run: `node scripts/normalize-baseline.mjs && npm test -- tests/data/normalize-baseline.test.js`
Expected: PASS and exact count checks above.

- [ ] **Step 7: Commit.**

```bash
git add data scripts tests/data
git commit -m "data: capture current Whitetail catalog baseline"
```

### Task 2: Application Shell, Baseline Loader, and Refresh-Diff Model

**Files:**
- Create: `package.json`
- Create: `vite.config.js`
- Create: `index.html`
- Create: `src/app.js`
- Create: `src/config.js`
- Create: `src/data/load-baseline.js`
- Create: `src/data/validate-baseline.js`
- Create: `src/styles.css`
- Create: `public/manifest.webmanifest`
- Test: `tests/data/normalize-baseline.test.js`

**Interfaces:**
- Consumes: Task 1 normalized JSON.
- Produces: `loadBaseline() -> Promise<Baseline>`; `validateBaseline(data) -> ValidationResult`; `diffSnapshots(oldSnapshot, newSnapshot) -> SnapshotDiff`.

- [ ] **Step 1: Write tests for baseline validation and refresh drift.**

Assert missing Shopify GID is invalid; duplicate GIDs are invalid; a future snapshot with one new product and one removed product reports those exact identities; a changed handle with the same Shopify GID remains the same product.

- [ ] **Step 2: Run tests and verify failure.**

Run: `npm test -- tests/data/normalize-baseline.test.js`
Expected: FAIL on missing loader/validator/diff functions.

- [ ] **Step 3: Implement the Vite shell, config constants, loader, validator, and snapshot diff.**

Set `SNAPSHOT_SCHEMA_VERSION = 1`; expose the October 6 capture metadata from `snapshot-meta.json`; keep all baseline objects frozen/read-only after load.

- [ ] **Step 4: Run tests and development build.**

Run: `npm test -- tests/data/normalize-baseline.test.js && npm run build`
Expected: PASS; Vite build completes without warnings about unresolved baseline assets.

- [ ] **Step 5: Commit.**

```bash
git add package.json vite.config.js index.html src public tests/data
git commit -m "feat: add Product Control app shell and baseline loader"
```

### Task 3: Local Decision Persistence and Safe Restore

**Files:**
- Create: `src/state/db.js`
- Create: `src/state/repository.js`
- Create: `tests/state/repository.test.js`

**Interfaces:**
- Consumes: immutable product/design IDs from Task 2.
- Produces: `openProductControlDb()`, `saveProductDecision(decision)`, `getProductDecision(productId)`, `listProductDecisions()`, `saveDesignDecision(decision)`, `saveExecutionState(item)`, `exportDecisionState()`.

- [ ] **Step 1: Write failing persistence tests.**

Test product decision save/read, overwrite creates updated timestamp but preserves decision ID history metadata, skip/later state, design decision storage, and execution-state storage.

- [ ] **Step 2: Add corrupted/newer-schema restore tests.**

Assert invalid JSON, wrong `store_domain`, and `schema_version > 1` return a validation error and leave existing stored decisions unchanged.

- [ ] **Step 3: Run tests and verify failure.**

Run: `npm test -- tests/state/repository.test.js`
Expected: FAIL because repository is not implemented.

- [ ] **Step 4: Implement IndexedDB schema `whitetail-product-control`, version 1.**

Object stores: `product_decisions`, `design_decisions`, `execution_states`, `app_meta`. Baseline catalog data is never written back into these stores as editable records.

- [ ] **Step 5: Run tests.**

Run: `npm test -- tests/state/repository.test.js`
Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add src/state tests/state
git commit -m "feat: persist local product decisions safely"
```

### Task 4: Deterministic Flags, Duplicate Signals, and Review Order

**Files:**
- Create: `src/domain/flags.js`
- Create: `src/domain/duplicates.js`
- Create: `src/domain/review-order.js`
- Create: `tests/domain/flags.test.js`
- Create: `tests/domain/duplicates.test.js`

**Interfaces:**
- Produces: `computeFlags(product, context) -> AuditFlag[]`; `buildDuplicateGroups(products, auditEvidence) -> DuplicateGroup[]`; `rankForReview(product, flags, launchSelection) -> number`.

- [ ] **Step 1: Write collection-mismatch tests using current live memberships.**

Assert Yearling baby one-pieces receive `collection_mismatch`; Doe men's-titled items receive `audience_fit_conflict`; Rutline has no purchasable scent products and does not falsely create product records.

- [ ] **Step 2: Write duplicate-signal tests.**

Assert repeated titles create candidates; the historical Ideal Crew 56-shared-SKU evidence creates a high-priority candidate; neither signal sets a merge decision or executable action.

- [ ] **Step 3: Write review-order tests.**

P1 products rank before collection mismatches; collection mismatches before generic duplicates; proposed launch products before remaining unflagged products.

- [ ] **Step 4: Run tests and verify failure.**

Run: `npm test -- tests/domain/flags.test.js tests/domain/duplicates.test.js`
Expected: FAIL.

- [ ] **Step 5: Implement flags, duplicate groups, and ranking as pure functions.**

Do not infer age/fit solely from arbitrary keywords when an explicit audit/live membership signal exists; label heuristic signals separately from audited facts.

- [ ] **Step 6: Run tests.**

Expected: PASS.

- [ ] **Step 7: Commit.**

```bash
git add src/domain tests/domain
git commit -m "feat: compute catalog review flags and duplicate signals"
```

### Task 5: Dashboard and Guided Product Review

**Files:**
- Create: `src/views/dashboard.js`
- Create: `src/views/product-review.js`
- Create: `src/components/product-card.js`
- Create: `src/components/status-chip.js`
- Create: `src/components/flag-list.js`
- Create: `src/components/decision-controls.js`
- Modify: `src/app.js`
- Modify: `src/styles.css`
- Test: `tests/e2e/product-review.spec.js`

**Interfaces:**
- Consumes: baseline, repository, flags, review order.
- Produces: guided product review and local `ProductDecision` records.

- [ ] **Step 1: Write the failing end-to-end product-review test.**

At a 390×844 viewport: open dashboard → choose `Needs Kraig` → open a baby one-piece → verify current title/image/price/vendor/options/Yearling+Fawn placement/flags → choose `Fawn` + `Move / recategorize` → save → reload → decision remains and live/current state remains unchanged.

- [ ] **Step 2: Run Playwright and verify failure.**

Run: `npm run test:e2e -- tests/e2e/product-review.spec.js`
Expected: FAIL because views do not exist.

- [ ] **Step 3: Implement dashboard summary counts and shortcuts.**

Required shortcuts: Review next product, Needs Kraig, Needs Craig, Provider check, Duplicate candidates, Design library, Launch collection.

- [ ] **Step 4: Implement product review with visually separate CURRENT and DECISION panels.**

Render all decision options verbatim from the spec; allow explicit intentional cross-listing; allow `Skip / come back later` without advancing reviewed count.

- [ ] **Step 5: Add responsive Whitetail visual styling.**

Use the brand's dark forest/charcoal/bone editorial language, large product imagery, large tap targets, and clear warning treatment for owner/global decisions. Avoid corporate-dashboard styling.

- [ ] **Step 6: Run E2E and unit tests.**

Expected: PASS.

- [ ] **Step 7: Commit.**

```bash
git add src/views src/components src/app.js src/styles.css tests/e2e
git commit -m "feat: add guided product review workflow"
```

### Task 6: Design Library and Global Rejection

**Files:**
- Create: `src/views/design-library.js`
- Create: `src/domain/design-impact.js`
- Create: `src/components/confirmation-dialog.js`
- Create: `tests/domain/design-impact.test.js`
- Modify: `src/app.js`

**Interfaces:**
- Produces: `computeDesignImpact(designId, products, decisions) -> DesignImpact`; local `DesignDecision` with status `rejected_globally`; product blockers/actions for affected products.

- [ ] **Step 1: Write blast-radius tests.**

Assert impact reports product count, known variant count, launch-product count, replacement candidates, and mixed/unmapped products separately.

- [ ] **Step 2: Write the mixed-design safety test.**

A product with more than one mapped design must become `manual_review_required` after one design is rejected; it must not receive an automatic replacement design.

- [ ] **Step 3: Run tests and verify failure.**

Run: `npm test -- tests/domain/design-impact.test.js`
Expected: FAIL.

- [ ] **Step 4: Implement the Design Library and confirmation flow.**

The confirmation dialog must display blast radius before saving. Saving only changes IndexedDB and locally computed blockers.

- [ ] **Step 5: Run tests.**

Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add src/views/design-library.js src/domain/design-impact.js src/components/confirmation-dialog.js tests/domain/design-impact.test.js
git commit -m "feat: add design decisions and global rejection safeguards"
```

### Task 7: Action Queue and Duplicate/Merge Review

**Files:**
- Create: `src/domain/actions.js`
- Create: `src/views/action-queue.js`
- Create: `src/views/duplicate-review.js`
- Create: `tests/domain/actions.test.js`
- Modify: `src/app.js`

**Interfaces:**
- Produces: `generateActions({ products, productDecisions, designDecisions, flags }) -> ActionItem[]`.

- [ ] **Step 1: Write action-generation tests.**

A Fawn recategorization generates a Craig collection-correction action; a description rewrite generates copy action; a rejected design generates design-replacement blocker/action; unknown provider route generates provider verification action.

- [ ] **Step 2: Write merge safety tests.**

`Merge after provider verification` must generate provider-verification + blocked merge-preparation actions. `Keep A / retire B` must remain an owner decision plus local retire action, never a live product status change.

- [ ] **Step 3: Run tests and verify failure.**

Run: `npm test -- tests/domain/actions.test.js`
Expected: FAIL.

- [ ] **Step 4: Implement action queue and duplicate side-by-side UI.**

Show current state, approved target state, reason, owner, blocker/dependency, priority, execution status, and evidence note.

- [ ] **Step 5: Run tests.**

Expected: PASS.

- [ ] **Step 6: Commit.**

```bash
git add src/domain/actions.js src/views/action-queue.js src/views/duplicate-review.js tests/domain/actions.test.js
git commit -m "feat: turn owner decisions into controlled action queue"
```

### Task 8: Launch Readiness, Exports, and Decision Re-import

**Files:**
- Create: `src/domain/readiness.js`
- Create: `src/views/launch-collection.js`
- Create: `src/export/exporters.js`
- Create: `src/export/import-decisions.js`
- Create: `tests/domain/readiness.test.js`
- Create: `tests/export/exporters.test.js`
- Create: `tests/export/import-decisions.test.js`
- Modify: `src/app.js`

**Interfaces:**
- Produces: `evaluateReadiness(product, context) -> ReadinessResult`; five required file exports; `importDecisionFile(text, currentState) -> ImportResult`.

- [ ] **Step 1: Write readiness-gate tests.**

A launch-selected product with unverified provider route or required sample status is `not_ready` and lists missing gates. A waived gate must include waiver owner, timestamp, and note.

- [ ] **Step 2: Write export tests.**

Assert exact filenames, stable columns/keys, UTF-8 CSV output, current Shopify GID/handle references, and no Shopify credentials/secrets.

- [ ] **Step 3: Write import safety tests.**

Reject wrong store domain, unsupported schema version, invalid JSON, unknown product IDs without explicit unresolved-import reporting, and imports that attempt to alter source baseline fields.

- [ ] **Step 4: Run tests and verify failure.**

Run: `npm test -- tests/domain/readiness.test.js tests/export/exporters.test.js tests/export/import-decisions.test.js`
Expected: FAIL.

- [ ] **Step 5: Implement readiness view, exporters, and safe re-import.**

Imported files may update only decision/design/execution stores after validation.

- [ ] **Step 6: Run tests.**

Expected: PASS.

- [ ] **Step 7: Commit.**

```bash
git add src/domain/readiness.js src/views/launch-collection.js src/export tests/domain/readiness.test.js tests/export
git commit -m "feat: add launch gates and portable decision exports"
```

### Task 9: Offline PWA, Mobile QA, and No-Write Verification

**Files:**
- Create: `public/sw.js`
- Create: `tests/e2e/offline.spec.js`
- Modify: `public/manifest.webmanifest`
- Modify: `src/app.js`
- Modify: `README.md`

**Interfaces:**
- Consumes: complete app.
- Produces: installable/offline-capable build with documented read-only data-refresh process.

- [ ] **Step 1: Write the failing offline smoke test.**

Open once online, enable offline mode, reload, verify dashboard and product review still load the 125-product bundled baseline and stored decisions.

- [ ] **Step 2: Write the persistence-failure test.**

Force IndexedDB initialization failure and verify a visible message explains that review decisions cannot be saved and instructs the user to export/retry rather than pretending the save succeeded.

- [ ] **Step 3: Run E2E and verify failure.**

Run: `npm run test:e2e -- tests/e2e/offline.spec.js`
Expected: FAIL before service worker/error handling exists.

- [ ] **Step 4: Implement service worker and manifest.**

Cache app shell and normalized JSON only. Do not cache or call Shopify Admin endpoints from the runtime app.

- [ ] **Step 5: Run a codebase no-write scan.**

Run:
```bash
rg -n "graphql_mutation|update_product|create_product|bulk_update|set_inventory|add_to_collection|publish|archive|delete.*product|admin/api" src public scripts
```
Expected: no Shopify-write implementation. Any matches must be comments/documentation or removed.

- [ ] **Step 6: Run the complete verification suite.**

Run: `npm test && npm run test:e2e && npm run build`
Expected: all tests PASS; production build succeeds.

- [ ] **Step 7: Manually verify 360 px, 390 px, tablet, and desktop layouts.**

Check: current/proposed distinction; decision controls; duplicate comparison; global-reject confirmation; action queue; exports; launch readiness; offline reload.

- [ ] **Step 8: Update README with the refresh procedure.**

Document: obtain a fresh Shopify snapshot using read-only extraction; run normalizer; review diff; never push changes from Product Control; execute any future live change only through a separately approved process outside this app.

- [ ] **Step 9: Commit.**

```bash
git add public src README.md tests/e2e
git commit -m "feat: ship offline Product Control PWA"
```

---

## Plan Self-Review

- **Spec coverage:** Dashboard, product review, audit flags, design library/global rejection, duplicate review, action queue, launch readiness, persistence, JSON/CSV export/re-import, mobile/offline behavior, and the hard read-only Shopify boundary all have implementation tasks.
- **Live-baseline coverage:** Task 1 explicitly uses the 125-product/1,722-variant October 6 baseline, eight current collections, 18 additions, one removal, and historical audit evidence.
- **Type consistency:** The stable identity is `shopify_product_id`/Shopify GID across normalization, decisions, actions, readiness, exports, and refresh diffing. `product_id` remains the app's stable entity key derived from that identity.
- **Safety coverage:** No task creates Shopify credentials or writes; Task 9 performs a codebase scan specifically for mutation/write paths.
- **Scope:** V1 stays an internal decision-control PWA. Shopify write-back, CRM/outreach tracking, retail checklist execution, order/customer management, and provider automation remain outside this build.
