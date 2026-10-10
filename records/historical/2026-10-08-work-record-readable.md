# Readable extraction

Source: Whitetail Syndicate work record, September 30 through October 8, 2026

This is extracted text; the original PDF controls page layout and signature fields.

PAGE 1
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  1
CRAIG RAMOS  /  PREPARED FOR KRAIG & LORI
Whitetail Syndicate
Work Completed & Remaining
Store & products  /  Website development  /  Brand outreach & relationships
September 30 through October 8, 2026
This record begins at the agreed $30-per-hour Whitetail work arrangement. Earlier artwork, files, and preparation 
are background only and are not included as new work in this reporting period.
Each work description is immediately followed by an approximate number of hours and the evidence supporting it. 
Items still to do carry separate forward-looking estimates. The work record is not an invoice, an exact time clock, or 
a claim that unapproved changes were applied to the live Shopify store.
Exhibit A. Original storefront captured in the October 1 site audit. This is an audit screenshot, not the revised website.
How to read the evidence
Completed  An artifact, source file, dated audit, sent message, or repository change establishes that the described 
work occurred.
In progress  A work product exists, but owner approval, testing, permissions, or implementation remains 
outstanding.
Estimate  Hours are retrospective, approximate task-effort estimates, not recorded start/stop measurements. Tasks 
are grouped to reduce double-counting. No financial balance or bill is included.
Scope boundary: no website publication, product changes, advertising purchase, filmed documentary, booked call, or 
contributor authorization is inferred merely from a draft, a reply, or a local test.

PAGE 2
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  2
01  Store & products
Work performed
Storefront and catalog audit  |  Sep 30 - Oct 1
Reviewed the existing shopping experience, collection structure, titles, product placement, pricing, repeated 
listings, product artwork, and purchasing friction. The October 1 audit preserved a 108-product/1,265-variant 
snapshot with 46 findings and a corresponding working tracker; it created a decision base rather than modifying 
merchandise.
Approximate time spent: 4.0 hours
Evidence: [S01] October 1 site audit HTML; [S02] October 3 follow-up audit.
Collection placement, duplicates and merchandising review  |  Oct 1 - 3
Investigated repeated titles and cross-category placement. The October 3 audit recorded 113 product entries and 25 
repeated-title groups involving 61 entries; examples included men's items in Doe and a duffle bag under child/youth 
categories. Identical titles were flagged for review, not automatically considered true duplicates.
Approximate time spent: 2.5 hours
Evidence: [S02] October 3 audit, pages 5-7; [S01] catalog register.
Customer path and storefront trust checks  |  Oct 3
Verified that a sample beanie size could reach the cart and checkout, then removed the test item without placing an 
order. Reviewed missing policy information, supplier-style product titles, an empty Rut Line, misleading video 
controls, and the incorrect Our Story navigation.
Approximate time spent: 1.5 hours
Evidence: [S02] audit, pages 1-4 and 7-8; [S01] cart and checkout screenshots.
Exhibit B. Checkout-entry screenshot preserved in the October 1 audit. This proves a sampled checkout entry, not 
payment or fulfillment.

