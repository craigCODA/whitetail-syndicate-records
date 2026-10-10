import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
test('service worker caches app shell and bundled baseline without Shopify admin endpoints',()=>{
 const sw=fs.readFileSync(new URL('../../public/sw.js',import.meta.url),'utf8');
 assert.ok(sw.includes('data/normalized/products.json'));
 assert.ok(sw.includes('data/raw/october-1-audit-reference.json'));
 assert.ok(!/admin\/api|graphql_mutation|update_product|set_inventory/i.test(sw));
});
test('manifest launches the root app from /public/manifest.webmanifest',()=>{
 const m=JSON.parse(fs.readFileSync(new URL('../../public/manifest.webmanifest',import.meta.url),'utf8'));
 assert.equal(m.start_url,'../');
 assert.equal(m.scope,'../');
 assert.equal(m.icons[0].src,'./icon.svg');
});
test('baseline data refresh is network-first so a new read-only snapshot can replace cache',()=>{
 const sw=fs.readFileSync(new URL('../../public/sw.js',import.meta.url),'utf8');
 assert.ok(sw.includes("url.pathname.includes('/data/')"));
 assert.ok(sw.includes('fetch(event.request)'));
});
test('root service worker matches the source worker used by the locally served app',()=>{const pub=fs.readFileSync(new URL('../../public/sw.js',import.meta.url),'utf8');const root=fs.readFileSync(new URL('../../sw.js',import.meta.url),'utf8');assert.equal(root,pub);});
