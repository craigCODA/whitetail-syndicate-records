export function canApplyGlobalReject(d){return d?.design_decision!=='reject_global'||Boolean(d?.current_design_id)}
export function normalizeDesignKey(id,label=''){if(id!=='OTHER')return id;const slug=String(label).trim().toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');return slug?`OTHER:${slug}`:'';}
export function computeDesignImpact(designId,products,decisions=[]){
 const affected=products.filter(p=>(p.design_ids||[]).includes(designId));
 const mixed=affected.filter(p=>(p.design_ids||[]).length>1);
 const single=affected.filter(p=>(p.design_ids||[]).length===1);
 const unmapped=products.filter(p=>!(p.design_ids||[]).length);
 return {
  designId,
  productCount:affected.length,
  knownVariantCount:affected.reduce((n,p)=>n+(p.variant_count_current||0),0),
  launchProductCount:affected.filter(p=>p.launch_selected).length,
  affectedProductIds:affected.map(p=>p.shopify_product_id),
  mixedProductIds:mixed.map(p=>p.shopify_product_id),
  unmappedProductIds:unmapped.map(p=>p.shopify_product_id),
  replacementCandidates:single.map(p=>p.shopify_product_id),
  manualReviewRequired:mixed.map(p=>p.shopify_product_id)
 };
}
