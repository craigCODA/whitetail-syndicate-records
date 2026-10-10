export function importDecisionFile(text,state){
 let data;try{data=JSON.parse(text)}catch{return {ok:false,error:'Invalid JSON'}}
 if(data.store_domain!==state.store_domain)return {ok:false,error:'Wrong store domain'};
 if(Number(data.schema_version)>Number(state.schema_version))return {ok:false,error:'Newer schema is not supported'};
 if(data.products||data.baseline||data.source_products)return {ok:false,error:'Import may not alter source baseline'};
 const list=data.product_decisions||[];const unresolved=list.filter(d=>!state.knownProductIds.has(d.product_id)).map(d=>d.product_id);
 return {ok:true,product_decisions:list.filter(d=>state.knownProductIds.has(d.product_id)),design_decisions:data.design_decisions||[],execution_states:data.execution_states||[],unresolved};
}
