const validWaiver=w=>w&&w.owner&&w.timestamp&&w.note;
const resolved=v=>v==='verified'||v==='not_applicable';
export function waiversFromDecision(decision={}){
 const out={};
 if(String(decision.provider_waiver_note||'').trim())out.provider_verification={owner:decision.decided_by||'Kraig',timestamp:decision.updated_at||decision.decided_at||'',note:decision.provider_waiver_note.trim()};
 if(String(decision.sample_waiver_note||'').trim())out.sample_status={owner:decision.decided_by||'Kraig',timestamp:decision.updated_at||decision.decided_at||'',note:decision.sample_waiver_note.trim()};
 return out;
}
export function evaluateReadiness(product,{launchSelected=false,decision={},waivers={}}={}){
 if(!launchSelected)return {ready:false,missing:['not_selected_for_launch']};
 const missing=[];
 if(!decision||!decision.disposition||['hold','retire','investigate','merge_candidate'].includes(decision.disposition))missing.push('owner_disposition');
 if(!resolved(decision.provider_verification||product.provider_verification)&&!validWaiver(waivers.provider_verification))missing.push('provider_verification');
 if(!resolved(decision.sample_status||product.sample_status)&&!validWaiver(waivers.sample_status))missing.push('sample_status');
 return {ready:missing.length===0,missing,waivers};
}
