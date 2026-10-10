import {productCard} from '../components/product-card.js';
export function renderDashboard({products,decisions,flagMap,filter='all'}){
 const reviewed=products.filter(p=>decisions.get(p.shopify_product_id)?.review_state==='reviewed').length;
 const waiting=products.length-reviewed; const flagged=products.filter(p=>(flagMap.get(p.shopify_product_id)||[]).length).length;
 let shown=products;if(filter==='needs-kraig')shown=products.filter(p=>decisions.get(p.shopify_product_id)?.review_state!=='reviewed'); if(filter==='flagged')shown=products.filter(p=>(flagMap.get(p.shopify_product_id)||[]).length);
 return `<section class="dashboard-hero"><p class="eyebrow">OCTOBER 6 LIVE BASELINE</p><h2>125 products.<br>One decision on every one.</h2><p>Source store remains read only. Decisions and proposed changes stay on this device.</p></section>
 <div class="metrics"><button data-filter="all"><strong>${products.length}</strong><span>Current products</span></button><button data-filter="needs-kraig"><strong>${waiting}</strong><span>Waiting on Kraig</span></button><button data-filter="flagged"><strong>${flagged}</strong><span>Flagged for review</span></button><div><strong>${reviewed}</strong><span>Reviewed</span></div></div>
 <div class="shortcut-grid"><button data-review-next class="primary">Review next product</button><button data-filter="needs-kraig">Needs Kraig</button><button data-route="actions">Needs Craig</button><button data-route="actions">Provider check</button><button data-route="duplicates">Duplicate candidates</button><button data-route="designs">Design library</button><button data-route="launch">Launch collection</button></div>
 <section class="list-head"><div><p class="eyebrow">CATALOG</p><h3>${shown.length} products shown</h3></div><input id="catalog-search" placeholder="Search title, handle, vendor…"></section><div id="product-list">${shown.map(p=>productCard(p,decisions.get(p.shopify_product_id),flagMap.get(p.shopify_product_id)||[])).join('')}</div>`;
}
