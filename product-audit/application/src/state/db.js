import {createRepository} from './repository.js';
export function openProductControlDb(){
 return new Promise((resolve,reject)=>{
  if(!('indexedDB' in globalThis)) return reject(new Error('IndexedDB unavailable'));
  const req=indexedDB.open('whitetail-product-control',1);
  req.onupgradeneeded=()=>{const db=req.result;for(const s of ['product_decisions','design_decisions','execution_states','app_meta'])if(!db.objectStoreNames.contains(s))db.createObjectStore(s);};
  req.onerror=()=>reject(req.error);
  req.onsuccess=()=>{
   const db=req.result;
   const adapter={
    get:(s,k)=>new Promise((res,rej)=>{const r=db.transaction(s).objectStore(s).get(k);r.onsuccess=()=>res(r.result??null);r.onerror=()=>rej(r.error)}),
    put:(s,k,v)=>new Promise((res,rej)=>{const r=db.transaction(s,'readwrite').objectStore(s).put(v,k);r.onsuccess=()=>res();r.onerror=()=>rej(r.error)}),
    list:s=>new Promise((res,rej)=>{const r=db.transaction(s).objectStore(s).getAll();r.onsuccess=()=>res(r.result||[]);r.onerror=()=>rej(r.error)}),
    clear:s=>new Promise((res,rej)=>{const r=db.transaction(s,'readwrite').objectStore(s).clear();r.onsuccess=()=>res();r.onerror=()=>rej(r.error)})
   };
   resolve(createRepository(adapter));
  };
 });
}
