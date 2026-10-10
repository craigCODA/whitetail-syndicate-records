const CACHE='whitetail-product-control-v1';
const ASSETS=[
 './','./index.html','./src/styles.css','./src/app.js','./src/config.js',
 './src/data/load-baseline.js','./src/data/validate-baseline.js','./src/state/db.js','./src/state/repository.js',
 './src/domain/flags.js','./src/domain/duplicates.js','./src/domain/review-order.js','./src/domain/design-impact.js','./src/domain/product-decision-flow.js','./src/domain/actions.js','./src/domain/readiness.js',
 './src/export/exporters.js','./src/export/import-decisions.js',
 './src/views/dashboard.js','./src/views/product-review.js','./src/views/design-library.js','./src/views/duplicate-review.js','./src/views/action-queue.js','./src/views/launch-collection.js',
 './src/components/status-chip.js','./src/components/flag-list.js','./src/components/decision-controls.js','./src/components/product-card.js','./src/components/confirmation-dialog.js',
 './data/normalized/products.json','./data/normalized/designs.json','./data/normalized/audit-flags.json','./data/normalized/snapshot-meta.json','./data/raw/october-1-audit-reference.json',
 './public/manifest.webmanifest','./public/icon.svg'
];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);
 if(url.origin!==self.location.origin)return;
 if(url.pathname.includes('/data/')){event.respondWith(fetch(event.request).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put(event.request,copy));return res}).catch(()=>caches.match(event.request)));return;}
 event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put(event.request,copy));return res}).catch(()=>caches.match('./index.html'))));
});
