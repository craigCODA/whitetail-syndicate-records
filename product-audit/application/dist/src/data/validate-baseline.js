export function validateBaseline(products){
 const errors=[]; const ids=new Set();
 for(const [i,p] of products.entries()){
   if(!p.shopify_product_id) errors.push(`product ${i} missing Shopify GID`);
   else if(ids.has(p.shopify_product_id)) errors.push(`duplicate Shopify GID ${p.shopify_product_id}`);
   else ids.add(p.shopify_product_id);
 }
 return {valid:errors.length===0,errors};
}
export function diffSnapshots(oldProducts,newProducts){
 const oldMap=new Map(oldProducts.map(p=>[p.shopify_product_id,p]));
 const newMap=new Map(newProducts.map(p=>[p.shopify_product_id,p]));
 const addedIds=[...newMap.keys()].filter(id=>!oldMap.has(id)).sort();
 const removedIds=[...oldMap.keys()].filter(id=>!newMap.has(id)).sort();
 const changedHandles=[];
 for(const [id,n] of newMap){const o=oldMap.get(id); if(o&&o.handle_current!==n.handle_current) changedHandles.push({id,from:o.handle_current,to:n.handle_current});}
 return {addedIds,removedIds,changedHandles};
}
