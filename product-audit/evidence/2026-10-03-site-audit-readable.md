# Readable extraction

Source: Whitetail_Syndicate_Site_Audit_and_Local_Build.pdf

This is extracted text; the original PDF controls page layout and signature fields.

PAGE 1
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
1
WHITETAIL SYNDICATE / 03 OCTOBER 2026
Site audit.
Local build review.
The storefront needs a repair pass before a launch push. Customers can buy, but the current presentation
makes promises the site does not fulfill: a story link opens sign-in, video buttons do nothing, and Rutline looks
like an empty store instead of a planned scent launch.
Current scope
Verified result
113 product records
Full catalog metadata inventory; 25 repeated-title groups contain 61 listings. These are review
candidates, not confirmed duplicates.
7 shopping collections +
Rutline
Collection structure and visible samples reviewed; men's items appear in Doe, and the $90
duffle appears in Fawn and Yearling.
Purchase baseline
One beanie, size M, carried correctly to cart and checkout. Test item removed; no order placed.
Local revision
New brand sections and theme source built. Nothing uploaded, saved or published in Shopify.
Test status
Theme Check: zero errors and no new warnings. Browser verification of this revision is pending.
What is ready
The exact supplied primary mark; readable collection links without false lifestyle mockups; factual draft Our
Story copy; a Rut Line scents coming-soon state; plain collection headers; square product-card media; one
general newsletter; and removal of generic social-site links.
What this is not claiming
This is a local revision for review, not a finished storefront launch. All 113 product records were inventoried, but
every product image, size combination and product detail page was not individually inspected. No paid orders,
email signups or contact submissions were made. Shipping rates, tax, payment capture and POD fulfillment
have not been tested.
Evidence is from the current storefront and a read-only view of the hidden Our Story page. Product and collection data remain
unchanged. The original recovered theme was preserved byte-for-byte.


PAGE 2
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
2
01 / VISUAL & CONTENT FAILURES
The first impression breaks trust
Evidence E02 / Home collection artwork. The Doe cap has contradictory brim shapes; tiny simulated logos and shop labels vary across
the scene. Gear/Rutline panels portray a broader assortment than the verified launch scope.
ID / priority
Observed problem
Local correction / remaining work
F01 / High
Malformed lifestyle mockups; tiny baked-in shop
labels and inconsistent simulated artwork.
Home cards replaced by native text links. Product
mockups and supplier print files still require
SKU-level review.
F02 / High
Rutline artwork advertises scents, feed, minerals,
attractants and food plots although the current plan is
scents coming soon.
Remove that panel from the home revision. New
scent-only status and copy; no fabricated packaging
or performance claims.
F03 / High
Main hero is cropped at 365px and the meaningful
logo image has an empty alt attribute.
Supplied primary mark displayed with contain sizing,
explicit dimensions and descriptive alt text. Browser
reflow check pending.
F04 / Medium
Collection headers place headings over a cropped
logo/deer scene.
Replace with plain readable native headings.
F05 / Medium
Two repeated collection headings, generic "Welcome
to our store", and supplier-style product titles weaken
hierarchy.
Native grouped shop navigation and brand
announcement added. Product titles need separate
data edits.


PAGE 3
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
3
02 / FALSE DESTINATIONS
A visitor expects a story or a video
Evidence E21 / This entire "Lifestyle Videos" area is one PNG. The play controls and five video-category tiles are pictures, not video
controls.
ID / priority
Observed problem
Correction / gate
F06 / High
Our Story navigation opens the customer account
sign-in flow.
New theme-owned navigation reaches the
homepage story. Shared Shopify menu has not been
changed.
F07 / High
Actual Our Story page exists but is Hidden with empty
content.
Separate our-story template supplied. Page
visibility, final copy and template assignment remain
future data changes.
F08 / High
No actual video or video iframe exists in the main
homepage content; the picture offers several false
play targets.
Picture removed from the home revision. Replace
with hunter-story copy and a real contact CTA. Add a
player only after real video and permissions exist.
F09 / Medium
Source social settings contain generic Facebook /
Instagram / YouTube / TikTok / X root URLs.
Clear those defaults in local source. Add only
verified brand profile URLs.
F10 / Medium
Contact page is a bare form without an order-help
route, response process or hunt-story intake
guidance.
Existing contact page retained. Define the inbox
owner, story questions, permissions and response
process before promotion.
Draft Our Story direction
Whitetail Syndicate brings together apparel and the people behind the hunt. We are gathering real accounts of
the preparation, long sits, missed chances and moments that stay with a hunter. The copy describes work
under way; it does not invent an origin story, testimonials or a finished documentary library.