PAGE 3
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  3
Actual store-product reference collection  |  Oct 4 - 5
Collected store-derived product imagery and identifiers as source material for accurate collection scenes. Compared 
artwork in the promotional scenes against real store products to avoid invented garment graphics, incorrect logos, 
and false assortment claims. The reference HTML and product archive were preserved for subsequent corrections.
Approximate time spent: 2.0 hours
Evidence: [S03] Original Store Products HTML; Verified Product Sources ZIP; real-product archive.
Current catalog snapshot and changes since audit  |  Oct 6
Captured and compared an updated read-only Shopify baseline: 125 active products, 1,722 variants, and eight 
collections, with 18 current handles absent from the October 1 audit and one older handle no longer present. 
Source data and a normalization report were saved. These counts are dated snapshots, not permanent live-store 
claims.
Approximate time spent: 1.5 hours
Evidence: [S04] Product Control package, snapshot-meta.json and raw Shopify JSON.
Whitetail Product Control application  |  Oct 6
Built a local/offline product-review workflow with catalog data, product/design decisions, duplicate signals, action 
queues, import/export functions and launch-readiness gates. The archived project contains source files, a built 
distribution, a Windows launch script, and 15 test files. The app has no Shopify write path, so decisions stay local 
until a separately approved implementation.
Approximate time spent: 4.5 hours
Evidence: [S04] Product Control ZIP, README, /src, /dist, /tests and export modules. Test files are present; runtime tests were not 
rerun for this report.
Kraig product-review handoff  |  Oct 7
Prepared a separate single-file, locally usable review interface designed to let Kraig look through products and 
provide keep, repair, move, merge-review or hold decisions. This is a review aid; no completed owner decision list 
or store changes were verified.
Approximate time spent: 2.0 hours
Evidence: [S05] Whitetail_Syndicate_Kraig_Product_Review.html.
Work still to be completed
Owner catalog decisions
Review the proposed initial five design families and determine which product records to keep, move, repair, merge, 
hold, or retire. Record these choices through the review workflow so implementation is traceable.
Estimated effort remaining: 3-5 hours
Depends on: Kraig and Lori approvals; current Shopify catalog export.
Supplier and sample verification
Match selected garments and variants to actual provider IDs, decorated costs, sizes, print placements, production 
timelines and samples. Do not treat the public vendor name as fulfillment proof.
Estimated effort remaining: 4-7 hours
Depends on: Supplier records, sample access, owner selection.

PAGE 4
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  4
Product data and catalog implementation
Turn approved review decisions into actual title, category, variant, image, SKU and collection corrections. Confirm 
redirects/duplicate handling before any product retirement or consolidation.
Estimated effort remaining: 6-10 hours
Depends on: Owner-approved change list and explicit live-store permission.
Commercial readiness and policies
Verify shipping rates, taxes, checkout, exchanges/returns, estimated production times, product help contact and 
accurate size information.
Estimated effort remaining: 4-6 hours
Depends on: Merchant policy decisions, suppliers, safe order-testing scope.
Product Control acceptance
Open the installed app with Kraig, test decisions/import/export with a fresh snapshot, verify mobile/offline 
handling, and agree on its change-approval process.
Estimated effort remaining: 2-4 hours
Depends on: Kraig access and actual acceptance testing.
02  Website development
Work performed
Horizon source recovery and review  |  Sep 30 - Oct 3
Worked from the Shopify Horizon source archive and inspected templates, Liquid sections, configuration, styling, 
and asset boundaries. The work was kept in a separate local copy, preserving the original and avoiding changes to 
the live theme.
Approximate time spent: 2.0 hours
Evidence: [S06] Horizon source ZIP; [S02] local-build audit.
Custom local storefront sections  |  Oct 3
Developed local theme sections and presentation changes for homepage structure, brand copy, Our Story, native 
collection navigation, single newsletter entry, more legible headings, and a Rut Line scents Coming Soon state. The 
source was designed to remove false video-play controls and unverified social links.
Approximate time spent: 4.0 hours
Evidence: [S02] local-build report, pages 1-4; [S06] local Horizon archive.
Static checks and package verification  |  Oct 3
Checked Liquid/JSON structure and JavaScript syntax, reported zero new Theme Check issues and preserved a 
matching original-theme backup. The review expressly left browser-runtime, Shopify-template, mobile interactions, 
checkout, tax and fulfillment tests open.
Approximate time spent: 2.0 hours
Evidence: [S02] audit, page 8; original source backup and ZIP verification.

