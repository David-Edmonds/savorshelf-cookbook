/* Role-aware suggested dietary formulations. Existing authored adaptations are retained. */
(function(root){'use strict';
function diets(r){
 const lactose={},dairy={},sugar={};let complex=false,sweetBlocked=false;
 const title=r.title.toLowerCase(),method=r.steps.join(' ').toLowerCase();
 const starchSet=r.ingredients.some(i=>/corn.?starch|cornflour|semolina|rice|tapioca|custard powder/i.test(i.name));
 for(const i of r.ingredients){
  const n=i.name.toLowerCase(),plant=/dairy.free|plant.based|(?:soy|oat|almond|coconut|rice|cashew) (?:milk|cream|yogurt)|peanut butter|cocoa butter|cream of tartar|butter beans|butter lettuce/.test(n);
  const milk=/\bmilk\b|\bcream\b|\bcheese\b|butter\b|ghee|yog[uh]rt|kefir|buttermilk|margarine|whey|casein|queso|paneer|mascarpone|ricotta|parmesan|mozzarella|cheddar|feta|chocolate|custard|leche poleada|sherbet|white sauce|pesto/i.test(n);
  if(milk&&!plant){
   lactose[i.key]={name:'Lactose-free '+i.name+' (matching product; check label)',substitution:'Use the labeled lactose-free equivalent with the same fat level, thickness and cooking role. This may still contain milk proteins.'};
   let alt=null;
   if(/chocolate/.test(n)&&!/cocoa powder|unsweetened cocoa/.test(n))alt='Dairy-free '+i.name+' (same cocoa percentage and form)';
   else if(/ice cream|sherbet/.test(n))alt='Dairy-free frozen dessert (same flavor and texture)';
   else if(/condensed.*soup|cream of.*soup/.test(n))alt='Dairy-free condensed '+i.name+' (same concentration)';
   else if(/butter|ghee|margarine/.test(n)&&!/buttermilk/.test(n))alt='Firm dairy-free baking butter (similar fat content)';
   else if(/sour cream|cr[eè]me fra[iî]che/.test(n))alt='Unsweetened cultured plant sour cream';
   else if(/yog[uh]rt|kefir|buttermilk/.test(n))alt='Unsweetened cultured soy '+(/buttermilk|kefir/.test(n)?'drink (match acidity and thickness)':'yogurt');
   else if(/condensed milk/.test(n))alt=null;
   else if(/milk/.test(n)&&!/powder|evaporated/.test(n))alt='Unsweetened soy milk';
   else if(/cream/.test(n)&&!/cheese|custard/.test(n))alt=/whip|stiff peak/.test(method)?'Dairy-free cream labeled for whipping':'Unsweetened plant cooking cream (similar fat content)';
   else if(/cheese|queso|parmesan|cheddar|mozzarella|feta/.test(n)&&/garnish|topping|sprinkl|sandwich|pizza|pasta|gratin|quesadilla/.test(n+' '+title))alt='Dairy-free '+i.name+' (product intended for the same melting or garnish use)';
   const delicate=/cheesecake|flan|leches|creme caramel|cr[eè]me br[uû]l[eé]e/.test(title)||(/custard|pudding/.test(title)&&!starchSet);
   if(alt&&!delicate)dairy[i.key]={name:alt,substitution:'Match the stated amount and product role; flavor, richness and setting may differ. Check every component for dairy.'};else complex=true;
  }
  const sweet=/sugar|honey|syrup|molasses|jaggery|jam|jelly|sweetened|chocolate|marshmallow|sherbet|ice cream|custard|leche poleada/.test(n)&&!/unsweetened|no.added.sugar/.test(n);
  if(sweet){
   // Omission is restricted to optional finishing sweeteners or drink/savory seasoning.
   const plain=/^(?:white |granulated |brown )?sugar\b|^honey\b|^maple syrup\b/.test(n);
   const optional=/optional/.test(n)&&/topping|serving|sugar/.test(n);
   const seasoning=/coffee|chai|tea\b|lemonade|tomato soup/.test(title)&&!/dalgona/.test(title);
   if(plain&&(optional||seasoning))sugar[i.key]=null;else sweetBlocked=true;
  }
 }
 const prior=r.adaptations||{},note='New suggested formulation, not kitchen-tested. Match quantities and check every packaged ingredient, including breads, sauces and chocolate. ';
 const proposed={regularDairy:{supported:true,note:'Keep the retained dairy or non-dairy formulation.'},lactoseFree:{supported:true,replace:lactose,note:note+'Lactose-free dairy still contains milk proteins.'},dairyFree:{supported:!complex,replace:complex?{}:dairy,note:complex?'A reliable dairy-free setting or composite product is not established for this formulation. Retain the base or use a separately developed recipe.':note+(starchSet?'Keep the starch amount; simmer gently until it thickens and judge doneness by texture. ':'' )+'Use products intended for the stated cooking/whipping role.'},noAddedSugar:{supported:!sweetBlocked,replace:sweetBlocked?{}:sugar,note:note+'Omit only the listed optional/drink sweeteners. Use unsweetened packaged ingredients. Natural sugars may remain; this is not sugar-free.'},sugarFree:{supported:false,note:'A zero-sugar formulation is not established; no-added-sugar is different.'}};
 // Preserve developed historical formulas; replace old unsupported placeholders only.
 for(const [key,a] of Object.entries(prior))if(a.supported!==false)proposed[key]=a;
 // Additional role-specific formulations. Fruit and milk sugars remain.
 const omitFamilies=/baked oatmeal|yogurt & oat bowls|Southern stovetop rice pudding|vanilla grits pudding/.test(r.title);
 if(omitFamilies){
  const replace={};for(const i of r.ingredients)if(/^(?:brown )?sugar$|^sugar for topping$|^honey$/i.test(i.name))replace[i.key]=null;
  proposed.noAddedSugar={supported:true,replace,note:note+'Omit the listed sugar or honey. Oats, rice or grits provide the body; fruit provides natural sweetness. Keep all cooking liquid and starch. The result is less sweet and may brown less. Use unsweetened milk/yogurt and fruit without added sugar; this is not sugar-free.'};
 }
 if(/Southern chicken salad/.test(r.title))proposed.noAddedSugar={supported:true,replace:{relish:{name:'Dill pickle relish with no added sugar',substitution:'Use the same volume, drained; this gives a tangier dressing.'}},note:note+'Replace sweet relish with no-added-sugar dill relish. Choose mayonnaise, mustard and seasoning without added sugar; natural sugars remain.'};
 if(/pimento cheese spread/.test(r.title))proposed.dairyFree={supported:true,replace:{cheese:{name:'Dairy-free cheddar-style block, freshly grated'},creamcheese:{name:'Plain dairy-free cream-cheese-style spread'}},note:note+'This is a cold spread, so the substitutes do not need to melt or set a baked custard. Use the same weights, soften the spread, then fold in the grated block. Check mayonnaise and every flavoring for dairy. Texture and saltiness differ.'};
 // Butter beans and butter lettuce are vegetables, not dairy products.
 for(const i of r.ingredients)if(/\bbutter (?:beans|lettuce)\b/i.test(i.name))for(const k of ['lactoseFree','dairyFree'])delete proposed[k].replace?.[i.key];
 r.adaptations=proposed;
}
if(typeof module!=='undefined')module.exports=diets;else root.CulinaryDiets=diets;
})(globalThis);
