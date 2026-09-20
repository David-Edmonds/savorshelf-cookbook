/* Public collection is separate from personal storage; chunks load on opening. */
(function(){'use strict';
let entries=[],active=null,request=0;const chunks=new Map();
const oldAll=allEntries;
allEntries=function(){const existing=oldAll();const ids=new Set(existing.map(e=>e.id));return existing.concat(entries.filter(e=>!ids.has(e.id)));};
const oldArt=recipeArt;
recipeArt=function(r,cls=''){return r.sourceWording&&!r.photo?'':oldArt(r,cls);};
const oldDetail=detail;
detail=function(){if(!current()?.sourceWording)return oldDetail();detailYield=current().servings;const box=document.createElement('div');box.innerHTML=oldDetail();const control=box.querySelector('.yield-control');if(control)control.outerHTML='<p class="small">Original quantities · yield unspecified. Automatic scaling is unavailable for this source recipe.</p>';for(const p of box.querySelectorAll('p'))if(p.textContent.includes('Quantities scale;'))p.remove();return box.innerHTML;};
async function load(chunk){if(!chunks.has(chunk))chunks.set(chunk,fetch('catalog/'+chunk).then(r=>{if(!r.ok)throw Error('Recipe download failed');return r.json();}).catch(e=>{chunks.delete(chunk);throw e;}));return chunks.get(chunk);}
async function open(entry){const ticket=++request;active=null;modal('<h2>Loading recipe…</h2>'+button('Back to results','uc-back','quiet'));
 try{const data=await load(entry.chunk);if(ticket!==request||!$('#modal').open)return;const r=data.find(r=>r.id===entry.id);if(!r)throw Error('Recipe not found');active=r;
 const prepared=r.sourceWording?r:RecipeTemplate.prepare(r);
 modal(button('Back to results','uc-back','quiet')+`<h2>${esc(r.title)}</h2><p>${esc(r.description)}</p><p class="small">${r.sourceWording?'Original quantities · yield not specified':esc(r.servings+' '+(r.yieldUnit||'servings'))}${r.minutes?' · '+r.minutes+' minutes':''}</p><h3>Ingredients</h3>${prepared.ingredients.map(i=>`<p class="idea-ingredient">${esc(K.ingredientText(i))}${i.substitution?'<br><small>'+esc(i.substitution)+'</small>':''}</p>`).join('')}<h3>Instructions</h3>${K.steps(prepared).map((s,n)=>`<div class="step"><span class="step-number">${n+1}</span><div>${esc(s)}</div></div>`).join('')}<p class="small">${esc(r.notes||'')}</p><p class="small source-paragraph">${esc(r.source||'')}</p>`+button('Save to my recipes','catalog-save','primary')+button('Back to results','uc-back','quiet'));
 $('#modal').classList.add('cookbook-full');$('#modal').scrollTop=0;
 }catch(error){if(ticket===request&&$('#modal').open)modal('<h2>Recipe could not load</h2><p>Check your connection and open this recipe again.</p>'+button('Back to results','uc-back','quiet'));}}
document.addEventListener('click',e=>{const b=e.target.closest('[data-action="catalog-save"]');if(!b||!active)return;e.preventDefault();e.stopImmediatePropagation();saveLibrary([structuredClone(active)]);},true);
$('#modal').addEventListener('close',()=>{request++;active=null;});
window.RecipeCatalog={open,get count(){return entries.length;}};
const notice=document.createElement('p');notice.className='public-edition-notice';notice.textContent='Loading the recipe collection…';document.body.append(notice);
fetch('catalog/index.json').then(r=>{if(!r.ok)throw Error('Collection download failed');return r.json();}).then(data=>{entries=data.map(([id,title,description,category,minutes,servings,yieldUnit,country,cuisineTags,ingredients,method,chunk,sourceWording])=>({id,title,kind:'Collection',chunk,fingerprint:'catalog:'+id,search:title+' '+ingredients.map(i=>i[0]).join(' '),recipe:{id,title,description,category,minutes,servings,yieldUnit,country,cuisineTags,ingredients:ingredients.map(([name,amount])=>({name,amount})),steps:[method],sourceWording}}));CookbookExperience.invalidate();render();notice.remove();}).catch(()=>{notice.textContent='The additional recipe collection could not load. Check your connection and reload to retry.';});
})();
