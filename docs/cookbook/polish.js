/* SavorShelf 0.4 — presentation, editable version names and keyless-creator handoff. */
'use strict';
const V=window.RecipeVersions;
const shellBeforePolish=shell;
shell=content=>shellBeforePolish(content)
 .replace(`<span class="brand-mark">${icon('chef')}</span>SavorShelf`,`<span class="brand-mark"><img class="brand-logo" src="icon.svg" alt=""></span><span class="brand-word">SavorShelf</span>`)
 .replace('On this device · 0.16.0','Saved on device');
const optionsBeforePolish=optionsPanel;
optionsPanel=(r,base)=>{
 let html=optionsBeforePolish(r,base);
 const chosen=choice(base),variantId=chosen.variant||'original';
 // Keep immutable dietary meanings visible beside any personal name.
 for(const [mode,label] of Object.entries(V.adaptationLabels)){
  const key='adaptation:'+variantId+':'+mode,custom=base.versionNames?.[key];
  if(custom)html=html.replace(new RegExp('(<option value="'+mode+'"[^>]*>)[^<]*(</option>)'),(_m,a,b)=>a+esc(custom+' · '+label)+b);
 }
 const dietary=[chosen.dairy,chosen.sugar].filter(mode=>V.adaptationLabels[mode]).map(mode=>{
  const key='adaptation:'+variantId+':'+mode;return base.versionNames?.[key]?esc(base.versionNames[key]+' · '+V.adaptationLabels[mode]):esc(V.adaptationLabels[mode]);
 });
 html=html.replace('<div class="variant-grid">',`<div class="current-version"><span class="small">Recipe version</span><strong>${esc(V.name(base,choice(base).variant&&choice(base).variant!=='original'?'variant:'+choice(base).variant:'original'))}</strong>${dietary.map(label=>`<span class="small">${label}</span>`).join('')}</div><div class="variant-grid">`);
 return html.replace('<h2>Make it your way</h2>',`<div class="version-heading"><h2>Make it your way</h2>${button(icon('edit')+'Rename versions','version-names','soft')}</div>`);
};
const collectBeforePolish=collectDraft;
collectDraft=(strict=false)=>{
 const r=collectBeforePolish(strict),saved=state.recipes.find(x=>x.id===r.id);
 if(saved&&r.versionNote!==saved.versionNote){
  r.versionNames={...(r.versionNames||{})};
  if(r.versionNote.trim())r.versionNames.original=r.versionNote.trim();else delete r.versionNames.original;
 }
 return r;
};
function versionNamesModal(){
 const r=current();if(!r)return;
 modal(`<h2>Name your versions</h2><p class="small">Use names such as “Sunday favorite,” “Coffee version” or “Less sweet.” Names do not change ingredients, dietary labels or recipe IDs.</p><div class="version-name-list">${V.entries(r).map((entry,n)=>`<label class="field version-name-row" for="version-name-${n}"><span class="small">${esc(entry.type)}</span><input id="version-name-${n}" data-version-key="${esc(entry.key)}" value="${esc(entry.name)}" maxlength="160" required autocomplete="off"></label>`).join('')}</div><p id="version-name-error" class="inline-error" role="status"></p><div class="dialog-actions">${button('Save names','save-version-names','primary')}${button('Cancel','close-modal')}</div>`);
}
function historyModal(){
 const r=current();modal(`<h2>Your saved versions</h2><p class="small">Restoring an earlier recipe keeps the current one in history. Your ratings, photos, pins and custom names stay with the card.</p>${button('Rename versions','version-names','soft')}${(r.history||[]).length?r.history.map((h,i)=>`<div class="history-item"><strong>${esc(V.name(r,V.historyKey(h)))}</strong><p class="small">${date(h.updatedAt)} · ${esc(h.notes?.slice(0,160)||'No extra notes.')}</p>${button('Make this current','restore','',`data-index="${i}"`)}</div>`).join(''):'<p>Edit and save this recipe to start its history.</p>'}<div class="dialog-actions">${button('Close','close-modal')}</div>`);
}
function creatorPageSettings(){
 modal(`<h2>Keyless recipe creator</h2><p>Puter can generate recipes through a small website without your own AI key or private server.</p><p class="small">The included <strong>puter-creator</strong> folder is ready to host on GitHub Pages or another HTTPS static host. The dedicated SavorShelf companion is published. You can use its address or another compatible HTTPS creator.</p><label class="field">Your hosted creator page<input id="creator-page-url" type="url" maxlength="1000" placeholder="https://yourname.github.io/savorshelf-creator/" value="${esc(state.creatorPageUrl||'')}"></label><p class="small">The page opens in your browser, where you sign in with Puter. Only the request and dietary choices you submit are shared. Puter has a limited free allowance; extra usage may cost money. Your saved library is not sent.</p><p id="creator-page-error" class="inline-error" role="status"></p><div class="dialog-actions">${button('Save page address','save-creator-page','primary')}${button('Remove address','remove-creator-page')}${button('Close','close-modal')}</div>`);
}
function creatorConsent(){
 keepCreationDraft();const text=T.prompt(makerPrompt,{servings:makerServings,dairy:makerDairy,sugar:makerSugar,avoid:makerAvoid});
 if(!state.creatorPageUrl){creatorPageSettings();return;}
 modal(`<h2>Create with Puter</h2><p>Your browser will open the creator page. Sign in to Puter there, generate a draft, then use <strong>Send to SavorShelf</strong> to review and save it.</p><p class="small">Only this request and its cooking preferences will be sent. Puter and its model provider process it. Their free allowance and usage charges apply. This is a browser handoff, not AI running inside the app.</p><details><summary>Review the request</summary><p class="notes">${esc(text)}</p></details><div class="dialog-actions">${button('Open creator page','open-creator-page','primary')}${button('Cancel','close-modal')}</div>`);
}
const creatorBeforePolish=creator;
creator=()=>creatorBeforePolish()
 .replace('<div class="maker-actions">',`<div class="maker-actions">${button('Create with Puter','puter-create','primary')}`)
 .replace('<strong>ChatGPT:</strong>','<strong>Puter:</strong> no developer API key or private server. A hosted creator page and your Puter sign-in are required. A browser handoff returns a draft for review.<br><strong>ChatGPT:</strong>');
