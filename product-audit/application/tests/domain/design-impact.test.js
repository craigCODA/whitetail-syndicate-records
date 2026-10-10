import test from 'node:test';import assert from 'node:assert/strict';
import {computeDesignImpact} from '../../src/domain/design-impact.js';
const products=[
 {shopify_product_id:'p1',variant_count_current:10,design_ids:['D01'],launch_selected:true},
 {shopify_product_id:'p2',variant_count_current:5,design_ids:['D01','D02'],launch_selected:false},
 {shopify_product_id:'p3',variant_count_current:2,design_ids:[],launch_selected:true}
];
test('global reject reports blast radius and mixed products require manual review',()=>{
 const x=computeDesignImpact('D01',products,[]);
 assert.equal(x.productCount,2);assert.equal(x.knownVariantCount,15);assert.equal(x.launchProductCount,1);
 assert.deepEqual(x.mixedProductIds,['p2']);assert.equal(x.replacementCandidates.length,1);assert.equal(x.manualReviewRequired.includes('p2'),true);
});
import {normalizeDesignKey} from '../../src/domain/design-impact.js';
test('custom design labels become distinct stable local keys',()=>{
 assert.equal(normalizeDesignKey('OTHER','Old antler badge'),'OTHER:old-antler-badge');
 assert.equal(normalizeDesignKey('D01','ignored'),'D01');
});
import {canApplyGlobalReject} from '../../src/domain/design-impact.js';
test('global reject requires a mapped design identity',()=>{assert.equal(canApplyGlobalReject({design_decision:'reject_global',current_design_id:''}),false);assert.equal(canApplyGlobalReject({design_decision:'reject_global',current_design_id:'D03'}),true);assert.equal(canApplyGlobalReject({design_decision:'keep',current_design_id:''}),true);});
test('unlabeled OTHER design cannot become a global key',()=>{assert.equal(normalizeDesignKey('OTHER',''), '');});
