import test from 'node:test';
import assert from 'node:assert/strict';
import {chooseNextProductId} from '../../src/domain/review-order.js';
test('skip-later is deferred until every unreviewed product has been handled',()=>{
 const products=[{shopify_product_id:'p1'},{shopify_product_id:'p2'},{shopify_product_id:'p3'}];
 const decisions=new Map([['p1',{review_state:'skip_later'}],['p2',{review_state:'reviewed'}]]);
 const flags=new Map(products.map(p=>[p.shopify_product_id,[]]));
 assert.equal(chooseNextProductId(products,decisions,flags),'p3');
 decisions.set('p3',{review_state:'reviewed'});
 assert.equal(chooseNextProductId(products,decisions,flags),'p1');
});
