import {canApplyGlobalReject,computeDesignImpact} from './design-impact.js';

const designIdsFor=(product,decision)=>{
 if(Array.isArray(decision?.current_design_ids)&&decision.current_design_ids.length)return decision.current_design_ids;
 if(decision?.current_design_id)return [decision.current_design_id];
 return product.design_ids_current||product.design_ids||[];
};

export async function commitProductDecision({decision,repo,products,currentDecisions=[],confirmGlobalReject}){
 if(!canApplyGlobalReject(decision))return {ok:false,error:'design_identity_required'};
 let impact=null;
 if(decision.design_decision==='reject_global'&&decision.current_design_id){
  const pending=new Map(currentDecisions.map(d=>[d.product_id,d]));
  pending.set(decision.product_id,decision);
  const mappedProducts=products.map(product=>{
   const local=pending.get(product.shopify_product_id);
   return {...product,design_ids:designIdsFor(product,local),launch_selected:!!local?.launch_selected};
  });
  impact=computeDesignImpact(decision.current_design_id,mappedProducts,[...pending.values()]);
  const confirmed=await confirmGlobalReject(impact);
  if(!confirmed)return {ok:false,cancelled:true,impact};
 }
 await repo.saveProductDecision(decision);
 if(decision.design_decision==='reject_global'&&decision.current_design_id){
  await repo.saveDesignDecision({design_id:decision.current_design_id,status:'rejected_globally',decided_by:decision.decided_by,note:decision.note});
 }
 return {ok:true,impact};
}
