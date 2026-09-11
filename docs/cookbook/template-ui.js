(function(){'use strict';
const earlier=activeRecipe,cache=new WeakMap();
function prepared(r){if(!r||typeof r!=='object')return r;if(!cache.has(r))cache.set(r,RecipeTemplate.prepare(r));return cache.get(r);}
activeRecipe=function(){return prepared(earlier());};
// Catalog recipe views and save previews use the same measured presentation.
for(const list of [window.WORLD_RECIPES,window.CENTRAL_AMERICAN_RECIPES,window.EASY_WEB_RECIPES,window.SOUTHERN_RECIPES,window.LIBRARY_500,window.TAILORED_RECIPES].filter(Array.isArray))for(const e of list)if(e.recipe)e.recipe=prepared(e.recipe);
// Actual collection names are kept explicit rather than changing saved user state.
for(const list of [typeof library500!=='undefined'?library500:[],typeof tailoredEntries!=='undefined'?tailoredEntries:[]])for(const e of list)if(e.recipe)e.recipe=prepared(e.recipe);
const oldAll=allEntries;allEntries=function(){return oldAll().map(e=>e.kind==='Recovered originals'?e:{...e,recipe:prepared(e.recipe)});};
const oldCollect=collectDraft;
collectDraft=function(strict=false){const r=oldCollect(strict),saved=state.recipes.find(x=>x.id===r.id);if(saved&&(JSON.stringify(saved.ingredients)!==JSON.stringify(r.ingredients)||JSON.stringify(saved.steps)!==JSON.stringify(r.steps))){r.dietaryTags=[];delete r.totalMinutes;}else if(saved&&saved.minutes!==r.minutes)delete r.totalMinutes;return r;};
render();
})();
