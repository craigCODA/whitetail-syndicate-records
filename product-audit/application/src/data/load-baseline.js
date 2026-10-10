import {validateBaseline} from './validate-baseline.js';
const deepFreeze=o=>{if(o&&typeof o==='object'&&!Object.isFrozen(o)){Object.freeze(o);Object.values(o).forEach(deepFreeze)}return o};
export async function loadBaseline(){
 const [products,designs,flags,meta]=await Promise.all([
   fetch('./data/normalized/products.json').then(r=>r.json()),
   fetch('./data/normalized/designs.json').then(r=>r.json()),
   fetch('./data/normalized/audit-flags.json').then(r=>r.json()),
   fetch('./data/normalized/snapshot-meta.json').then(r=>r.json())
 ]);
 const check=validateBaseline(products); if(!check.valid) throw new Error(check.errors.join('; '));
 return deepFreeze({products,designs,flags,meta});
}
