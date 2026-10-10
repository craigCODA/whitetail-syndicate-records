import test from 'node:test';import assert from 'node:assert/strict';
import {importDecisionFile} from '../../src/export/import-decisions.js';
const state={store_domain:'www.whitetailsyndicate.com',schema_version:1,knownProductIds:new Set(['p1'])};
test('rejects corrupt, foreign, newer-schema, and baseline mutation imports',()=>{
 assert.equal(importDecisionFile('{',state).ok,false);
 assert.equal(importDecisionFile(JSON.stringify({store_domain:'x',schema_version:1}),state).ok,false);
 assert.equal(importDecisionFile(JSON.stringify({store_domain:state.store_domain,schema_version:2}),state).ok,false);
 assert.equal(importDecisionFile(JSON.stringify({store_domain:state.store_domain,schema_version:1,products:[{shopify_product_id:'p1',title_current:'hack'}]}),state).ok,false);
});