PAGE 5
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  5
Collection imagery and typography refinement  |  Oct 4 - 5
Revised Buck, Doe, Yearling and Fawn collection presentation and discussed correcting clothing and logos so scenes 
show actual products rather than made-up product designs. Several image revisions remained under review; 
generated imagery by itself does not prove a final retail product exists.
Approximate time spent: 3.0 hours
Evidence: [S03] product source archive; [S07] Horizon preview files; saved artwork examples.
Exhibit C. Working visual concept from the collection-imagery process. Artwork proof only; a product-match check is still 
required.
Local preview and theme packaging  |  Oct 5 - 8
Produced and iterated standalone HTML previews and Horizon theme ZIP packages so the revised storefront could 
be reviewed before publishing. Prepared a local story-facing section and adjusted navigation and copy for the new 
brand/story direction.
Approximate time spent: 2.0 hours
Evidence: [S07] Horizon Preview Updated-4 ZIP, Updated Theme ZIP and local preview HTMLs.
Hats, gear and Rut Line collection tiles  |  Oct 7 - 8
Added Shopify-linked collection tiles for Hats & Beanies and Gear & Accessories, preserved the Rut Line Coming 
Soon treatment, then restored the original Buck/Doe/Yearling/Fawn desktop layout when the added tiles affected its 
styling. The final recorded correction is GitHub commit 96f5f5b.
Approximate time spent: 2.0 hours
Evidence: [S08] GitHub commits 0f57507, 666fb65 and 96f5f5b.
Version control and browser-preview route  |  Oct 7 - 8
Created the dedicated GitHub repository for the local Horizon work and configured a GitHub Pages browser 
preview. At first, the browser showed an older README-like page. Refreshing the page resolved that display issue, 
and the preview worked. The earlier claim that Pages was not working was withdrawn. This is a completed preview 
setup, not a claim that the Horizon changes were published to the live Shopify store.
Approximate time spent: 2.5 hours

PAGE 6
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  6
Evidence: [S08] GitHub commit history and Pages/CNAME changes; final working preview status clarified by Craig on October 8.
Work still to be completed
Finish accurate collection artwork
Finish the remaining Hats & Beanies and Gear & Accessories scenes and verify every prominently depicted product, 
mark, text treatment and collection link against the approved catalog.
Estimated effort remaining: 3-5 hours
Depends on: Final product image sources and visual approval.
Owner walkthrough and revision pass
Show Kraig and Lori the actual local Horizon version, identify what changed from their current storefront, collect 
corrections, and freeze a reviewed candidate.
Estimated effort remaining: 3-5 hours
Depends on: Owners' review and final collection copy/artwork.
Browser, mobile and accessibility acceptance
Test the revised theme in a real Shopify draft environment: mobile/tablet layout, navigation, readable artwork, 
working forms, keyboard focus, images, state changes and speed.
Estimated effort remaining: 3-6 hours
Depends on: Permission to install an unpublished theme copy.
Approved Shopify implementation and launch gate
Only after approval, implement the final theme/template/menu changes in Shopify, confirm rollback, and test 
shipping/payment/provider/customer flows before a public switch.
Estimated effort remaining: 6-10 hours
Depends on: Separate explicit publishing approval and documented commerce readiness.
03  Outreach, brand & relationships
Work performed
Launch positioning and working business plan  |  Sep 30 - Oct 6
Built the launch approach around a recognizable hunting brand with commerce as one part of the operation. 
Prepared formal launch-plan and presentation revisions covering initial apparel, catalog discipline, customer 
experience, storytelling, marketing, dependencies, ownership and the proposed October-January execution 
window.
Approximate time spent: 4.0 hours
Evidence: [S09] formal launch plan; [S10] combined October 8 recommendations packet.
Hunter interview and permission workflow  |  Oct 2 - 6
Developed a live interview questionnaire, story-gathering approach, recording/share preferences and a proposed 
release/permission process. Established that youth stories, photography, audio, location access and contributor 
rights need separate authorization.
Approximate time spent: 1.5 hours
Evidence: Interview packet and permissions drafts; [S09] media/rights sections.

