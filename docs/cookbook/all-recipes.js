/* Unified read-only catalog. Opening entries never saves or rewrites recipes. */
'use strict';
let allQuery='',allKind='All',allPage=0;
const originalFormats=new Map();
function formatOriginalEntry(entry){
 if(originalFormats.has(entry.id))return originalFormats.get(entry.id);
 let recipe=null;
 const blocks=entry.text.match(/(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?ingredients\b/gi)||[];
 if(blocks.length<=1){try{const pack=T.parse(entry.text);if(pack.recipes.length===1)recipe=pack.recipes[0];}catch(_){}}
 const result={recipe,incomplete:!recipe||recipe.notes.includes('placeholder')||recipe.ingredients.some(i=>i.amount===null)||T.coverage(recipe).length>0};
 originalFormats.set(entry.id,result);return result;
}
function allEntries(){return [
 ...state.recipes.map(recipe=>({id:recipe.id,title:recipe.title,kind:'Saved',recipe,search:[recipe.title,...recipe.ingredients.map(i=>i.name)].join(' ')})),
 ...library500.map(e=>({id:e.recipe.id,title:e.recipe.title,kind:'500 suggestions',recipe:e.recipe,search:[e.recipe.title,...e.recipe.ingredients.map(i=>i.name)].join(' ')})),
 ...tailoredEntries.map(e=>({id:e.recipe.id,title:e.recipe.title,kind:'10 suggestions',recipe:e.recipe,search:[e.recipe.title,...e.recipe.ingredients.map(i=>i.name)].join(' ')})),
 ...SOUTHERN_RECIPES.map(e=>({id:e.recipe.id,title:e.recipe.title,kind:'Southern & Lowcountry',recipe:e.recipe,search:[e.recipe.title,...e.recipe.ingredients.map(i=>i.name)].join(' ')})),
 ...EASY_WEB_RECIPES.map(e=>({id:e.recipe.id,title:e.recipe.title,kind:'Easy web recipes',recipe:e.recipe,search:[e.recipe.title,...e.recipe.ingredients.map(i=>i.name)].join(' ')})),
 ...sourceArchive.entries.map(e=>({id:e.id,title:e.title,kind:'Recovered originals',recipe:e,search:e.title+' '+e.text}))
 ];}
let allRows=[];
function allRecipes(){allRows=allEntries().map(e=>({...e,search:e.search.toLocaleLowerCase()}));modal(`<h2>All recipes & notes</h2><p class="small">Your saved shelf, suggestions and recovered history in one place. Archive notes and versions are not additional unique recipes.</p><label class="field">Search everything<input id="all-search" type="search" value="${esc(allQuery)}" placeholder="Recipe or ingredient"></label><label class="field">Collection<select id="all-kind">${['All','Saved','500 suggestions','10 suggestions','Southern & Lowcountry','Easy web recipes','Recovered originals'].map(k=>`<option ${k===allKind?'selected':''}>${k}</option>`).join('')}</select></label><div id="all-results"></div>${button('Close','close-modal')}`);allResults();}
function allResults(){const terms=allQuery.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);const rows=allRows.filter(e=>(allKind==='All'||e.kind===allKind)&&terms.every(t=>e.search.includes(t)));const pages=Math.max(1,Math.ceil(rows.length/20));allPage=Math.min(allPage,pages-1);$('#all-results').innerHTML=`<p class="small">${rows.length} entries · page ${allPage+1} of ${pages}</p>`+rows.slice(allPage*20,allPage*20+20).map(e=>`<article class="history-item">${recipeArt(e.recipe,'idea-cover')}<span class="badge">${esc(e.kind)}</span><h3>${esc(e.title)}</h3>${button('Open recipe or note','all-open','',`data-id="${esc(e.id)}" data-kind="${esc(e.kind)}"`)}</article>`).join('')+`<div class="row">${button('Previous page','all-prev','',allPage===0?'disabled':'')}${button('Next page','all-next','',allPage===pages-1?'disabled':'')}</div>`;}
function readableOriginal(text){
 return text.split(/\r?\n/).filter(l=>l.trim()).map(line=>{
  const heading=line.match(/^\s*#{1,6}\s+(.+)|^\s*\*\*([^*]+)\*\*\s*:??\s*$/);
  const clean=s=>esc(s.replace(/\*\*|__/g,''));
  if(heading)return `<h3>${clean(heading[1]||heading[2])}</h3>`;
  const numbered=line.match(/^\s*(\d+)[.)]\s+(.+)/);if(numbered)return `<div class="step"><span class="step-number">${esc(numbered[1])}</span><div>${clean(numbered[2])}</div></div>`;
  return `<p class="source-paragraph">${clean(line.replace(/^\s*[-*•]\s+/,''))}</p>`;
 }).join('');
}
readOriginal=id=>{
 const entry=sourceArchive.entries.find(e=>e.id===id);if(!entry)return;
 const {recipe:r,incomplete}=formatOriginalEntry(entry);
 const body=r?`<p class="small">${r.notes.includes('placeholder')?'Yield not recorded':`${r.servings} ${esc(r.yieldUnit)}`}${r.minutes?' · '+r.minutes+' minutes':''}</p><h3>Ingredients</h3>${r.ingredients.map(i=>`<p class="idea-ingredient">${esc(K.ingredientText(i))}</p>`).join('')}<h3>Instructions</h3>${K.steps(r).map((step,n)=>`<div class="step"><span class="step-number">${n+1}</span><div>${esc(step)}</div></div>`).join('')}<h3>Notes</h3><p class="source-paragraph">${esc(r.notes.replace('Review needed: servings were not supplied; 4 is a placeholder. Set the correct yield before scaling.','Yield not recorded. Do not scale until the original yield is confirmed.'))}</p>`:readableOriginal(entry.text);
 modal(`${recipeArt(entry,'idea-cover')}<span class="badge">${r?'Formatted recovered recipe':'Original recipe text or cooking note'}</span><h2>${esc(entry.title)}</h2><p class="small">${esc(entry.sources[0].chatTitle)} · ${esc(entry.date)}. Historical text, not kitchen-tested.</p>${incomplete?'<p class="review-warning">This entry needs review: it may be a partial recipe, several recipes, or have missing yield or unlinked amounts. Original details are preserved; missing quantities have not been invented.</p>':''}${body}<details><summary>Unchanged source text</summary><div class="original-recipe-text">${esc(entry.text)}</div></details><div class="maker-actions">${button('Format & save a recipe','format-original','primary',`data-source-id="${esc(id)}"`)}${button('Back to all recipes','all-browse')}${button('Back to originals','browse-originals')}${button('Close','close-modal')}</div>`);
};
const homeBeforeAll=home;
home=()=>homeBeforeAll().replace('<section class="shelf-start"',`<section class="panel all-entry"><h2>Everything in your kitchen</h2><p class="small">Saved recipes, 760 suggestions, 500 easy web recipes and ${sourceArchive.entries.length} recovered recipes and notes. Every entry has a cover image.</p>${button('Browse all recipes & notes','all-browse','primary')}</section><section class="shelf-start"`);
document.addEventListener('input',e=>{if(e.target.id==='all-search'){allQuery=e.target.value;allPage=0;allResults();}});
document.addEventListener('change',e=>{if(e.target.id==='all-kind'){allKind=e.target.value;allPage=0;allResults();}});
document.addEventListener('click',e=>{const b=e.target.closest('[data-action]');if(!b||!b.dataset.action.startsWith('all-'))return;e.preventDefault();e.stopImmediatePropagation();const a=b.dataset.action;if(a==='all-browse')allRecipes();if(a==='all-next'||a==='all-prev'){allPage+=a==='all-next'?1:-1;allResults();$('#modal').scrollTop=0;}if(a==='all-open'){const {id,kind}=b.dataset;if(kind==='Recovered originals')readOriginal(id);else if(kind==='500 suggestions')libraryReview(id);else if(kind==='10 suggestions')tailoredReview(id);else if(kind==='Southern & Lowcountry')southernReview(id);else if(kind==='Easy web recipes')easywebReview(id);else{closeModal();view={type:'detail',id};detailYield=state.recipes.find(r=>r.id===id).servings;render();}if($('#modal')?.open&&!$('#modal').querySelector('[data-action="all-browse"]'))$('#modal').insertAdjacentHTML('beforeend',button('Back to all recipes','all-browse'));}},true);
render();
