/* Shared visual structure for saved recipes and public collection previews. */
(function(){'use strict';
window.RecipePresentation={
 header(r,{category=r.category||'Other',facts='',extra=''}={}){return `<section class="recipe-header"><div class="recipe-header-art">${recipeArt(r,'detail-cover')}</div><div class="recipe-header-copy"><p class="eyebrow">${esc(category)}</p><h1>${esc(r.title)}</h1><p class="recipe-intro">${esc(r.description)}</p><div class="recipe-facts">${facts}</div>${extra}</div></section>`;},
 ingredients({progress='',control='',rows='',footer=''}={}){return `<section class="panel ingredients-panel"><div class="section-label"><h2>Ingredients</h2>${progress}</div>${control}<div id="ingredient-list">${rows}</div>${footer}</section>`;},
 method(r,servings=r.servings){return `<section class="panel method-panel"><div class="section-label"><h2>Method</h2><span class="small">${r.steps.length} steps</span></div>${K.steps(r,servings).map((s,n)=>`<div class="step"><span class="step-number">${n+1}</span><div>${esc(s)}</div></div>`).join('')}</section>`;}
};
})();
