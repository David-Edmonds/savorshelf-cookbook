/* Display-only descriptions and honest image fallbacks. Stored recipes are not changed. */
(function(){'use strict';
const desc=window.RECIPE_ENGLISH_DESCRIPTIONS||{};
function describe(r){if(desc[r.id])return desc[r.id];if(r.description&&r.description.trim()&&!/^(Imported recipe draft|Traditional dish|.*Wikibooks community recipe)/i.test(r.description))return r.description;const names=(r.ingredients||[]).filter(i=>!/^water|salt|pepper|oil$/i.test(i.name)).slice(0,3).map(i=>i.name);return names.length?'A '+String(r.category||'cooking').toLowerCase()+' recipe featuring '+names.join(', ')+'. Follow the measured ingredients and method below.':'A saved cooking recipe. Review its ingredient list and instructions before preparing it.';}
function decorate(r){return {...r,description:describe(r)};}
for(const list of [window.WORLD_RECIPES,window.CENTRAL_AMERICAN_RECIPES,window.EASY_WEB_RECIPES].filter(Array.isArray))for(const e of list)e.recipe=decorate(e.recipe);
const previous=allEntries;allEntries=function(){return previous().map(e=>({...e,recipe:e.kind==='Recovered originals'?{...e.recipe,description:'An archived recipe or cooking note. Historical text may be incomplete and does not scale automatically.'}:decorate(e.recipe)}));};
const previousActive=activeRecipe;activeRecipe=function(){const r=previousActive();return r?decorate(r):r;};
const priorArt=recipeArt;
const formula=r=>JSON.stringify([r.title,(r.ingredients||[]).map(i=>[i.amount,i.unit,i.name])]);
const imageBaselines=new Map();
const candidates=[...(window.STARTER_RECIPES||[]),...(window.RECOVERED_RECIPE_PACK?.recipes||[]),...(window.CENTRAL_AMERICAN_RECIPES||[]).map(e=>e.recipe),...(window.WORLD_RECIPES||[]).map(e=>e.recipe)];
for(const r of candidates){const p=RecipePhotos.resolve(r);if(p?.kind==='generated'){if(!imageBaselines.has(p.recipeId))imageBaselines.set(p.recipeId,new Set());imageBaselines.get(p.recipeId).add(formula(r));}}

recipeArt=function(r,cls=''){
 if(r.photo)return priorArt(r,cls);
 // The bundled images were visually reviewed as dish illustrations, not photographs of a tested cook.
 const photo=RecipePhotos.resolve(r);
 if(photo?.kind==='generated'&&imageBaselines.get(photo.recipeId)?.has(formula(r)))return priorArt(r,cls);
 return `<div class="cover recipe-photo-pending ${esc(cls)}" role="img" aria-label="No verified dish photo for ${esc(r.title)}"><span class="photo-pending-mark" aria-hidden="true">${icon('book')}</span><span>Recipe photo needed</span><small>No unrelated food image shown</small></div>`;
};
window.RecipeContentQuality={describe,decorate};window.CookbookExperience?.invalidate();render();
})();
