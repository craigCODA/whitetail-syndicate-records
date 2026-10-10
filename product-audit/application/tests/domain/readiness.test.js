import test from 'node:test';import assert from 'node:assert/strict';
import {evaluateReadiness} from '../../src/domain/readiness.js';
test('launch product is blocked by provider and sample gates',()=>{
 const r=evaluateReadiness({shopify_product_id:'p1',provider_verification:'unknown',sample_status:'unknown'},{launchSelected:true,decision:{disposition:'keep'}});
 assert.equal(r.ready,false);assert.ok(r.missing.includes('provider_verification'));assert.ok(r.missing.includes('sample_status'));
});
test('explicit waiver requires owner timestamp and note',()=>{
 const bad=evaluateReadiness({shopify_product_id:'p1',provider_verification:'verified',sample_status:'unknown'},{launchSelected:true,decision:{disposition:'keep'},waivers:{sample_status:{owner:'Kraig'}}});
 assert.equal(bad.ready,false);
 const good=evaluateReadiness({shopify_product_id:'p1',provider_verification:'verified',sample_status:'unknown'},{launchSelected:true,decision:{disposition:'keep'},waivers:{sample_status:{owner:'Kraig',timestamp:'2026-10-06T12:00:00Z',note:'owner waiver'}}});
 assert.equal(good.ready,true);
});

test('local verification overlay can satisfy launch gates',()=>{const r=evaluateReadiness({shopify_product_id:'p1',provider_verification:'unknown',sample_status:'unknown'},{launchSelected:true,decision:{disposition:'keep',provider_verification:'verified',sample_status:'verified'}});assert.equal(r.ready,true);});
test('not-applicable provider and sample states satisfy those gates',()=>{const r=evaluateReadiness({shopify_product_id:'p1',provider_verification:'unknown',sample_status:'unknown'},{launchSelected:true,decision:{disposition:'keep',provider_verification:'not_applicable',sample_status:'not_applicable'}});assert.equal(r.ready,true);});
import {waiversFromDecision} from '../../src/domain/readiness.js';
test('owner waiver notes become timestamped readiness waivers from saved decision metadata',()=>{const w=waiversFromDecision({decided_by:'Kraig',updated_at:'2026-10-06T20:00:00Z',provider_waiver_note:'Owner approved provider exception',sample_waiver_note:'Sample exception'});assert.deepEqual(w.provider_verification,{owner:'Kraig',timestamp:'2026-10-06T20:00:00Z',note:'Owner approved provider exception'});assert.equal(w.sample_status.note,'Sample exception');});
