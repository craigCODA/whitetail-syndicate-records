const flag=(type,priority,message,source='live_rule')=>({type,priority,message,source});
const resolved=v=>v==='verified'||v==='not_applicable';
export function computeFlags(p,{launchSelected=false,currentDesignId='',currentDesignIds=[],rejectedDesignIds=new Set(),providerVerification, sampleStatus}={}){
 const out=(p.audit_review_flags||[]).map(m=>flag('audit_evidence','P2',m,'october_1_audit'));
 const cs=p.collections_current||[]; const h=p.handle_current||''; const t=p.title_current||'';
 const designIds=currentDesignIds.length?currentDesignIds:(currentDesignId?[currentDesignId]:(p.design_ids_current||p.design_ids||[]));
 const providerState=providerVerification||p.provider_verification;
 const sampleState=sampleStatus||p.sample_status;
 if(cs.includes('The Yearling Collection')&&/^baby-short-sleeve-one-piece/.test(h)) out.push(flag('collection_mismatch','P2','Infant one-piece is currently listed in Yearling.','audited_live_membership'));
 if(cs.includes('The Doe Collection')&&(/Men['’]?s/i.test(t)||h==='mens-rash-guard'||h.startsWith('men-s-windbreaker'))) out.push(flag('audience_fit_conflict','P2','Men-titled product is currently listed in Doe.','audited_live_membership'));
 if(!p.product_type_current) out.push(flag('taxonomy_missing','P2','Public product type is blank.'));
 if(p.source_detail==='october_6_live'&&cs.length===0) out.push(flag('uncategorized_new_product','P2','New live product is not in a named launch collection.'));
 if(!resolved(providerState)) out.push(flag('provider_unverified','P2','Actual fulfillment/provider route still requires private verification.'));
 const rejectedHere=designIds.filter(id=>rejectedDesignIds.has(id));
 if(rejectedHere.length) out.push(flag('global_design_rejected','P1',`${rejectedHere.join(', ')} ${rejectedHere.length>1?'are':'is'} globally rejected in Product Control.`,'local_design_decision'));
 if(rejectedDesignIds.size&&designIds.length===0) out.push(flag('design_mapping_required_after_global_reject','P1','A design has been globally rejected; this unmapped product must be checked before it can clear design review.','local_design_decision'));
 if(launchSelected&&!resolved(sampleState)) out.push(flag('sample_unverified','P1','Launch-selected product has no verified sample status.'));
 return out;
}
