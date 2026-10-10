export function rankForReview(product,flags=[],launchSelected=false){
 let score=1000;
 if(flags.some(f=>f.priority==='P1'))score-=800;
 else if(flags.some(f=>['collection_mismatch','audience_fit_conflict'].includes(f.type)))score-=600;
 else if(flags.some(f=>f.type==='duplicate_candidate'))score-=350;
 if(launchSelected)score-=100;
 return score;
}
export function chooseNextProductId(products,decisions,flagMap){
 const ranked=list=>[...list].sort((a,b)=>rankForReview(a,flagMap.get(a.shopify_product_id)||[],!!decisions.get(a.shopify_product_id)?.launch_selected)-rankForReview(b,flagMap.get(b.shopify_product_id)||[],!!decisions.get(b.shopify_product_id)?.launch_selected));
 const unreviewed=ranked(products.filter(p=>!decisions.get(p.shopify_product_id)?.review_state));
 if(unreviewed.length)return unreviewed[0].shopify_product_id;
 const skipped=ranked(products.filter(p=>decisions.get(p.shopify_product_id)?.review_state==='skip_later'));
 return skipped[0]?.shopify_product_id||products[0]?.shopify_product_id;
}
