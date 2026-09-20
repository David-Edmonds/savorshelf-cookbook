(function(root){'use strict';
const aliases={eggs:'egg',beans:'bean',onions:'onion',tomatoes:'tomato',potatoes:'potato',mushrooms:'mushroom',cloves:'clove',breasts:'breast'};
const norm=s=>String(s||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(' ').map(w=>aliases[w]||w).join(' ');
function quality(r){const flags=[];if(!r.minutes)flags.push('Time needed');if((r.ingredients||[]).some(i=>i.amount==null))flags.push('Check amounts');if(/placeholder/i.test(r.notes||''))flags.push('Confirm servings');if(!(r.steps||[]).length)flags.push('Instructions needed');return flags;}
function index(rows){return rows.map((e,i)=>({...e,key:String(i),fingerprint:e.fingerprint||(e.kind==='Recovered originals'?e.id:JSON.stringify([norm(e.recipe.title),e.recipe.servings,e.recipe.ingredients,e.recipe.steps])),text:norm(e.search+' '+[e.recipe.country,e.recipe.cuisine,e.recipe.regionalCuisine,...(e.recipe.ethnicCuisines||[]),...(e.recipe.cuisineTags||[])].filter(Boolean).join(' ')+' '+Object.values(e.recipe.versionNames||{}).join(' ')),flags:e.kind==='Recovered originals'?['Historical note']:quality(e.recipe)}));}
function totalMinutes(r){
 if(Number.isFinite(r.totalMinutes)&&r.totalMinutes>0)return r.totalMinutes;
 const notes=String(r.notes||'');
 if(/active preparation|active time|plus.*(?:hour|minute)|overnight|refrigerat|chill|marinat|rise|rising|soak/i.test(notes))return null;
 return Number.isFinite(r.minutes)&&r.minutes>0?r.minutes:null;
}
function facetsMatch(e,f={}){if(!Object.entries(f).some(([k,v])=>k!=='sort'&&v))return true;const r=e.recipe,ingredients=(r.ingredients||[]).filter(i=>i.amount!==0),names=ingredients.map(i=>norm(i.name)),steps=norm((r.steps||[]).join(' '));
 if(f.country&&norm(r.country)!==norm(f.country))return false;
 if(f.region&&norm(r.regionalCuisine)!==norm(f.region))return false;
 if(f.ethnicity&&!(r.ethnicCuisines||[]).some(x=>norm(x)===norm(f.ethnicity)))return false;
 if(f.diet&&!(r.dietaryTags||[]).includes(f.diet))return false;
 if(f.cuisine&&!norm([r.country,r.cuisine,...(r.cuisineTags||[])].filter(Boolean).join(' ')).includes(norm(f.cuisine)))return false;
 if(f.meal&&norm(r.category)!==norm(f.meal))return false;
 const duration=totalMinutes(r);
 if(f.time&&(!duration||duration>Number(f.time)))return false;
 const ranges={'under15':[0,15],'15to30':[15,30],'30to60':[30,60],'over60':[60,Infinity]};
 if(f.timeRange){const range=ranges[f.timeRange];if(range&&(!duration||duration<=range[0]||duration>range[1]))return false;}
 if(f.count&&ingredients.length>Number(f.count))return false;
 const groups={fish:/\b(fish|salmon|tuna|cod|tilapia|trout)\b/,beef:/\b(beef|steak|brisket)\b/,pork:/\b(pork|bacon|ham)\b/};
 if(f.ingredient&&!names.some(n=>groups[f.ingredient]?groups[f.ingredient].test(n):(' '+n+' ').includes(' '+norm(f.ingredient)+' ')))return false;
 if(f.exclude&&f.exclude.split(/[,;\n]/).map(norm).filter(Boolean).some(t=>names.some(n=>(' '+n+' ').includes(' '+t+' '))))return false;
 const methods={'Oven':/\b(bake|roast|oven)\b/,'Air fryer':/\bair fry/,'Stovetop':/\b(skillet|stovetop|simmer|saucepan|saute)\b/,'Slow cooker':/\b(slow cooker|crockpot)\b/,'Grill':/\bgrill/};
 if(f.method&&methods[f.method]&&!methods[f.method].test(steps))return false;
 if(f.review==='recorded'&&e.flags.length)return false;
 return true;
}
function select(rows,query='',filter='All',stock='',facets={}){
 const terms=norm(query).split(' ').filter(Boolean),have=stock.split(/[,;\n]/).map(norm).filter(Boolean);
 const matching=rows.filter(e=> (filter==='Notes'?e.kind==='Recovered originals':e.kind!=='Recovered originals')&&(filter!=='Saved'||e.kind==='Saved')&&(filter!=='Southern'||e.kind==='Southern & Lowcountry')&&(filter!=='Quick'||(e.recipe.minutes>0&&e.recipe.minutes<=30&&!/chill|overnight/i.test(e.recipe.notes||'')))&&terms.every(t=>e.text.includes(t))&&(filter==='Notes'||facetsMatch(e,facets)));
 const ranked=matching.map(e=>{const ingredients=(e.recipe.ingredients||[]).filter(i=>i.amount!==0);const hits=have.length?ingredients.filter(i=>have.some(t=>(' '+norm(i.name)+' ').includes(' '+t+' '))).length:0;return {entry:e,hits,missing:ingredients.length-hits,score:hits/(ingredients.length||1)};}).filter(r=>!have.length||r.hits>0);
 ranked.sort((a,b)=>(have.length?b.score-a.score:0)||a.entry.flags.length-b.entry.flags.length||(a.entry.kind==='Saved'?-1:0)-(b.entry.kind==='Saved'?-1:0)||a.entry.title.localeCompare(b.entry.title));
 if(facets.sort==='time')ranked.sort((a,b)=>(totalMinutes(a.entry.recipe)||Infinity)-(totalMinutes(b.entry.recipe)||Infinity));
 if(facets.sort==='name')ranked.sort((a,b)=>a.entry.title.localeCompare(b.entry.title));
 // Hide only identical title/formula duplicates in search; never merge stored versions.
 const seen=new Set();return ranked.filter(x=>{const k=x.entry.fingerprint;if(seen.has(k))return false;seen.add(k);return true;});
}
const api={norm,quality,index,select,facetsMatch,totalMinutes};if(typeof module==='object'&&module.exports)module.exports=api;else root.CookbookIndex=api;
})(globalThis);
