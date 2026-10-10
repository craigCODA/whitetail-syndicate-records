import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {buildDuplicateGroups} from '../../src/domain/duplicates.js';
const products=JSON.parse(fs.readFileSync(new URL('../../data/normalized/products.json',import.meta.url)));
const audit=JSON.parse(fs.readFileSync(new URL('../../data/raw/october-1-audit-reference.json',import.meta.url)));
test('duplicate title and shared-SKU evidence remain signals only',()=>{
 const groups=buildDuplicateGroups(products,audit);
 const babies=groups.find(g=>g.members.some(m=>m.handle==='baby-short-sleeve-one-piece'));
 assert.ok(babies&&babies.reason==='repeated_title'); assert.equal(babies.merge_decision,undefined);
 const ideal=groups.find(g=>g.reason==='shared_sku_evidence'); assert.ok(ideal); assert.equal(ideal.priority,'high'); assert.equal(ideal.merge_decision,undefined);
});
