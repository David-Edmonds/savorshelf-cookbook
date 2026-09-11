/* Completeness checks only; never invent or rewrite cooking quantities. */
(function(root){'use strict';
function inspect(r){const issues=[],ingredients=r.ingredients||[],steps=r.steps||[];
 if(!(Number(r.servings)>0))issues.push('Add a serving yield.');
 if(!(Number(r.minutes)>0))issues.push('Add the total time.');
 if(!ingredients.length)issues.push('Add an ingredient list.');
 const missing=ingredients.filter(i=>i.amount==null&&!/to taste|as needed/i.test(i.name+' '+(i.unit||'')));
 if(missing.length)issues.push('Check amounts: '+missing.map(i=>i.name).join(', ')+'.');
 if(!steps.length)issues.push('Add cooking instructions.');
 const keys=new Set(ingredients.map(i=>i.key).filter(Boolean));
 const refs=steps.join(' ').matchAll(/\{\{([a-z0-9_-]+)(?:\|[\d.]+)?\}\}/gi);
 for(const ref of refs)if(!keys.has(ref[1]))issues.push('Repair an ingredient link: '+ref[1]+'.');
 const plainAmounts=steps.some(s=>/\b\d+(?:[./]\d+)?\s*(?:cups?|tbsp|tsp|tablespoons?|teaspoons?|grams?|ounces?|oz|ml|pounds?|lbs?)\b/i.test(s));
 return {issues:[...new Set(issues)],plainAmounts};
}
const api={inspect};if(typeof module==='object'&&module.exports)module.exports=api;else root.RecipeReview=api;
})(globalThis);
