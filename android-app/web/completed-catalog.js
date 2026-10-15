/* Only evidenced completed additions enter discovery. Never filters or mutates saved storage. */
(function(){'use strict';
const completed=new Set((window.ENRICHED_RECIPES||[]).map(e=>e.recipe.id));
const previous=allEntries;
allEntries=function(){return previous().filter(e=>e.kind==='Saved'||completed.has(e.recipe.id));};
// Superseded browsing routes lead to the same cookbook; personal version history is untouched.
const browse=()=>{closeModal();navigate('recipes');};
allRecipes=browse;originalsList=browse;readOriginal=browse;
libraryBrowse=browse;easywebBrowse=browse;southernBrowse=browse;
const priorHome=home,priorSettings=settings;
function clean(html){const wrapper=document.createElement('div');wrapper.innerHTML=html;
 for(const button of wrapper.querySelectorAll('[data-action="browse-originals"],[data-action="all-browse"],[data-action="library-browse"],[data-action="easyweb-browse"],[data-action="southern-browse"]')){
  const panel=button.closest('section.panel');if(panel&&!panel.querySelector('[data-action="export-originals"]'))panel.remove();else button.remove();
 }
 // There is no pending-recipe collection or review-state filter.
 wrapper.querySelectorAll('[data-cookbook-facet="review"]').forEach(el=>el.closest('label').remove());
 return wrapper.innerHTML;
}
home=()=>clean(priorHome());settings=()=>clean(priorSettings());
window.CompletedCatalog={ids:Object.freeze([...completed]),isCompleted:id=>completed.has(id)};
window.CookbookExperience?.invalidate();render();
})();