const settingsBeforePolish=settings;
settings=()=>settingsBeforePolish()
 .replace('Fully in-app AI generation needs a private HTTPS server and a provider account.','The existing private-server connection remains optional. Puter is an alternative without your own API key or server.')
 .replace('Network access is used only when you deliberately use a configured AI connection.','Requests leave the app only when you deliberately use a configured AI connection or open an external creator.')
 +`<div class="settings-grid added-settings"><section class="panel"><h2>Keyless creator website</h2><p class="muted">Connect the included Puter recipe-creator page after hosting it. Open it from Create, sign in, and send a reviewed draft back to this same app.</p>${button('Set creator page address','creator-page-settings','primary')}<p class="small">${state.creatorPageUrl?'A page address is saved. It has not been tested with your account.':'Not connected. No page has been published or paid service activated.'}</p></section></div>`;
document.addEventListener('click',async e=>{
 const el=e.target.closest('[data-action]');if(!el)return;const a=el.dataset.action;
 if(!['version-names','save-version-names','history','restore','creator-page-settings','save-creator-page','remove-creator-page','puter-create','open-creator-page'].includes(a))return;
 e.preventDefault();e.stopImmediatePropagation();
 try{
  if(a==='version-names')versionNamesModal();
  else if(a==='save-version-names'){
   const r=current(),updates=Object.fromEntries([...document.querySelectorAll('[data-version-key]')].map(x=>[x.dataset.versionKey,x.value]));
   try{const renamed=V.renamed(r,updates);C.validRecipe(renamed);if(commit(s=>s.recipes[s.recipes.findIndex(x=>x.id===r.id)]=renamed)){closeModal();render();toast('Version names saved. Your recipes were not duplicated.');}}catch(err){$('#version-name-error').textContent=err.message;}
  }else if(a==='history')historyModal();
  else if(a==='restore'){
   const r=current(),n=Number(el.dataset.index),h=r.history?.[n];if(!h)return;
   const restoredName=V.name(r,V.historyKey(h)),currentName=V.name(r,'original');
   if(commit(s=>{const i=s.recipes.findIndex(x=>x.id===r.id),names={...(r.versionNames||{}),...(h.versionNames||{})};for(const [key,value] of Object.entries(r.versionNames||{}))if(key.startsWith('history:'))names[key]=value;names[V.historyKey(r)]=currentName;names.original=restoredName;
    s.recipes[i]={...structuredClone(h),id:r.id,versionNames:names,photo:r.photo,favorite:r.favorite,rating:r.rating||0,pinned:!!r.pinned,cookCount:r.cookCount||0,lastCookedAt:r.lastCookedAt,updatedAt:new Date().toISOString(),history:[snapshot(r),...r.history.filter((_,j)=>j!==n)].slice(0,20)};
    s.recipes[i]=V.renamed(s.recipes[i],{});s.checked=[];
   })){delete selectedChoices[r.id];closeModal();detailYield=current().servings;checkedIngredients.clear();render();toast('Earlier recipe restored. Your custom names were kept.');}
  }else if(a==='creator-page-settings')creatorPageSettings();
  else if(a==='save-creator-page'){
   try{const url=V.creatorURL($('#creator-page-url').value);if(commit(s=>s.creatorPageUrl=url)){closeModal();render();toast('Page address saved. No request has been sent.');}}catch(err){$('#creator-page-error').textContent=err.message;}
  }else if(a==='remove-creator-page'){if(commit(s=>delete s.creatorPageUrl)){closeModal();render();}}
  else if(a==='puter-create')creatorConsent();
  else if(a==='open-creator-page'){
   const base=V.creatorURL(state.creatorPageUrl),text=T.prompt(makerPrompt,{servings:makerServings,dairy:makerDairy,sugar:makerSugar,avoid:makerAvoid});
   const url=base+'#request='+encodeURIComponent(text);
   if(window.AndroidBridge?.openCreatorPage){const error=AndroidBridge.openCreatorPage(url);if(error)throw Error(error);}else window.open(url,'_blank','noopener,noreferrer');
   closeModal();
  }
 }catch(err){toast(err.message||'That change could not be saved.');}
},true);
// Consolidate separately-added settings groups into one grid for equal columns and spacing.
const renderBeforePolish=render;
render=()=>{
 renderBeforePolish();
 if(tab==='settings'&&view.type==='home'){
  const grids=[...document.querySelectorAll('.settings-grid')];if(grids.length){for(const extra of grids.slice(1)){grids[0].append(...extra.children);extra.remove();}}
 }
};
window.SavorShelf.versions=V;
render();