PAGE 4
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
4
03 / THE RUT LINE
Coming soon should feel intentional
Evidence E03 / Current /collections/rutline shows 0 items and "No products found" with an irrelevant clear-filters suggestion.
ID / priority
Observed problem
Local behavior
F11 / High
Empty shopping page reads as a failed search or
missing inventory.
"Rut Line scents" / "Coming soon" / brief launch
status. Suppress the product grid, filters, count and
empty-shop message for this handle.
F12 / High
Copy says products are engineered to bring bucks in
range; that capability is unverified.
No performance, ingredient, scent-type or
launch-date claims in the draft.
F13 / Medium
No explicit intent capture for the planned scent
launch.
Native customer interest form in source with
newsletter and rut-line-interest tags, required email,
translated errors and success state. Local preview
never sends data.
Review before use
Approve the product status and email wording. Define who owns the interest list, what updates will be sent,
and how subscribers can unsubscribe. The form has not been submitted or connected to a new automation. Rut
apparel already in the catalog remains separate from this scent-launch state.
The scent page follows the confirmed scope: scents coming soon. It does not rename all Rut apparel or introduce
feed/minerals/food-plot branches.


PAGE 5
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
5
04 / CATALOG & PURCHASE CLARITY
The catalog needs a controlled migration
ID / priority
Verified problem
Work required
F14 / High
113 products; 25 repeated-title groups covering 61
records. Same titles can have different art, suppliers,
costs or prices.
Map blank/garment, design, size, color, supplier,
SKU, variant image and fulfillment linkage before
deciding what becomes a variant.
F15 / High
Doe includes Men's Rash Guard / Men's windbreaker;
Fawn and Yearling include a $90 duffle.
Repair manual membership or collection rules after
establishing the target taxonomy. Theme source
cannot change this data.
F16 / High
POD purchase information is incomplete near the
tested beanie: delivery/production expectations,
returns/exchanges and a usable size guide are
absent.
Confirm supplier-specific facts and merchant policy
decisions; show concise details near purchase
controls.
F17 / Medium
Supplier-style names include All-Over Print / With Box
/ 230GSM; some image alt text exposes product
codes or "Product mockup".
Approve a brand naming convention, meaningful
image descriptions, and SKU-level copy.
F18 / Medium
Unequal card image ratios leave jagged product rows.
Square gallery settings added to home and
collection templates. Check for logo/detail crop in
actual product cards before using.
F19 / Medium
Home featured collection defaults to the broad
all-products assortment; repeated beanie titles
compete without design names.
Choose a reviewed launch collection and distinguish
designs. Current all-products binding is retained
until that collection exists.
F20 / High
Public footer / checkout surface only Privacy policy;
requested shipping, refund and terms search
returned no content.
Draft accurate policies from confirmed fulfillment
and business decisions, then add prominent links.
No invented return terms.
F21 / Low
Two general newsletter areas and generic offers
duplicate the same action.
Remove extra home signup; retain one footer signup
with brand-specific copy. Rut interest form is a
distinct purpose.
F22 /
Investigate
Beanie recommendations remained in loading state
during the sampled journey.
Reproduce on an actual device and inspect Shopify
recommendations. Captured console errors were
browser-extension errors, not proof of a storefront
cause.
All observed prices are current catalog data, not recommended launch prices. Cost, shipping, fees, promotions and margin need a
supplier-based price worksheet before repricing.


