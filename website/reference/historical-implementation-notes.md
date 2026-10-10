# Whitetail Syndicate Horizon: local review build

**Status:** Local build for review. The original uploaded theme was used as the base. Nothing was uploaded, installed, published, or modified in the connected Shopify store.

## Included in the theme

- **Hunting-story selection:** Nathan Deville's *Wait Till He Turns* has a thumbnail using his real photograph. Story cards can be managed in the Horizon theme editor. The first card links to `/pages/wait-till-he-turns`.
- **Dark story view:** The original branded story copy and imagery are presented as a dedicated story-page template to match the dark website appearance. It has a link back to the stories section.
- **Rut Line signup:** Uses Shopify's `customer` form and tags subscribers `newsletter,rut-line`.
- **General Whitetail signup:** A separate home-page signup uses Shopify's `customer` form and tags subscribers `newsletter,whitetail-community`.
- **Footer signup:** Uses Shopify's customer form with `newsletter,whitetail-community` tags.
- **Contact address:** `info@whitetailsyndicate.com` is shown as a clickable email link.

## Important distinction: database vs. email alerts

The *customer* forms are designed to save email signups as Shopify customer contacts after the theme is installed on Shopify. The `info@whitetailsyndicate.com` address itself is **not** a database, and entering it as a `mailto:` link does not route form submissions there. To receive inbox notifications, set up a workflow in Shopify Flow or an approved Shopify Forms/notification system that emails `info@whitetailsyndicate.com` after a customer is created or tagged. Test both signup sources. Only collect and use email consent in accordance with your marketing policies.

## When you are ready to install, without publishing

1. In **Shopify Admin > Online Store > Themes**, import the theme ZIP as a **new unpublished theme**. Do not publish it over the current site until it has been reviewed.
2. In **Online Store > Pages**, create a page with the handle **`wait-till-he-turns`** (so its URL is `/pages/wait-till-he-turns`). Choose the template named **`wait-till-he-turns`**. Ensure the page is available in the storefront when you want the story card to work. The actual story content comes from the template/section, not the Shopify page text editor.
3. Preview the theme and verify the story thumbnail, story back link, product and collection links, and mobile layout. Check that existing store navigation and product handles are valid.
4. Use test email addresses to verify both Shopify forms truly create or update contacts and apply their expected tags. Verify the consent behavior and any signup confirmation handling.
5. Configure and test the notification workflow to `info@whitetailsyndicate.com`. Without that step, the theme alone **does not send signup notification emails** to that inbox.
6. Publish only after explicit approval. No Shopify action was performed during this local build.

## Local preview details

The separate HTML preview is a standalone visual/interaction review file. It contains the hero, existing sections, hunting-story selection, full story, and signup UI. **The local preview never sends or stores signup form submissions.** Shopify Liquid is not rendered in the standalone HTML; real Shopify forms can be tested only after a safe unpublished-theme import to Shopify.

## Checks run

All 14 intended modifications were checked against the uploaded source ZIP (507 total theme files). The JSON files, section schemas and Liquid delimiters, presence of original story text, CSS parsing, form markup/tag distinctions, JavaScript syntax, and theme references passed static preflight checks. The standalone preview's story open/back behavior and non-submitting forms were checked in desktop and mobile Chromium. These checks are not a substitute for Shopify Theme Check or an on-Shopify test.
