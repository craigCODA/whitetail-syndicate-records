import test from 'node:test';
import assert from 'node:assert/strict';
import {commitProductDecision} from '../../src/domain/product-decision-flow.js';

const product={shopify_product_id:'p1',variant_count_current:12,design_ids_current:[]};

test('cancelled global rejection saves nothing and counts the pending product in blast radius', async()=>{
 const saved=[]; let seenImpact=null;
 const repo={saveProductDecision:async d=>saved.push(['product',d]),saveDesignDecision:async d=>saved.push(['design',d])};
 const decision={product_id:'p1',current_design_id:'D01',design_decision:'reject_global',decided_by:'Kraig'};
 const result=await commitProductDecision({decision,repo,products:[product],currentDecisions:[],confirmGlobalReject:async impact=>{seenImpact=impact;return false;}});
 assert.equal(result.cancelled,true);
 assert.equal(saved.length,0);
 assert.equal(seenImpact.productCount,1);
 assert.deepEqual(seenImpact.affectedProductIds,['p1']);
});

test('confirmed global rejection persists both local records only after confirmation', async()=>{
 const saved=[];
 const repo={saveProductDecision:async d=>saved.push(['product',d]),saveDesignDecision:async d=>saved.push(['design',d])};
 const decision={product_id:'p1',current_design_id:'D01',design_decision:'reject_global',decided_by:'Kraig',note:'remove it'};
 const result=await commitProductDecision({decision,repo,products:[product],currentDecisions:[],confirmGlobalReject:async()=>true});
 assert.equal(result.ok,true);
 assert.deepEqual(saved.map(x=>x[0]),['product','design']);
 assert.equal(saved[1][1].status,'rejected_globally');
});
