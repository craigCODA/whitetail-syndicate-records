import fs from 'node:fs';

const titleKey=s=>String(s||'').toLowerCase().replace(/[’']/g,"'").replace(/[^a-z0-9]+/g,' ').trim();

export function normalizeBaseline({liveProducts,liveCollections,audit,liveMeta={}}){
  const auditByHandle=new Map((audit.products||[]).map(p=>[p.handle_current,p]));
  const products=liveProducts.map(p=>({
    ...p,
    audit_previous:auditByHandle.get(p.handle_current)||null,
    identity:{shopify_product_id:p.shopify_product_id,handle:p.handle_current},
    current_title_key:titleKey(p.title_current),
    provider_verification:'unknown',sample_status:'unknown',open_order_dependency:'unknown'
  }));
  const liveHandles=new Set(products.map(p=>p.handle_current));
  const auditHandles=new Set((audit.products||[]).map(p=>p.handle_current));
  const added=[...liveHandles].filter(h=>!auditHandles.has(h)).sort();
  const removed=[...auditHandles].filter(h=>!liveHandles.has(h)).sort();
  const meta={
    capturedAt:liveMeta.captured_at||'2026-10-06',
    liveProductCount:products.length,
    liveVariantCount:Number(liveMeta.variant_count||products.reduce((n,p)=>n+(p.variant_count_current||0),0)),
    collectionCount:liveCollections.length,
    addedSinceAudit:added,
    removedSinceAudit:removed,
    vendorCounts:liveMeta.vendors||{},
    sourceMode:'read_only',
    decisionStorage:'local_only'
  };
  const designs=[1,2,3,4,5].map(n=>({id:`D0${n}`,name:`Master Design D0${n}`,status:'review',mapped_product_ids:[]}));
  const flags=[];
  for(const p of products){
    for(const msg of p.audit_review_flags||[]) flags.push({product_id:p.shopify_product_id,handle:p.handle_current,source:'october_1_audit',type:'audit_evidence',priority:'P2',message:msg});
  }
  return {products,designs,flags,meta};
}

if(import.meta.url===`file://${process.argv[1]}`){
  const live=JSON.parse(fs.readFileSync('data/raw/shopify-live-2026-10-06.json','utf8'));
  const audit=JSON.parse(fs.readFileSync('data/raw/october-1-audit-reference.json','utf8'));
  const out=normalizeBaseline({liveProducts:live.products,liveCollections:live.collections,audit,liveMeta:live});
  fs.mkdirSync('data/normalized',{recursive:true});
  fs.writeFileSync('data/normalized/products.json',JSON.stringify(out.products,null,2));
  fs.writeFileSync('data/normalized/designs.json',JSON.stringify(out.designs,null,2));
  fs.writeFileSync('data/normalized/audit-flags.json',JSON.stringify(out.flags,null,2));
  fs.writeFileSync('data/normalized/snapshot-meta.json',JSON.stringify(out.meta,null,2));
}
