/* Review-driven adoption: stable recipe identity, reversible previous formulation. */
(function(root){'use strict';
const copy=x=>structuredClone(x);
function target(recipes,entry){return recipes.find(r=>r.id===entry.sourceId)||recipes.find(r=>r.culinaryGuidance?.originalId===entry.sourceId);}
function adopt(recipes,entry,label,now=new Date().toISOString()){
 const old=target(recipes,entry),r=copy(entry.recipe);label=String(label||'Suggested measured version').trim();if(!label||label.length>160)throw Error('Use a version name of 1–160 characters.');
 r.id=old?.id||entry.sourceId;r.versionNames={...r.versionNames,original:label};r.baseLabel=label;r.versionNote=label;r.updatedAt=now;
 if(old?.variants?.length)r.variants=copy(old.variants);
 const signature=x=>JSON.stringify([x.servings,x.ingredients,x.steps,x.adaptations,x.variants]);
 if(old&&signature(old)===signature(r))return {recipes:copy(recipes),id:old.id,unchanged:true};
 if(old){
  if((old.history||[]).length>=20)throw Error('This recipe already has 20 earlier versions. Export a backup and remove an unwanted version before applying this suggestion.');
  const previous=copy(old);delete previous.history;
  r.history=[previous,...copy(old.history||[])];
  for(const key of ['photo','rating','favorite','pinned','cookCount','lastCookedAt','cookingSettings','pan','familyKey'])if(Object.hasOwn(old,key))r[key]=copy(old[key]);
  // Retain user-named variations; suggestion variants remain available in the previous source.
  if(old.variants?.length)r.variants=copy(old.variants);
  for(const [k,v] of Object.entries(old.versionNames||{}))if(k!=='original')r.versionNames[k]=v;
  delete r.preferredChoice;
 }else if(recipes.length>=2000)throw Error('The collection limit is 2,000 recipes.');
 const out=copy(recipes),index=out.findIndex(x=>x.id===r.id);if(index<0)out.push(r);else out[index]=r;
 return {recipes:out,id:r.id,unchanged:false};
}
const api={target,adopt};if(typeof module!=='undefined')module.exports=api;else root.CulinarySave=api;
})(globalThis);
