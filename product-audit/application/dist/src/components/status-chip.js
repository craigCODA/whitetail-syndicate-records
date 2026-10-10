export const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function statusChip(label,tone='neutral'){return `<span class="chip chip-${tone}">${esc(label)}</span>`}
