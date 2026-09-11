/* Offline ingredient matching. Name matches are not quantity or allergy checks. */
(function(root){
 'use strict';
 const aliases={eggs:'egg',bananas:'banana',tomatoes:'tomato',potatoes:'potato',onions:'onion',cloves:'clove',oats:'oat',chickpeas:'chickpea',scallions:'spring onion',cilantro:'coriander',aubergine:'eggplant',courgette:'zucchini'};
 const normalize=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).map(w=>aliases[w]||w).join(' ');
 const has=(name,term)=>(' '+normalize(name)+' ').includes(' '+normalize(term)+' ');
 const terms=s=>[...new Set(String(s||'').slice(0,2000).split(/[,;\n]+/).map(normalize).filter(Boolean))].slice(0,60);
 const ingredients=r=>(r.ingredients||[]).filter(i=>i.amount!==0&&normalize(i.name)!=='omitted');
 const searchCache=new WeakMap();
 function matches(r,q){const raw=[r.title,r.description,r.notes,...ingredients(r).map(i=>i.name),...(r.variants||[]).map(v=>v.label),...Object.values(r.versionNames||{})].join(' ');let cached=searchCache.get(r);if(!cached||cached.raw!==raw){cached={raw,text:' '+normalize(raw)+' '};searchCache.set(r,cached);}return normalize(q).split(' ').filter(Boolean).every(w=>cached.text.includes(' '+w+' '));}

 function pantry(r,stock){const found=[],missing=[];for(const i of ingredients(r))(stock.some(t=>has(i.name,t))?found:missing).push(i.name);return {recipe:r,found,missing,score:found.length/(found.length+missing.length||1)};}
 function rank(recipes,input,onlyComplete=false){const stock=terms(input);if(!stock.length)return [];return recipes.map(r=>pantry(r,stock)).filter(m=>m.found.length&&(!onlyComplete||!m.missing.length)).sort((a,b)=>b.score-a.score||b.found.length-a.found.length||a.recipe.title.localeCompare(b.recipe.title));}
 function similar(recipe,recipes){const names=ingredients(recipe).map(i=>normalize(i.name));const tokens=new Set(names.flatMap(n=>n.split(' ')).filter(t=>t.length>2&&!['salt','water','oil','ground','fresh','dried','chopped','optional','unsalted'].includes(t)));return recipes.filter(r=>r.id!==recipe.id).map(r=>{const shared=ingredients(r).filter(i=>normalize(i.name).split(' ').some(t=>tokens.has(t))).map(i=>i.name);return {recipe:r,shared,score:shared.length/Math.max(ingredients(r).length,names.length,1)};}).filter(m=>m.shared.length>=2).sort((a,b)=>b.score-a.score||a.recipe.title.localeCompare(b.recipe.title)).slice(0,6);}
 const api={normalize,terms,matches,pantry,rank,similar};if(typeof module==='object'&&module.exports)module.exports=api;else root.RecipeDiscovery=api;
})(typeof window==='object'?window:globalThis);
