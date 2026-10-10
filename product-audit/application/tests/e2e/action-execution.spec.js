import test from 'node:test';import assert from 'node:assert/strict';
import {renderActionQueue} from '../../src/views/action-queue.js';
test('action queue can show local execution state and completion control',()=>{const a={id:'title:p1',title:'Baby',handle:'baby',type:'title_rewrite',owner:'Craig',priority:'normal',status:'open',reason:'Title',target_value:'Fawn'};const html=renderActionQueue([a],new Map([['title:p1',{action_id:'title:p1',status:'done'}]]));assert.ok(html.includes('DONE'));assert.ok(html.includes('data-action-status'));});
