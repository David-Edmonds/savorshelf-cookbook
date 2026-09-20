/* NIST household equivalents; never convert volume to mass or infer a cup standard. */
(function(root){'use strict';
const mass={g:1,kg:1000,oz:28.349523125,lb:453.59237};
function equivalent(amount,unit,preference='both',system=''){
 if(!Number.isFinite(amount)||amount<=0||preference==='original')return '';
 const format=n=>String(Number(n.toPrecision(4)));
 if(mass[unit]){const target=preference==='metric'?'g':preference==='us'?'oz':['g','kg'].includes(unit)?'oz':'g';if(unit===target)return '';return '≈'+format(amount*mass[unit]/mass[target])+' '+target;}
 const volume={ml:1,l:1000,'US cup':236.5882365,'US tbsp':14.78676478125,'US tsp':4.92892159375,'US fl oz':29.5735295625};
 const key=system==='US'&&['cup','tbsp','tsp'].includes(unit)?'US '+unit:unit;
 if(volume[key])return ['ml','l'].includes(key)?'≈'+format(amount*volume[key]/volume['US fl oz'])+' US fl oz':'≈'+format(amount*volume[key])+' ml';
 return '';
}
const api={equivalent};if(typeof module==='object'&&module.exports)module.exports=api;else root.RecipeMeasurements=api;
})(globalThis);
