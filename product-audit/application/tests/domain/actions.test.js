import test from 'node:test';import assert from 'node:assert/strict';
import {generateActions} from '../../src/domain/actions.js';
const p={shopify_product_id:'p1',handle_current:'baby',title_current:'Baby',provider_verification:'unknown'};
test('decisions generate local Craig/provider actions without store writes',()=>{
 const a=generateActions({products:[p],productDecisions:[{product_id:'p1',audience:'fawn',disposition:'move',description_flags:['rewrite']}],designDecisions:[],flags:[]});
 assert.ok(a.some(x=>x.type==='collection_correction'&&x.owner==='Craig'));
 assert.ok(a.some(x=>x.type==='copy_rewrite'));
 assert.ok(a.some(x=>x.type==='provider_verification'));
 assert.ok(a.every(x=>x.live_store_write===false));
});
test('merge remains blocked until provider verification',()=>{
 const a=generateActions({products:[p],productDecisions:[{product_id:'p1',disposition:'merge_candidate'}],designDecisions:[],flags:[]});
 assert.ok(a.some(x=>x.type==='merge_preparation'&&x.status==='blocked'));
});

test('local provider verification suppresses provider-check action',()=>{const a=generateActions({products:[p],productDecisions:[{product_id:'p1',disposition:'keep',provider_verification:'verified'}],designDecisions:[],flags:[]});assert.equal(a.some(x=>x.type==='provider_verification'),false);});
test('proposed title and description become explicit local copy actions',()=>{
 const a=generateActions({products:[p],productDecisions:[{product_id:'p1',disposition:'repair',title_decision:'rewrite',proposed_title:'Fawn One Piece',proposed_description:'New local copy',provider_verification:'verified'}],designDecisions:[],flags:[]});
 assert.ok(a.some(x=>x.type==='title_rewrite'&&x.target_value==='Fawn One Piece'));
 assert.ok(a.some(x=>x.type==='copy_rewrite'&&x.target_value==='New local copy'));
});
test('global design rejection creates blockers for every locally mapped product',()=>{
 const p2={...p,shopify_product_id:'p2',handle_current:'other',title_current:'Other'};
 const a=generateActions({products:[p,p2],productDecisions:[{product_id:'p1',current_design_id:'D01',provider_verification:'verified'},{product_id:'p2',current_design_id:'D02',provider_verification:'verified'}],designDecisions:[{design_id:'D01',status:'rejected_globally'}],flags:[]});
 const hit=a.filter(x=>x.type==='design_replacement');assert.equal(hit.length,1);assert.equal(hit[0].product_id,'p1');assert.equal(hit[0].status,'blocked');
});
test('unreviewed products do not flood the action queue with provider checks',()=>{const a=generateActions({products:[p],productDecisions:[],designDecisions:[],flags:[]});assert.equal(a.length,0);});
test('keep-as-is audience classification does not create a collection correction',()=>{const a=generateActions({products:[p],productDecisions:[{product_id:'p1',audience:'fawn',disposition:'keep',provider_verification:'verified'}],designDecisions:[],flags:[]});assert.equal(a.some(x=>x.type==='collection_correction'),false);});
test('cross-list action carries every explicit target collection',()=>{const a=generateActions({products:[p],productDecisions:[{product_id:'p1',audience:'shared',disposition:'cross_list',target_collections:['fawn','yearling'],provider_verification:'verified'}],designDecisions:[],flags:[]});const x=a.find(x=>x.type==='collection_correction');assert.equal(x.target_value,'fawn | yearling');});
test('provider not-applicable suppresses provider verification action',()=>{const a=generateActions({products:[p],productDecisions:[{product_id:'p1',disposition:'keep',provider_verification:'not_applicable'}],designDecisions:[],flags:[]});assert.equal(a.some(x=>x.type==='provider_verification'),false);});