PAGE 6
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
6
05 / REPEATED-TITLE REGISTER
25 groups to investigate, not blindly merge
Current title
Listings
Observed base prices / supplier
Youth t-shirt
2
$19.00-$24.00 / WHITETAIL SYNDICATE
Women's relaxed v-neck t-shirt
3
$28.00-$29.00 / WHITETAIL SYNDICATE
DryBlend® T-Shirt
2
$30.00 / WHITETAIL SYNDICATE
Kiss-cut vinyl decals
2
$7.50-$12.00 / WHITETAIL SYNDICATE
Windshield Sunshade | 137cm(53.9")
2
$37.50 / Yoycol
Womens Lightweight Wash Sweatshirt
2
$49.00 / Apliiq
All-Over Print Men's Hoodie With Double-side Print Hood
2
$49.00 / Yoycol
All-Over Print Men's Stand-up Collar Vest
2
$49.00 / Yoycol
Womens Lightweight Wash Hooded Sweatshirt
3
$52.86 / Apliiq
Men's windbreaker
2
$59.00 / WHITETAIL SYNDICATE
All-Over Print Beanie
2
$29.00-$30.00 / WHITETAIL SYNDICATE
Toddler fleece pullover hoodie
2
$34.00 / WHITETAIL SYNDICATE
Kids crew neck sweatshirt
2
$26.00-$30.00 / WHITETAIL SYNDICATE
Baby short sleeve one piece
3
$30.00-$32.00 / WHITETAIL SYNDICATE
Value Fleece Vest
3
$48.00 / Apliiq
skull cap
5
$26.96-$29.00 / Apliiq
Vintage Cotton Twill Cap
2
$27.00 / WHITETAIL SYNDICATE
Lightweight Crop Hoodie
4
$49.00 / Apliiq
Women's garment dye cropped tee
2
$29.00-$30.00 / WHITETAIL SYNDICATE
Women's micro rib racer tank top
2
$35.00 / WHITETAIL SYNDICATE
Camouflage trucker hat
3
$29.00-$30.00 / WHITETAIL SYNDICATE
Posi UV Pro Hoodie
2
$68.34 / Apliiq
Avenue Pullover Hooded Sweatshirt
2
$63.06-$65.00 / Apliiq
Tapered stainless steel tumbler
2
$34.00 / WHITETAIL SYNDICATE
Cotton Blend Cap
3
$34.84 / Apliiq
Full product IDs, handles, variants, options, vendors and observed prices are included in catalog-current.json. Different artwork and
garments may appropriately remain separate products even when current titles match.


PAGE 7
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
7
06 / AUDIT WALKTHROUGH
What was observed, and its current health
Step
Surface
Health
Evidence / result
01
Homepage desktop
Needs repair
Native hero / announcement / category hierarchy; E01-E02.
02
Homepage 365px preview
Needs repair
Logo cropped and baked-in category copy hard to read; E26.
03
Collection imagery
Needs repair
Contradictory cap shapes, simulated logos and false
assortment imagery; E02.
04
Rutline destination
Broken intent
Empty shop instead of scent-launch status; E03.
05
Our Story menu
Wrong destination
Opens customer sign-in; E04.
06
Actual Our Story page
Unavailable
Hidden and blank, observed read-only; E24.
07
Contact page
Incomplete
Form visible; response / story intake workflow undefined. No
submission.
08
Buck collection / 44
Needs cleanup
Repeated skull caps / supplier names; E06 and collection text.
09
Doe collection / 33
Needs cleanup
Men's items and repeated titles; E07 and collection text.
10
Yearling collection / 10
Needs cleanup
Duffle / beanies / baby items mixed with youth; collection text.
11
Fawn collection / 7
Needs cleanup
Duffle and kids / baby assortment mixed; E09.
12
Hats 25 / Gear 16
Needs cleanup
Repeated design/product names; Gear source sample E11.
13
All-products inventory
Needs cleanup
All 113 records captured, 25 repeated-title groups.
14
Sample product / size
Works; info gaps
S changed to M. Missing clear fit / delivery / returns guidance;
E13-E14.
15
Cart / checkout entry
Baseline pass
M and $30 carried through; E17-E19. No address or order
submitted.
16
Lifestyle video block
False controls
One PNG, no player or main-content video links; E21.
17
Footer / policies
Incomplete
Privacy only visible, generic social roots, duplicate signup.
18
Local theme source
Review ready
No new Theme Check diagnostics. Browser runtime acceptance
pending.
The audit spans visual presentation, navigation, catalog structure, content/trust, and the commerce/source boundary. It is not a claim
that every product and page was visited five times. No accessibility-conformance or speed certification is claimed.


PAGE 8
WHITETAIL SYNDICATE / LOCAL REVIEW ONLY
03 Oct 2026 | No Shopify uploads or changes | Review before implementation
8
07 / TESTING & NEXT SEQUENCE
Review first. Then work in measured stages.
Check
Result
Limit
Shopify Theme Check 3.30.1
PASS: 0 errors / 0 new
warnings
Six original warnings remain in existing
header/divider files.
JSON / JSONC / Liquid schemas
PASS
All 76 JSON-family files and 140 embedded schemas
parsed.
JavaScript syntax
PASS
81 existing JS files and local preview script parsed.
Source theme adds no new commerce JS.
Asset fidelity / backup / ZIP
PASS
Three supplied assets copied exactly. Original
source matched its backup. Theme ZIP CRC verified.
New Liquid brand sections
PASS: local rendering
Home / scents / story markup rendered from source
with merchant defaults. Local substitute form is
inert.
Actual revised-page browser behavior
PENDING
Cloud browser blocks local file URLs. Local HTML is
supplied for user review; Shopify rendering requires
later explicit direction.
Checkout / fulfillment / delivery
PENDING for revision
Baseline cart entry passed. No rate, tax, payment,
provider mapping or fulfillment test completed.
1. Review the local revision / Craig
Open the single-file preview. Review Home, Rut Line scents and Our Story at desktop and 365px. Confirm the
exact primary mark, wording, navigation and story contact path. The preview demonstrates brand sections; it
does not replace a Shopify runtime test.
2. Lock artwork and a launch assortment / Craig + owner
Finish the five approved design masters with repeatable WS and antlers, no W&S, named files and revision
control. Select a small reviewed launch collection. Audit every selected SKU against real supplier mockups and
samples.
3. Prepare catalog and policy changes / store admin + POD owner
Use the 113-record register to plan merges, variant mappings, redirects and collection repairs. Confirm
production estimates, delivery regions, support ownership, returns and size charts. Establish price/margin
decisions from actual costs.
4. Run a real draft-store test after explicit authorization
Import an unpublished copy only when directed. Assign approved page templates and resource changes, then
check desktop/mobile reflow, keyboard links, valid/invalid email behavior, product images, variant choice, cart
changes, checkout shipping and provider routing. Order tests require a defined item and budget.
5. Publish and promote after the acceptance gate
Publication waits for separate direction. Keep the live theme rollback, verify production routes after launch,
then connect real story videos, approved profiles and campaign tracking. Keep scent interest separate from
apparel shopping.
Official platform workflow references are in README_LOCAL_REVIEW.md. Findings in this report are direct observations.
