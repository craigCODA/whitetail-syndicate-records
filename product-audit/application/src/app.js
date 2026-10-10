import {loadBaseline} from './data/load-baseline.js';
import {openProductControlDb} from './state/db.js';
import {createMemoryAdapter,createRepository} from './state/repository.js';
import {computeFlags} from './domain/flags.js';
import {buildDuplicateGroups} from './domain/duplicates.js';
import {chooseNextProductId} from './domain/review-order.js';
import {computeDesignImpact,normalizeDesignKey} from './domain/design-impact.js';
import {commitProductDecision} from './domain/product-decision-flow.js';
import {generateActions} from './domain/actions.js';
import {evaluateReadiness,waiversFromDecision} from './domain/readiness.js';
import {buildExports,downloadExport} from './export/exporters.js';
import {importDecisionFile} from './export/import-decisions.js';
import {STORE_DOMAIN,SNAPSHOT_SCHEMA_VERSION} from './config.js';
import {renderDashboard} from './views/dashboard.js';
import {renderProductReview} from './views/product-review.js';
import {renderDesignLibrary} from './views/design-library.js';
import {renderDuplicateReview} from './views/duplicate-review.js';
import {renderActionQueue} from './views/action-queue.js';
import {renderLaunchCollection} from './views/launch-collection.js';
import {confirmAction} from './components/confirmation-dialog.js';
import './styles.css';

