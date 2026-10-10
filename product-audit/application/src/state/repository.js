const now=()=>new Date().toISOString();
export function createMemoryAdapter(){
 const stores=new Map();
 const store=n=>{if(!stores.has(n)) stores.set(n,new Map());return stores.get(n)};
 return {async get(s,k){return structuredClone(store(s).get(k)??null)},async put(s,k,v){store(s).set(k,structuredClone(v));},async list(s){return [...store(s).values()].map(v=>structuredClone(v))},async clear(s){store(s).clear();}};
}
export function createRepository(adapter){
 const save=async(store,keyField,input)=>{const key=input[keyField];if(!key)throw new Error(`${keyField} required`);const old=await adapter.get(store,key);const ts=now();const rec={...(old||{}),...input,created_at:old?.created_at||ts,updated_at:ts};await adapter.put(store,key,rec);return rec};
 return {
  saveProductDecision:d=>save('product_decisions','product_id',d),
  getProductDecision:id=>adapter.get('product_decisions',id),
  listProductDecisions:()=>adapter.list('product_decisions'),
  saveDesignDecision:d=>save('design_decisions','design_id',d),
  listDesignDecisions:()=>adapter.list('design_decisions'),
  saveExecutionState:d=>save('execution_states','action_id',d),
  listExecutionStates:()=>adapter.list('execution_states'),
  exportDecisionState:async()=>({product_decisions:await adapter.list('product_decisions'),design_decisions:await adapter.list('design_decisions'),execution_states:await adapter.list('execution_states')})
 };
}
