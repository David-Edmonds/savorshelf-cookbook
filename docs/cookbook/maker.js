/* Explicitly limited offline recipe builder, not a language model. */
(function(root){'use strict';
function build(prompt,options={}){
 const q=String(prompt||'').trim().toLowerCase();if(!q||q.length>1800)throw Error('Describe the meal in 1–1,800 characters.');
 if(options.sugar==='sugarFree')throw Error('This offline template cannot verify a sugar-free recipe. Use the ChatGPT handoff to explore an appropriate recipe, then review its ingredients.');
 if(/\b(raw chicken|raw beef|for (?:a )?baby|infant|canning|preserv|sushi|wild mushroom|allerg|diabet|medical|zero sugar|sugar.free)\b/.test(q))throw Error('This limited builder cannot safely handle that request. Use a suitable verified recipe or a connected AI draft with careful review.');
 let servings=Number(q.match(/(?:for|serves?|feeding)\s+(\d+)\b/)?.[1]||options.servings||4);if(!Number.isInteger(servings)||servings<1||servings>20)throw Error('The offline builder supports 1–20 servings.');
 const dairy=/lactose[ -]?free/.test(q)?'lactoseFree':/dairy[ -]?free|no dairy/.test(q)?'dairyFree':(options.dairy||'regular');
 const avoided=new Set((options.avoid||'').toLowerCase().split(',').map(s=>s.trim()).filter(Boolean));
 for(const x of ['garlic','onion','milk','egg','cheese','pepper','tomato','broccoli','carrot','mushroom','spinach','pasta','rice','chicken'])if(new RegExp('(?:no|without|avoid)\\s+(?:any\\s+)?'+x+'s?\\b').test(q))avoided.add(x);
 const banned=name=>[...avoided].some(x=>x&&name.toLowerCase().includes(x));
 const ins=[],steps=[];function add(key,amount,unit,name,sub=''){if(banned(name))return false;ins.push({key,amount:amount===null?null:amount*servings/4,unit,name,substitution:sub});return true;}
 let title,category='Dinner',minutes=30;
 const pasta=/pasta|linguine|spaghetti|noodle/.test(q)&&!avoided.has('pasta');const eggs=/omelet|omelette|scrambl|egg/.test(q)&&!avoided.has('egg');const rice=/rice|bowl/.test(q)&&!avoided.has('rice');const veg=/vegetable|veggie|asparagus|carrot|broccoli/.test(q);
 const chicken=/chicken/.test(q)&&!avoided.has('chicken');
 if(/cake|cookie|bread|tres leches|dessert|pizza|pancake|beef|burger|shrimp|salmon|fish/.test(q))throw Error('The offline builder currently supports chicken/rice bowls, chicken or vegetable pasta, egg skillets and roasted vegetables—not that dish. Connected AI handles wider requests once configured.');
 if(!pasta&&!eggs&&!rice&&!veg&&!chicken)throw Error('Try chicken pasta, a rice bowl, an egg skillet or roasted vegetables. The offline builder does not understand every dish yet.');
 if(/air.fry/.test(q)||(/oven/.test(q)&&(pasta||rice||eggs||chicken)))throw Error('This offline template uses the stovetop. Remove the oven/air-fryer instruction, or use connected AI for a different method.');
 add('oil',2,'tbsp','Olive oil','The same amount of neutral cooking oil works.');
 if(chicken)add('chicken',600,'g','Boneless chicken thighs, cut into bite-size pieces');
 const vegetables=[];for(const [word,name] of [['broccoli','Broccoli florets'],['carrot','Carrots, thinly sliced'],['spinach','Spinach'],['asparagus','Asparagus, trimmed'],['mushroom','Mushrooms, sliced'],['zucchini','Zucchini, sliced']]){if(q.includes(word)&&!avoided.has(word))vegetables.push(name);}
 if(!vegetables.length){const fallback=[veg?'Carrots, thinly sliced':'Broccoli florets','Zucchini, sliced','Carrots, thinly sliced'].find(n=>!banned(n));if(fallback)vegetables.push(fallback);}
 vegetables.forEach((name,n)=>add('veg'+n,300/vegetables.length,'g',name));
 if(!ins.some(i=>i.key.startsWith('veg'))&&!chicken&&!eggs)throw Error('The exclusions leave no main ingredients in this offline template.');
 add('salt',.5,'tsp','Salt, plus more only after tasting');if(!/non.spicy|not spicy|no pepper/.test(q))add('pepper',.25,'tsp','Black pepper (optional)');
 if(pasta){
  title=chicken?'Creamy chicken & vegetable pasta':'Creamy vegetable pasta';add('pasta',320,'g','Dry pasta');
  const milkName=dairy==='lactoseFree'?'Lactose-free whole milk':dairy==='dairyFree'?'Unsweetened soy milk':'Whole milk';
  if(!add('milk',1.5,'cup',milkName))throw Error('This creamy pasta template needs milk or plant milk. Use another dish or connected AI.');
  add('starch',1,'tbsp','Cornstarch','Use cornstarch/cornflour intended for thickening, not coarse cornmeal.');
  steps.push('Cook {{pasta}} in boiling water according to its package. Drain, reserving some pasta water.');
  if(chicken)steps.push('Heat {{oil}} in a large skillet. Cook {{chicken}} in uncrowded batches, turning until the thickest pieces reach 165°F (74°C). Remove to a clean plate.');
  steps.push((chicken?'In the same pan, cook ':'Heat {{oil}} in a skillet. Cook ')+ins.filter(i=>i.key.startsWith('veg')).map(i=>'{{'+i.key+'}}').join(' and ')+' until tender, adding a splash of water if the pan dries.');
  steps.push('Whisk {{milk}} and {{starch}} while cold. Pour into the skillet, bring to a gentle simmer and stir until thickened, about 2–4 minutes.');
  steps.push('Add the drained pasta'+(chicken?' and cooked chicken':'')+'. Season with {{salt}}'+(ins.some(i=>i.key==='pepper')?' and {{pepper}}':'')+'. Loosen with a little reserved pasta water as needed. Serve hot.');
 }else if(eggs&&!chicken){
  title='Vegetable egg skillet';minutes=20;add('eggs',8,'','Eggs');
  steps.push('Heat {{oil}} in a skillet over medium heat. Cook '+ins.filter(i=>i.key.startsWith('veg')).map(i=>'{{'+i.key+'}}').join(' and ')+' until tender.');
  steps.push('Beat {{eggs}} with {{salt}}'+(ins.some(i=>i.key==='pepper')?' and {{pepper}}':'')+'. Pour into the pan and cook gently, stirring and folding until the eggs are fully set.');
  steps.push('The egg mixture should reach 160°F (71°C). Remove from the heat promptly and serve.');
 }else if(rice||chicken){
  title=chicken?'Chicken & vegetable rice bowls':'Vegetable rice bowls';add('rice',1.5,'cup','Dry long-grain white rice');
  steps.push('Cook {{rice}} with the water quantity on its package. Keep warm while preparing the topping.');
  if(chicken)steps.push('Heat {{oil}} in a large skillet. Add {{chicken}} in uncrowded batches and cook until the thickest pieces reach 165°F (74°C). Transfer to a clean plate.');
  steps.push((chicken?'In the same pan, cook ':'Heat {{oil}} in a skillet. Cook ')+ins.filter(i=>i.key.startsWith('veg')).map(i=>'{{'+i.key+'}}').join(' and ')+' until tender, adding a splash of water if needed.');
  steps.push('Season with {{salt}}'+(ins.some(i=>i.key==='pepper')?' and {{pepper}}':'')+'. Serve over the cooked rice'+(chicken?' with the cooked chicken':'')+'.');
 }else{
  title='Simple roasted vegetables';minutes=35;
  steps.push('Heat the oven to 400°F (205°C). Cut the vegetables into evenly sized pieces.');
  steps.push('Toss '+ins.filter(i=>i.key.startsWith('veg')).map(i=>'{{'+i.key+'}}').join(' and ')+' with {{oil}} and {{salt}}'+(ins.some(i=>i.key==='pepper')?' and {{pepper}}':'')+'. Spread over a tray without crowding.');
  steps.push('Roast until tender and lightly browned, checking asparagus or spinach earlier and carrots later. Start checking at 10 minutes; firm vegetables may need 25–35 minutes. Turn halfway.');
 }
 if(ins.some(i=>banned(i.name)))throw Error('An ingredient conflicts with your exclusions.');
 for(const i of ins)if(!i.substitution){
  if(i.key==='chicken')i.substitution='Use the same weight of boneless chicken breast; it may cook faster. Check for 165°F (74°C) at the thickest point.';
  else if(i.key.startsWith('veg'))i.substitution='Use the same weight of a similar vegetable you can eat. Hard vegetables need longer than tender leaves; cook until tender.';
  else if(i.key==='milk')i.substitution=dairy==='dairyFree'?'Use the same volume of another unsweetened dairy-free cooking milk; thickness and taste vary.':dairy==='lactoseFree'?'Use the same volume of labelled lactose-free milk; do not substitute ordinary dairy milk.':'Use the same volume of lactose-free milk or unsweetened soy milk; the taste may differ.';
  else if(i.key==='pasta')i.substitution='Use the same dry weight of another pasta shape, following its package cooking time.';
  else if(i.key==='rice')i.substitution='Use the same dry volume of another white rice; follow its own water ratio and cooking time.';
  else if(i.key==='eggs')i.substitution='Egg size varies. This egg-skillet template has no tested egg-free swap; use an egg-free recipe instead.';
  else if(i.key==='salt')i.substitution='Fine salts differ in density. Start with less, taste the cooked dish and adjust.';
  else if(i.key==='pepper')i.substitution='Leave out for a milder dish; do not replace it with chilli.';
  else i.substitution='No direct substitution is built into this template. Review a recipe designed for the ingredient you have.';
 }
 const now=new Date().toISOString();return {id:'draft-'+Date.now()+'-'+Math.random().toString(36).slice(2,7),title,description:'A new template-built draft. Review before cooking.',category,servings,creationOptions:{servings,dairy,sugar:options.sugar||'original',avoid:[...avoided]},yieldUnit:'servings',minutes,ingredients:ins,steps,notes:(options.sugar==='noAddedSugar'?'No-added-sugar request: use unsweetened ingredients and check labels. Milk and vegetables still contain naturally occurring sugars.\n':'')+'Built offline from a limited recipe template—not generated by ChatGPT and not kitchen-tested. Request: '+prompt+'\nOnly the supported dish, serving count, named vegetables and explicit exclusions above are handled. Review any other requested details yourself. Pan size, temperature and timing do not scale automatically.',source:'SavorShelf offline kitchen builder',versionNote:'New offline draft · review before cooking',rating:0,favorite:false,photo:'',history:[],updatedAt:now};
}
if(typeof module!=='undefined')module.exports={build};else root.RecipeMaker={build};
})(typeof globalThis!=='undefined'?globalThis:this);