PAGE 7
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  7
Nathan Deville: Wait Till He Turns  |  Oct 6 - 7
Developed the first substantial original hunter story using Nathan's account, his father's involvement, the lease trip, 
the deer encounter and the central instruction, "Wait till he turns." Worked through contradictory timeline details, 
revised prose and produced a branded HTML page with supporting artwork. This is an editorial treatment, not a 
released documentary or cleared publication.
Approximate time spent: 4.0 hours
Evidence: [S11] Wait_Till_He_Turns_branded(1).html; interview/story drafts.
Exhibit D. Media extracted from the October 7 branded story HTML. Evidence of story-page development, not permission 
to publish Nathan's account.
Prospect research and qualification  |  Oct 5 - 8
Identified hunters, nonprofits, guide services, youth and veteran programs, deer-recovery organizations, outdoor 
media, archery groups, conservation contacts, and hunting-related community organizations. Reviewed why each 
organization might have a meaningful story or participant, rather than treating every listing as a generic 
advertising lead.
Approximate time spent: 3.5 hours
Evidence: [S12] outreach records/prospect JSONs and individual Gmail messages.

PAGE 8
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  8
Personalized first-contact outreach  |  Oct 5 - 8
Sent a verified minimum of 99 relevant first-contact emails across these dates (18 on October 5, 46 on October 6, 32 
on October 7, 3 on October 8). Wrote invitations around each recipient's actual hunt, mission, event or community 
work. Additional website form submissions are separate from this email count.
Approximate time spent: 5.0 hours
Evidence: [S12] email folder/archive and Gmail sent messages; dated outreach briefing.
Response review and relationship development  |  Oct 5 - 8
Read, sorted and responded to people willing to talk, offering referrals, asking for sample publications, or requiring 
organizational permission. Examples include Bobby Cole, Lea White, Greg Ray, Pete Eisentrager, Darren Haverstick, 
Shawn Daniel and Mike Cranford. Positive email responses were treated as conversation openings, not signed 
releases or confirmed bookings.
Approximate time spent: 2.0 hours
Evidence: [S12] outreach update October 7; [S13] selected incoming/reply Gmail threads.
Owner-facing outreach brief and documentary recommendation  |  Oct 7 - 8
Prepared a relationship/reply briefing for Kraig and a separate owner-facing launch recommendation. 
Recommended completing the site before directing these contacts to it, and proposed a limited original-
documentary pilot around Every Hunt Has a Story, with permissions, budgets and approval gates.
Approximate time spent: 2.0 hours
Evidence: [S10] recommendations and combined launch packet; [S12] contact brief.
Work still to be completed
Consolidate the contact pipeline
Reconcile sent mail, replies, phone numbers, introductions, bounced contacts, website-form submissions and 
approved follow-up status in one reviewed master record.
Estimated effort remaining: 3-5 hours
Depends on: Current inbox, email export, and owner priorities.
Complete appropriate follow-ups
Respond to people who asked specific questions or offered introductions, define the initial call agenda for each, and 
confirm scheduling when authorized. Do not supply an unapproved website as the finished brand.
Estimated effort remaining: 3-6 hours
Depends on: Recipient preferences, owner direction and approved presentation example.
Finalize story permissions and Nathan's feature
Confirm the accurate timeline with Nathan, obtain story/photo/film releases and location permissions as required, 
and prepare a genuinely approved page for publishing.
Estimated effort remaining: 3-6 hours
Depends on: Nathan's factual review, contributor rights and website approval.
Design a controlled documentary pilot
Prepare the candidate story treatment, locations, storyboards, shot list, contractor/rental options, schedule, releases 
and capped production estimate before any filming spend.
Estimated effort remaining: 5-9 hours

