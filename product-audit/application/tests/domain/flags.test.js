import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {computeFlags} from '../../src/domain/flags.js';import {rankForReview} from '../../src/domain/review-order.js';
const products=JSON.parse(fs.readFileSync(new URL('../../data/normalized/products.json',import.meta.url)));
const by=Object.fromEntries(products.map(p=>[p.handle_current,p]));
test('flags audited collection mismatches',()=>{
 assert.ok(computeFlags(by['baby-short-sleeve-one-piece'],{}).some(f=>f.type==='collection_mismatch'));
 assert.ok(computeFlags(by['mens-rash-guard'],{}).some(f=>f.type==='audience_fit_conflict'));
});
test('review priority keeps stronger issues ahead',()=>{
 assert.ok(rankForReview(by['baby-short-sleeve-one-piece'],[{priority:'P1'}],false)<rankForReview(by['baby-short-sleeve-one-piece'],computeFlags(by['baby-short-sleeve-one-piece'],{}),false));
 assert.ok(rankForReview(by['baby-short-sleeve-one-piece'],computeFlags(by['baby-short-sleeve-one-piece'],{}),false)<rankForReview(by['unisex-t-shirt'],[],false));
 assert.ok(rankForReview(by['unisex-t-shirt'],[],true)<rankForReview(by['unisex-t-shirt'],[],false));
});
test('globally rejected mapped design becomes a product blocker flag',()=>{const p=by['short-sleeve-unisex-t-shirt'];const f=computeFlags(p,{currentDesignId:'D01',rejectedDesignIds:new Set(['D01'])});assert.ok(f.some(x=>x.type==='global_design_rejected'&&x.priority==='P1'));});
test('a global rejection makes unmapped products mandatory design-review blockers',()=>{const p=by['short-sleeve-unisex-t-shirt'];const f=computeFlags(p,{currentDesignId:'',rejectedDesignIds:new Set(['D01'])});assert.ok(f.some(x=>x.type==='design_mapping_required_after_global_reject'&&x.priority==='P1'));});
test('local provider and sample verification overrides clear resolved flags',()=>{const p=by['short-sleeve-unisex-t-shirt'];const f=computeFlags(p,{providerVerification:'not_applicable',sampleStatus:'verified',launchSelected:true});assert.equal(f.some(x=>x.type==='provider_unverified'),false);assert.equal(f.some(x=>x.type==='sample_unverified'),false);});
