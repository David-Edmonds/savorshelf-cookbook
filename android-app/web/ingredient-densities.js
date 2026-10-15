/* Culinary approximations, not universal physical densities. Match named preparation only. */
(function(root){'use strict';
const source='https://www.kingarthurbaking.com/learn/ingredient-weight-chart';
const rows=[
 ['all-purpose flour',120,['all-purpose flour','unbleached all-purpose flour']],
 ['bread flour',120,['bread flour']],
 ['almond flour',96,['almond flour']],
 ['almond meal',84,['almond meal']],
 ['granulated sugar',198,['granulated sugar','white granulated sugar']],
 ['packed brown sugar',213,['packed brown sugar','brown sugar, packed','light brown sugar, packed','dark brown sugar, packed']],
 ['unsifted confectioners sugar',113,["confectioners sugar, unsifted","confectioners' sugar, unsifted",'powdered sugar, unsifted']],
 ['butter',226,['butter','unsalted butter','salted butter','butter, softened','unsalted butter, softened','butter, melted','melted butter']],
 ['unsweetened cocoa',84,['unsweetened cocoa powder','unsweetened cocoa','cocoa powder, unsweetened']],
 ['old-fashioned oats',89,['old-fashioned rolled oats','old-fashioned oats','quick-cooking oats']],
 ['cornstarch',112,['cornstarch']],
 ['chocolate chips',170,['chocolate chips','semisweet chocolate chips','semi-sweet chocolate chips']],
 ['honey',336,['honey']],
 ['maple syrup',312,['maple syrup','pure maple syrup']],
 ['baking powder',192,['baking powder']],
 ['baking soda',288,['baking soda']],
 ['applesauce',255,['applesauce','unsweetened applesauce']],
 ['mashed banana',227,['mashed banana','mashed bananas','bananas, mashed']],
 ['dried breadcrumbs',112,['dried breadcrumbs','dry breadcrumbs']],
 ['panko breadcrumbs',50,['panko breadcrumbs','panko']],
 ['chia seeds',148,['chia seeds']],
 ['flax meal',100,['flax meal','ground flaxseed']],
 ['molasses',340,['molasses']]
];
function lookup(ingredient){if(ingredient.preserveHistoricalUnits)return null;const name=String(ingredient.name||'').toLowerCase().trim().replace(/\s+/g,' ');const row=rows.find(r=>r[2].includes(name));return row?{name:row[0],gramsPerMl:row[1]/236.5882365,gramsPerCup:row[1],source,assumption:'Approximate culinary weight for this named ingredient and preparation; brand and packing can vary.'}:null;}
const api={lookup,rows,source};if(typeof module!=='undefined')module.exports=api;else root.IngredientDensities=api;
})(globalThis);