PAGE 9
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  9
Depends on: Owner approval, participant consent, land access and budget.
Brand introduction and content rollout
Publish approved written stories and photographs, establish verified business social profiles, and measure outreach 
engagement and website visits after the public storefront is approved. This activity is limited to content 
coordination and launch tracking.
Estimated effort remaining: 2-4 hours coordination
Depends on: Published site, cleared written/photo material and approved marketing direction.
Approximate effort by workstream
These figures sum only the activity-level estimates printed directly under the descriptions in this report. They are 
retrospective work-effort estimates, not independently timed hours and not a payment or billing statement.
Workstream Completed (approx.) Remaining (estimated)
Store and products 18.0 hours 19-32 hours
Website development 17.5 hours 15-26 hours
Outreach, brand and 
relationships
22.0 hours 16-30 hours
Combined 57.5 hours 50-88 hours
The discontinued promotional MP4/video-concept task (2.5 estimated hours) is not part of completed work here. 
Documentary pilot planning remains a distinct future workstream; the completed GitHub Pages preview setup and 
retained design iterations are included. The dropped retail rollout had no standalone hours in this report.
Evidence exhibits & source register
The proof below is preserved either as a named dated file produced during the work or as a direct external 
repository/email link. Earlier source documents are historical evidence and may describe plans no longer being 
pursued; this revised work record identifies the current scope. Photos/screenshots are included where helpful, but 
do not establish Shopify publication.
[S01]  Whitetail_Syndicate_Current_Site_Audit-1.html - October 1 audit with embedded screenshots, catalog, findings and 
buying-path review.
[S02]  Whitetail_Syndicate_Site_Audit_and_Local_Build.pdf - October 3 eight-page audit and local-theme test limits.
[S03]  Whitetail_Syndicate_Original_Store_Products.html; Whitetail_Syndicate_Verified_Product_Sources.zip; 
Whitetail_Real_Product_Photo_Archive.zip.
[S04]  Whitetail_Syndicate_Product_Control_2026-10-06.zip - raw and normalized snapshot, README, /src, /dist and /tests.
[S05]  Whitetail_Syndicate_Kraig_Product_Review.html - October 7 offline review artifact.
[S06]  whitetail-syndicate-horizon.zip; Whitetail_Syndicate_Horizon_Theme_Updated.zip - original and revised local code 
archives.
[S07]  Whitetail_Syndicate_Horizon_Preview_Updated-4.zip; Whitetail_Syndicate_Horizon_Theme_Updated(1).zip; local-
preview HTML versions.
[S08]  GitHub: https://github.com/craigCODA/whitetail-syndicate-horizon/commits/main (initial theme, collection tiles, 
layout restoration).
[S09]  Whitetail_Syndicate_Formal_Launch_Plan_2026_Core.pdf and related launch-plan revisions (retained documentary-
pilot recommendation; no promotional MP4 production claim).

PAGE 10
INTERNAL REVIEW  /  SEPT 30 - OCT 8, 2026
WHITETAIL SYNDICATE  |  WORK RECORD  |  10
[S10]  Whitetail_Syndicate_Combined_Launch_Packet_Oct_2026.pdf - October 8 recommendations, gate decisions, status 
and wider launch plan.
[S11]  Wait_Till_He_Turns_branded(1).html - Nathan Deville story presentation and embedded imagery.
[S12]  Whitetail_Outreach_Update_2026-10-07_Late.md; Whitetail_Syndicate_Full_Outreach_Brief_2026-10-07.pdf; 
Whitetail_Outreach_Full_Record_2026-10-07.json; Whitetail_Syndicate_Email_Folder_2026-10-08.zip.
[S13]  Gmail examples: Bobby Cole Oct 5: https://mail.google.com/mail/u/?authuser=mistercraigr%40gmail.com#all/
1a10e15b3c8c066e ; Greg Ray Oct 7 reply: https://mail.google.com/mail/u/?authuser=mistercraigr%40gmail.com#all/
1a1178bebeea5ce3 ; Atterbury request: https://mail.google.com/mail/u/?authuser=mistercraigr%40gmail.com#all/
1a1176d03dd12255.
Openable technical and correspondence proof
GitHub: Horizon theme commit history
Gmail: Original Bobby Cole invitation (Oct 5)
Gmail: Greg Ray response (Oct 7)
Gmail: Atterbury request for publication example (Oct 7)
Gmail: Virginia Rhame follow-up (Oct 8)
Verification note: Evidence supports local source creation and communication activity. Product data are historical 
snapshots; use a fresh read-only Shopify extract before live implementation. Hour estimates were not independently time-
tracked.
