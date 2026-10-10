import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { normalizeBaseline } from '../../scripts/normalize-baseline.mjs';

const live=JSON.parse(fs.readFileSync(new URL('../../data/raw/shopify-live-2026-10-06.json', import.meta.url)));
const audit=JSON.parse(fs.readFileSync(new URL('../../data/raw/october-1-audit-reference.json', import.meta.url)));

test('normalizes the Oct 6 baseline without losing identities',()=>{
 const result=normalizeBaseline({liveProducts:live.products,liveCollections:live.collections,audit,liveMeta:live});
 assert.equal(result.meta.liveProductCount,125);
 assert.equal(result.meta.liveVariantCount,1722);
 assert.equal(result.meta.collectionCount,8);
 assert.equal(result.meta.addedSinceAudit.length,18);
 assert.deepEqual(result.meta.removedSinceAudit,['cotton-blend-cap']);
 assert.equal(result.products.length,125);
 assert.equal(new Set(result.products.map(p=>p.shopify_product_id)).size,125);
});

test('preserves current collection mismatch evidence',()=>{
 const result=normalizeBaseline({liveProducts:live.products,liveCollections:live.collections,audit,liveMeta:live});
 const byHandle=Object.fromEntries(result.products.map(p=>[p.handle_current,p]));
 for(const h of ['baby-short-sleeve-one-piece','baby-short-sleeve-one-piece-1','baby-short-sleeve-one-piece-2'])
   assert.ok(byHandle[h].collections_current.includes('The Yearling Collection'));
 for(const h of ['mens-rash-guard','men-s-windbreaker','men-s-windbreaker-1'])
   assert.ok(byHandle[h].collections_current.includes('The Doe Collection'));
});
import { validateBaseline, diffSnapshots } from '../../src/data/validate-baseline.js';

test('baseline validation rejects missing or duplicate Shopify GIDs',()=>{
 assert.equal(validateBaseline([{shopify_product_id:'gid://shopify/Product/1'}]).valid,true);
 assert.equal(validateBaseline([{handle_current:'x'}]).valid,false);
 assert.equal(validateBaseline([{shopify_product_id:'gid://shopify/Product/1'},{shopify_product_id:'gid://shopify/Product/1'}]).valid,false);
});

test('snapshot diff follows Shopify GID even when handle changes',()=>{
 const oldS=[{shopify_product_id:'gid://shopify/Product/1',handle_current:'old'},{shopify_product_id:'gid://shopify/Product/2',handle_current:'gone'}];
 const newS=[{shopify_product_id:'gid://shopify/Product/1',handle_current:'new'},{shopify_product_id:'gid://shopify/Product/3',handle_current:'added'}];
 const d=diffSnapshots(oldS,newS);
 assert.deepEqual(d.addedIds,['gid://shopify/Product/3']);
 assert.deepEqual(d.removedIds,['gid://shopify/Product/2']);
 assert.equal(d.changedHandles[0].from,'old');
 assert.equal(d.changedHandles[0].to,'new');
});
