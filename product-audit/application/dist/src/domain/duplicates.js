const key=s=>String(s||'').toLowerCase().replace(/[’']/g,"'").replace(/[^a-z0-9]+/g,' ').trim();
export function buildDuplicateGroups(products,auditEvidence={}){
 const byTitle=new Map();
 for(const p of products){const k=key(p.title_current);if(!k)continue;if(!byTitle.has(k))byTitle.set(k,[]);byTitle.get(k).push(p)}
 const groups=[];let n=1;
 for(const [k,ps] of byTitle)if(ps.length>1)groups.push({id:`title-${n++}`,reason:'repeated_title',priority:'normal',title_key:k,members:ps.map(p=>({product_id:p.shopify_product_id,handle:p.handle_current,title:p.title_current}))});
 for(const ev of auditEvidence.shared_sku_evidence||[]){
  const members=products.filter(p=>(ev.handles||[]).includes(p.handle_current)).map(p=>({product_id:p.shopify_product_id,handle:p.handle_current,title:p.title_current}));
  if(members.length>1)groups.push({id:`sku-${ev.group}`,reason:'shared_sku_evidence',priority:'high',shared_sku_values:ev.shared_sku_values,members});
 }
 return groups;
}
