/* Source-backed, read-only cuisine decoration. Personal records stay unchanged. */
(function(){'use strict';
const previous=allEntries;
allEntries=function(){return [...previous(),...[...(window.WORLD_RECIPES||[]),...(window.CENTRAL_AMERICAN_RECIPES||[])].map(e=>({id:e.recipe.id,title:e.recipe.title,kind:'International recipes',recipe:e.recipe,search:[e.recipe.title,...e.recipe.ingredients.map(i=>i.name)].join(' ')}))].map(e=>{
 let tags=null;const source=e.recipe.source||'';const url=source.match(/https:\/\/en\.wikibooks\.org\/wiki\/[^\s|]+/)?.[0];if(url)tags=window.CUISINE_METADATA?.[url];
 if(e.kind==='Southern & Lowcountry')tags={country:'United States',cuisine:'Southern American',regionalCuisine:'Southern / Lowcountry',cuisineTags:['Southern','Lowcountry','South Carolina','Charleston'],cuisineLabelBasis:'Existing Southern-inspired collection; untested drafts'};
 if(!tags)return e;return {...e,recipe:{...tags,...e.recipe,cuisineTags:e.recipe.cuisineTags||tags.cuisineTags}};
 });};
})();