const view=document.querySelector('#view');
const state={baseline:null,repo:null,persistenceError:null,route:'dashboard',filter:'all',productId:null,productDecisions:[],designDecisions:[],executionStates:[]};
const toast=msg=>{const e=document.createElement('div');e.className='toast';e.textContent=msg;document.body.append(e);setTimeout(()=>e.remove(),2200)};
const decisionMap=()=>new Map(state.productDecisions.map(d=>[d.product_id,d]));
const flagMap=()=>{const dm=decisionMap();const rejected=new Set(state.designDecisions.filter(d=>d.status==='rejected_globally').map(d=>d.design_id));return new Map(state.baseline.products.map(p=>{const d=dm.get(p.shopify_product_id);const currentDesignIds=d?.current_design_id?[d.current_design_id]:(p.design_ids_current||p.design_ids||[]);return [p.shopify_product_id,computeFlags(p,{launchSelected:!!d?.launch_selected,currentDesignId:d?.current_design_id||'',currentDesignIds,rejectedDesignIds:rejected,providerVerification:d?.provider_verification,sampleStatus:d?.sample_status})]}));};
const productWithLocalDesign=p=>{const d=decisionMap().get(p.shopify_product_id);return {...p,design_ids:d?.current_design_id?[d.current_design_id]:(p.design_ids_current||p.design_ids||[]),launch_selected:!!d?.launch_selected}};
async function reloadLocal(){state.productDecisions=await state.repo.listProductDecisions();state.designDecisions=await state.repo.listDesignDecisions();state.executionStates=await state.repo.listExecutionStates();}
function nextProductId(){return chooseNextProductId(state.baseline.products,decisionMap(),flagMap())}
function buildActions(){return generateActions({products:state.baseline.products,productDecisions:state.productDecisions,designDecisions:state.designDecisions,flags:[...flagMap().values()].flat()})}
function launchRows(){const dm=decisionMap();return state.baseline.products.map(p=>{const d=dm.get(p.shopify_product_id);const r=evaluateReadiness(p,{launchSelected:!!d?.launch_selected,decision:d||{},waivers:waiversFromDecision(d||{})});return {product_id:p.shopify_product_id,title:p.title_current,handle:p.handle_current,selected:!!d?.launch_selected,...r}}).filter(r=>r.selected)}
function persistenceNotice(){return state.persistenceError?`<div class="notice notice-danger"><strong>Local persistence unavailable.</strong> Decisions cannot be safely saved in this browser. ${state.persistenceError}</div>`:''}
function render(){
 if(!state.baseline)return;
 const dm=decisionMap(),fm=flagMap();
 if(state.route==='product'){
  const p=state.baseline.products.find(x=>x.shopify_product_id===state.productId);view.innerHTML=persistenceNotice()+renderProductReview(p,fm.get(p.shopify_product_id)||[],dm.get(p.shopify_product_id));
 } else if(state.route==='designs') view.innerHTML=persistenceNotice()+renderDesignLibrary({designs:state.baseline.designs,designDecisions:state.designDecisions,productDecisions:state.productDecisions});
 else if(state.route==='duplicates') view.innerHTML=renderDuplicateReview(buildDuplicateGroups(state.baseline.products,window.__auditEvidence||{}),state.baseline.products);
 else if(state.route==='actions') view.innerHTML=renderActionQueue(buildActions(),new Map(state.executionStates.map(x=>[x.action_id,x])))+renderExportPanel();
 else if(state.route==='launch') view.innerHTML=renderLaunchCollection(launchRows());
 else view.innerHTML=persistenceNotice()+renderDashboard({products:state.baseline.products,decisions:dm,flagMap:fm,filter:state.filter});
 bind();
}
function renderExportPanel(){return `<section class="card" style="margin-top:18px"><p class="eyebrow">PORTABLE OUTPUTS</p><h3>Export local control files</h3><p class="muted">Exports contain decisions and action plans only. They do not execute changes.</p><div class="shortcut-grid"><button data-export-all>Download all 5 exports</button><label class="file-btn">Import decision JSON<input type="file" accept="application/json,.json" data-import-decisions hidden></label></div><p class="muted">Import only overlays local decisions. Source catalog fields are rejected.</p></section>`}
function formDecision(form){const fd=new FormData(form);return {product_id:form.dataset.productId,review_state:'reviewed',audience:fd.get('audience')||'',target_collections:fd.getAll('target_collections'),disposition:fd.get('disposition')||'',title_decision:fd.get('title_decision')||'',current_design_id:fd.get('current_design_id')||'',current_design_label:fd.get('current_design_label')||'',design_decision:fd.get('design_decision')||'',proposed_title:fd.get('proposed_title')||'',proposed_description:fd.get('proposed_description')||'',provider_verification:fd.get('provider_verification')||'unknown',sample_status:fd.get('sample_status')||'unknown',provider_waiver_note:fd.get('provider_waiver_note')||'',sample_waiver_note:fd.get('sample_waiver_note')||'',description_flags:fd.getAll('description_flags'),launch_selected:fd.get('launch_selected')==='on',note:fd.get('note')||'',decided_by:fd.get('decided_by')||'Kraig'}}
function bind(){
 document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>{state.route=b.dataset.route;render()});
 document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{state.route='dashboard';state.filter=b.dataset.filter;render()});
 document.querySelectorAll('[data-open-product]').forEach(b=>b.onclick=()=>{state.route='product';state.productId=b.dataset.openProduct;render()});
 document.querySelector('[data-review-next]')?.addEventListener('click',()=>{state.route='product';state.productId=nextProductId();render()});
 const search=document.querySelector('#catalog-search');if(search)search.oninput=()=>{const q=search.value.toLowerCase();document.querySelectorAll('.product-row').forEach(r=>{r.hidden=!r.innerText.toLowerCase().includes(q)})};
 const form=document.querySelector('#decision-form');if(form){
  form.onsubmit=async e=>{e.preventDefault();if(state.persistenceError)return toast('Persistence unavailable — decision was not saved.');const d=formDecision(form);d.current_design_id=normalizeDesignKey(d.current_design_id,d.current_design_label);const result=await commitProductDecision({decision:d,repo:state.repo,products:state.baseline.products,currentDecisions:state.productDecisions,confirmGlobalReject:impact=>confirmAction({title:`Reject ${d.current_design_id} everywhere?`,body:`<p>This local rule currently touches <strong>${impact.productCount}</strong> mapped products and <strong>${impact.knownVariantCount}</strong> known variants. ${impact.mixedProductIds.length} mixed-design products require manual review, and ${impact.unmappedProductIds.length} unmapped products will be forced back through design mapping.</p>`,confirmLabel:'Reject locally'})});if(!result.ok)return toast(result.cancelled?'Global rejection canceled. Nothing was saved.':'Choose the current design identity before rejecting it globally.');await reloadLocal();toast('Local decision saved. Shopify unchanged.');state.productId=nextProductId();render()};
  form.querySelector('[data-skip]').onclick=async()=>{if(state.persistenceError)return toast('Persistence unavailable — skip state was not saved.');await state.repo.saveProductDecision({product_id:form.dataset.productId,review_state:'skip_later',decided_by:'Kraig'});await reloadLocal();state.productId=nextProductId();render()};
 }
 document.querySelectorAll('[data-design-status]').forEach(b=>b.onclick=async()=>{if(state.persistenceError)return;await state.repo.saveDesignDecision({design_id:b.dataset.designId,status:b.dataset.designStatus,decided_by:'Kraig'});await reloadLocal();render()});
 document.querySelectorAll('[data-design-reject]').forEach(b=>b.onclick=async()=>{if(state.persistenceError)return;const id=b.dataset.designReject;const impact=computeDesignImpact(id,state.baseline.products.map(productWithLocalDesign),state.productDecisions);const ok=await confirmAction({title:`Reject ${id} globally?`,body:`<p>${impact.productCount} mapped products · ${impact.knownVariantCount} known variants · ${impact.launchProductCount} launch candidates.</p><p>${impact.mixedProductIds.length} mixed-design products and ${impact.unmappedProductIds.length} unmapped products will require manual review. This creates local blockers only.</p>`,confirmLabel:'Reject locally'});if(ok){await state.repo.saveDesignDecision({design_id:id,status:'rejected_globally',decided_by:'Kraig'});await reloadLocal();render()}});
 document.querySelectorAll('[data-action-status]').forEach(b=>b.onclick=async()=>{if(state.persistenceError)return toast('Persistence unavailable.');await state.repo.saveExecutionState({action_id:b.dataset.actionStatus,status:b.dataset.nextStatus||'done',completed_by:'Craig'});await reloadLocal();render()});
 document.querySelector('[data-export-all]')?.addEventListener('click',()=>{const ex=buildExports({products:state.baseline.products,productDecisions:state.productDecisions,designDecisions:state.designDecisions,actions:buildActions(),readiness:launchRows()});ex.forEach((f,i)=>setTimeout(()=>downloadExport(f),i*180))});
 const importer=document.querySelector('[data-import-decisions]');if(importer)importer.onchange=async()=>{if(state.persistenceError)return toast('Persistence unavailable — import was not applied.');const file=importer.files?.[0];if(!file)return;const text=await file.text();const result=importDecisionFile(text,{store_domain:STORE_DOMAIN,schema_version:SNAPSHOT_SCHEMA_VERSION,knownProductIds:new Set(state.baseline.products.map(p=>p.shopify_product_id))});if(!result.ok)return toast('Import rejected: '+result.error);for(const d of result.product_decisions)await state.repo.saveProductDecision(d);for(const d of result.design_decisions)await state.repo.saveDesignDecision(d);for(const e of result.execution_states||[])await state.repo.saveExecutionState(e);await reloadLocal();toast(`Imported ${result.product_decisions.length} product decisions${result.unresolved.length?`; ${result.unresolved.length} unresolved IDs`:''}.`);render()};
}
async function boot(){
 try{state.baseline=await loadBaseline();window.__auditEvidence=await fetch('./data/raw/october-1-audit-reference.json').then(r=>r.json());}catch(e){view.innerHTML=`<section class="error"><h2>Baseline could not load</h2><p>${e.message}</p></section>`;return}
 try{state.repo=await openProductControlDb();}catch(e){state.persistenceError='Enable browser storage or retry in a standard browser profile.';state.repo=createRepository(createMemoryAdapter())}
 await reloadLocal();render();
 if('serviceWorker' in navigator)navigator.serviceWorker.register('./sw.js').catch(()=>{});
}
boot();
