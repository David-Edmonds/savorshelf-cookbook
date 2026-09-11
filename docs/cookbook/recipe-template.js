/* Measured presentation and conservative substitution guidance, not a data migration. */
(function(root){'use strict';
const node=typeof module==='object'&&module.exports,T=node?require('./transfer.js'):root.RecipeTransfer;
function substitute(i){if(i.substitution?.trim())return i.substitution;const name=String(i.name||'').toLowerCase();
 if(/loroco/.test(name))return 'Loroco has no close flavor equivalent. Use food-grade frozen loroco if fresh is unavailable. Omit it for a cheese-only version; that changes the dish.';
 if(/quesillo/.test(name))return 'Use the same weight of low-moisture mozzarella for melting; it will be milder and less tangy than Salvadoran quesillo.';
 if(/chipil[ií]n/.test(name))return 'Use food-grade chipilín where possible. The same weight of chopped spinach replaces the leafy bulk, but not the distinctive flavor; label this as an adaptation.';
 if(/miltomate/.test(name))return 'Use the same weight of husked tomatillos. The acidity can differ; taste the finished sauce before adjusting.';
 if(/pepitoria/.test(name))return 'Use the same weight of unsalted, hulled pumpkin seeds. Toast as directed; this does not replace sesame if both are listed.';
 if(/chile guaque/.test(name))return 'Use the same weight of stemmed and seeded dried guajillo chile as a practical adaptation. Flavor and heat differ.';
 if(/chile pasa/.test(name))return 'Use the same weight of stemmed and seeded dried ancho chile as a practical adaptation; flavor will differ.';
 if(/chile cobanero/.test(name))return 'There is no exact substitute. Start with one-quarter of the listed amount of cayenne, then adjust; its heat and smoky flavor differ.';
 if(/panela|piloncillo|rapadura/.test(name))return 'Use the same weight of dark brown sugar. It dissolves more readily and has a different molasses flavor.';
 if(/masa harina/.test(name))return 'Use nixtamalized corn masa harina intended for tortillas. Plain cornmeal, cornstarch and precooked arepa flour are not direct replacements.';
 if(/banana lea(?:f|ves)|corn husks/.test(name))return 'For steaming, use food-safe parchment with foil outside it; the leaf aroma is lost. Keep foil away from direct microwave use.';
 if(/^(?:salvadoran )?crema$/.test(name))return 'Use the same weight of sour cream as a practical alternative. It is thicker and tangier; warm gently to avoid splitting.';
 if(/^queso fresco$/.test(name))return 'Use the same weight of mild, firm fresh farmer cheese. Saltiness and crumbliness differ; this is not a substitute for melting quesillo.';
 if(/^whole milk$/.test(name))return 'For a less rich version, use the same volume of 2% milk. Plant milks behave differently in custards and baking and need a recipe-specific adjustment.';
 if(/^white wine$/.test(name))return 'For an alcohol-free savory adaptation, replace each 120 ml wine with 110 ml unsalted stock plus 10 ml lemon juice. Flavor changes.';
 if(/^chayote$|^g[üu]isquil$/.test(name))return 'Chayote and güisquil are names for the same vegetable. Use the same weight; neither is a substitute for its root, ichintal.';
 if(/seedless tamarind pulp/.test(name))return 'Use the same weight of unsweetened tamarind pulp sold without seeds. Concentrated paste is stronger and cannot be swapped in at the same amount.';
 if(/food-grade morro seeds/.test(name))return 'Morro gives Salvadoran horchata its characteristic flavor. Use food-grade morro sold for drinks; seed mixes without it make a different style of horchata.';
 if(/^fresh cilantro|^cilantro/.test(name))return 'Use the same amount of flat-leaf parsley only if necessary; it replaces the herb bulk, not cilantro flavor.';
 if(/^scallions|^green onions/.test(name))return 'Scallions and green onions are interchangeable in the same amount.';
 if(/^unsalted butter$/.test(name))return 'The same weight of salted butter can work; reduce separately added salt to taste. Baking behavior otherwise stays similar.';
 if(/^olive oil$|^vegetable oil$|^canola oil$/.test(name))return 'Use the same volume of another neutral cooking oil suitable for the stated temperature. Flavor changes with unrefined oils.';
 return '';
}
function prepare(recipe){const r={...recipe,ingredients:(recipe.ingredients||[]).map(i=>({...i,substitution:substitute(i)})),steps:[...(recipe.steps||[])]};
 if(!r.ingredients.length||!r.steps.length)return r;
 T.linkAmounts(r);const used=new Set(r.steps.flatMap(s=>[...s.matchAll(/\{\{([\w-]+)/g)].map(m=>m[1])));
 const unlinked=r.ingredients.filter(i=>Number.isFinite(i.amount)&&i.amount>0&&i.key&&!used.has(i.key));
 if(unlinked.length)r.steps.unshift('Before cooking, measure and set out '+unlinked.map(i=>'{{'+i.key+'}}').join('; ')+'. These are total recipe quantities, not extra additions. Follow any divided amounts in the method.');
 return r;
}
const api={prepare,substitute};if(node)module.exports=api;else root.RecipeTemplate=api;
})(globalThis);
