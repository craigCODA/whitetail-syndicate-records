import test from 'node:test';import assert from 'node:assert/strict';
import {renderActionQueue} from '../../src/views/action-queue.js';
test('action queue shows exact proposed target value',()=>{const html=renderActionQueue([{title:'Baby',handle:'baby',type:'title_rewrite',owner:'Craig',priority:'normal',status:'open',reason:'Title decision',target_value:'Fawn One Piece'}]);assert.ok(html.includes('Fawn One Piece'));assert.ok(html.includes('Target'));});
