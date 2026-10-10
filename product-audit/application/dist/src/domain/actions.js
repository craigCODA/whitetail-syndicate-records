const mk=(type,p,extra={})=>({id:`${type}:${p.shopify_product_id}`,type,product_id:p.shopify_product_id,handle:p.handle_current,title:p.title_current,owner:'Craig',priority:'normal',status:'open',live_store_write:false,...extra});
const verificationResolved=v=>v==='verified'||v==='not_applicable';
export function generateActions({products,productDecisions=[],designDecisions=[],flags=[]}){
 const dm=new Map(productDecisions.map(d=>[d.product_id,d])); const rejected=new Set(designDecisions.filter(d=>d.status==='rejected_globally').map(d=>d.design_id)); const out=[];
 for(const p of products){const d=dm.get(p.shopify_product_id);
  if(d?.disposition==='move'||d?.disposition==='cross_list'){
   const targetValue=d.disposition==='cross_list'?(d.target_collections||[]).join(' | '):(d.audience||'');
   out.push(mk('collection_correction',p,{target_audience:d.audience||null,target_collections:d.target_collections||[],target_value:targetValue,reason:d.disposition==='cross_list'?'Owner intentional cross-list decision':'Owner placement decision'}));
  }
  if(d?.title_decision==='rewrite'||d?.title_decision==='craig_rewrite'||d?.proposed_title)out.push(mk('title_rewrite',p,{reason:'Title decision',target_value:d.proposed_title||''}));
  if((d?.description_flags||[]).some(x=>['rewrite','too_generic','technical','sizing','care','delivery','broken_links'].includes(x))||d?.proposed_description)out.push(mk('copy_rewrite',p,{reason:'Description decision',target_value:d.proposed_description||''}));
  if(d?.design_decision&&['D01','D02','D03','D04','D05','blank','review','reject_global'].includes(d.design_decision))out.push(mk('design_review',p,{reason:d.design_decision==='reject_global'?'Current design rejected globally':'Design decision pending execution',status:d.design_decision==='reject_global'?'blocked':'open'}));
  if(d?.current_design_id&&rejected.has(d.current_design_id))out.push(mk('design_replacement',p,{priority:'high',status:'blocked',reason:`${d.current_design_id} is globally rejected in Product Control`,target_value:'replace/remove rejected design'}));
  const inWorkflow=Boolean(d&&(d.disposition||d.launch_selected));
  if(inWorkflow&&!verificationResolved(d?.provider_verification||p.provider_verification))out.push(mk('provider_verification',p,{owner:'Craig',priority:d?.disposition==='merge_candidate'?'high':'normal',reason:'Private provider route is unknown'}));
  if(d?.disposition==='merge_candidate')out.push(mk('merge_preparation',p,{status:'blocked',priority:'high',reason:'Merge candidate requires provider verification first'}));
  if(d?.disposition==='retire')out.push(mk('retire_candidate',p,{reason:'Owner approved local retirement plan'}));
 }
 return out;
}
