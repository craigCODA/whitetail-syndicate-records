import {EXPORT_FILENAMES,STORE_DOMAIN,SNAPSHOT_SCHEMA_VERSION} from '../config.js';
const csvEscape=v=>`"${String(v??'').replaceAll('"','""')}"`;
const csv=(rows,cols)=>[cols.join(','),...rows.map(r=>cols.map(c=>csvEscape(r[c])).join(','))].join('\n');
export function buildExports({products,productDecisions,designDecisions,actions,readiness}){
 const byId=new Map(products.map(p=>[p.shopify_product_id,p]));
 const decisionPayload={store_domain:STORE_DOMAIN,schema_version:SNAPSHOT_SCHEMA_VERSION,exported_at:new Date().toISOString(),product_decisions:productDecisions};
 const actionRows=actions.map(a=>({product_id:a.product_id,handle:a.handle,type:a.type,owner:a.owner,priority:a.priority,status:a.status,target:a.target_value||a.target_audience||'',reason:a.reason||''}));
 const launchRows=(readiness||[]).map(r=>({product_id:r.product_id,handle:byId.get(r.product_id)?.handle_current||'',title:byId.get(r.product_id)?.title_current||'',ready:r.ready?'yes':'no',missing:(r.missing||[]).join('|')}));
 const decisionMap=new Map(productDecisions.map(d=>[d.product_id,d]));
 const resolved=v=>v==='verified'||v==='not_applicable';
 const unresolved=products.map(p=>{const d=decisionMap.get(p.shopify_product_id)||{};return {...p,provider_verification:d.provider_verification||p.provider_verification,sample_status:d.sample_status||p.sample_status}}).filter(p=>!resolved(p.provider_verification)||!resolved(p.sample_status)).map(p=>({product_id:p.shopify_product_id,handle:p.handle_current,title:p.title_current,provider_verification:p.provider_verification,sample_status:p.sample_status}));
 return [
  {filename:EXPORT_FILENAMES.decisions,mime:'application/json',content:JSON.stringify(decisionPayload,null,2)},
  {filename:EXPORT_FILENAMES.actions,mime:'text/csv',content:csv(actionRows,['product_id','handle','type','owner','priority','status','target','reason'])},
  {filename:EXPORT_FILENAMES.designs,mime:'application/json',content:JSON.stringify({store_domain:STORE_DOMAIN,schema_version:SNAPSHOT_SCHEMA_VERSION,design_decisions:designDecisions},null,2)},
  {filename:EXPORT_FILENAMES.launch,mime:'text/csv',content:csv(launchRows,['product_id','handle','title','ready','missing'])},
  {filename:EXPORT_FILENAMES.unresolved,mime:'text/csv',content:csv(unresolved,['product_id','handle','title','provider_verification','sample_status'])}
 ];
}
export function downloadExport(file){const blob=new Blob([file.content],{type:file.mime});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=file.filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),500)}
