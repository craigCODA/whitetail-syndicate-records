import test from 'node:test';import assert from 'node:assert/strict';
import {renderProductReview} from '../../src/views/product-review.js';
const p={shopify_product_id:'gid://shopify/Product/1',title_current:'Baby short sleeve one piece',handle_current:'baby-short-sleeve-one-piece',vendor_label_current:'WHITETAIL SYNDICATE',product_type_current:'T-SHIRT',price_min_current:32,price_max_current:32,variant_count_current:18,option_summary_current:'Color: Black ; Size: 3-6m',collections_current:['The Yearling Collection','The Fawn Collection'],description_current:'Baby description',image_urls_current:['https://example.com/baby.jpg'],online_store_url_current:'https://example.com/product'};
test('product review renders current facts separately from decision controls',()=>{
 const html=renderProductReview(p,[{type:'collection_mismatch',priority:'P2',message:'Infant product in Yearling'}],null);
 for(const s of ['CURRENT LIVE LISTING','OWNER DECISION','The Yearling Collection','The Fawn Collection','WHITETAIL SYNDICATE','Move / recategorize','Reject this design globally','Proposed title','Proposed description','Other design / variant label','Provider route verification','Sample status','Public status']) assert.ok(html.includes(s),s);
});
test('product review exposes explicit cross-list targets and owner waiver notes',()=>{const html=renderProductReview(p,[],{});for(const s of ['Cross-list targets','name="target_collections"','Provider waiver note','Sample waiver note'])assert.ok(html.includes(s),s);});
