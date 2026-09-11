/* Private offline source archive. Never include in the public companion. */
'use strict';
const sourceArchive=window.CHATGPT_RECIPE_ORIGINALS;
let recoveredImportProblem='';
if(!storageProblem&&!state.recoveredChatGPTPackVersion){
 try{
  const deleted=new Set(state.deletedBundledIds||[]);
  const incoming=window.RECOVERED_RECIPE_PACK.recipes.filter(r=>!deleted.has(r.id));
  const merged=T.merge(state.recipes,incoming);
  if(!commit(s=>{s.recipes=merged.recipes;s.recoveredChatGPTPackVersion=1;if(!s.creatorPageUrl)s.creatorPageUrl='https://david-edmonds.github.io/savorshelf-creator/';}))recoveredImportProblem='Saving recovered recipe cards failed. Your source originals are still available below.';
 }catch(error){recoveredImportProblem='Recovered cards were not merged: '+error.message;}
}
const settingsBeforeOriginals=settings;
settings=()=>settingsBeforeOriginals()+`<div class="settings-grid added-settings"><section class="panel"><h2>Your ChatGPT recipe originals</h2><p>${sourceArchive.entries.length} recipe and cooking-note entries recovered from ${sourceArchive.conversationCount} conversations. Earlier recipes and corrections are preserved separately from your rated shelf.</p>${button('Browse recipe originals','browse-originals','primary')}${button('Export recipe originals','export-originals')}<p class="small">Includes cooking text recovered from your September 2026 export. Images, attachments and absent or deleted history are not reconstructed. Original text does not scale automatically and may contain outdated advice.</p></section></div>`;
const homeBeforeOriginals=home;
home=()=>homeBeforeOriginals()+`<section class="panel"><h2>Recipes from your ChatGPT history</h2><p class="small">Search original recipes, earlier versions and cooking notes without changing your saved recipes.</p>${button('Browse '+sourceArchive.entries.length+' originals','browse-originals','soft')}</section>`;
function originalsList(){
 modal(`<h2>Your recipe originals</h2><p class="small">Historical recipes and notes, not verified cooking or dietary guidance. Ten fully structured original versions were prepared for the shelf; all other recovered text remains here without invented quantities. Nothing is sent to an AI provider.</p>${recoveredImportProblem?`<p class="error">${esc(recoveredImportProblem)}</p>`:''}<label class="field">Search recipe originals<input id="originals-search" type="search" placeholder="Pancakes, chicken, coffee…"></label><div id="originals-results"></div>${button('Close','close-modal')}`);
 filterOriginals('');
}
function filterOriginals(q){
 const query=q.toLocaleLowerCase().trim();
 const matches=sourceArchive.entries.filter(e=>(e.title+' '+e.text+' '+e.sources[0].chatTitle).toLocaleLowerCase().includes(query));
 $('#originals-results').innerHTML=`<p class="small">${matches.length} matches. Showing up to 60; narrow your search for more.</p>`+matches.slice(0,60).map(e=>`<div class="history-item">${recipeArt(e,'idea-cover')}<strong>${esc(e.title)}</strong><p class="small">${esc(e.sources[0].chatTitle)} · ${esc(e.date)}</p>${button('Read original','read-original','',`data-source-id="${esc(e.id)}"`)}</div>`).join('');
}
function readOriginal(id){
 const entry=sourceArchive.entries.find(e=>e.id===id);if(!entry)return;
 modal(`${recipeArt(entry,'idea-cover')}<h2>${esc(entry.title)}</h2><p class="small">${esc(entry.sources[0].chatTitle)} · ${esc(entry.date)}. Recovered historical text; not kitchen-tested. Amount ranges are preserved. Do not rely on historical color-based meat checks or dietary safety claims.</p><div class="original-recipe-text">${esc(entry.text)}</div><div class="maker-actions">${button('Copy original text','copy-original','',`data-source-id="${esc(id)}"`)}${button('Format as a recipe','format-original','primary',`data-source-id="${esc(id)}"`)}${button('Back to originals','browse-originals')}${button('Close','close-modal')}</div>`);
}
document.addEventListener('input',e=>{if(e.target.id==='originals-search')filterOriginals(e.target.value);});
document.addEventListener('click',async e=>{
 const b=e.target.closest('[data-action]');if(!b)return;
 if(!['browse-originals','read-original','export-originals','copy-original'].includes(b.dataset.action))return;
 e.preventDefault();e.stopImmediatePropagation();
 if(b.dataset.action==='browse-originals')originalsList();
 if(b.dataset.action==='read-original')readOriginal(b.dataset.sourceId);
 if(b.dataset.action==='export-originals')exportText('SavorShelf-ChatGPT-originals.json',JSON.stringify(sourceArchive,null,2),'application/json');
 if(b.dataset.action==='copy-original'){
  const entry=sourceArchive.entries.find(x=>x.id===b.dataset.sourceId);
  try{await navigator.clipboard.writeText(entry.text);toast('Original text copied.');}catch(_){toast('Clipboard unavailable. Export your originals from Settings.');}
 }
},true);
render();

document.addEventListener('click',e=>{const b=e.target.closest('[data-action="format-original"]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();const entry=sourceArchive.entries.find(x=>x.id===b.dataset.sourceId);if(entry){try{showImportPreview(entry.text);}catch(err){transferModal(entry.text);const message=document.querySelector('#transfer-error');if(message)message.textContent=err.message;}}},true);
