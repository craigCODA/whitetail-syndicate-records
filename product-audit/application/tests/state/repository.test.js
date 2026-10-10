import test from 'node:test'; import assert from 'node:assert/strict';
import {createRepository,createMemoryAdapter} from '../../src/state/repository.js';

test('saves decisions locally and preserves created history',async()=>{
 const repo=createRepository(createMemoryAdapter());
 await repo.saveProductDecision({product_id:'p1',review_state:'reviewed',disposition:'move',decided_by:'Kraig'});
 const a=await repo.getProductDecision('p1'); assert.equal(a.disposition,'move'); assert.ok(a.created_at);
 await repo.saveProductDecision({product_id:'p1',review_state:'reviewed',disposition:'hold',decided_by:'Kraig'});
 const b=await repo.getProductDecision('p1'); assert.equal(b.disposition,'hold'); assert.equal(b.created_at,a.created_at); assert.ok(b.updated_at);
});

test('stores skip/later, design decisions and execution state separately',async()=>{
 const repo=createRepository(createMemoryAdapter());
 await repo.saveProductDecision({product_id:'p2',review_state:'skip_later'});
 await repo.saveDesignDecision({design_id:'D01',status:'approved_master'});
 await repo.saveExecutionState({action_id:'a1',status:'done'});
 assert.equal((await repo.getProductDecision('p2')).review_state,'skip_later');
 assert.equal((await repo.listDesignDecisions())[0].status,'approved_master');
 assert.equal((await repo.listExecutionStates())[0].status,'done');
});
