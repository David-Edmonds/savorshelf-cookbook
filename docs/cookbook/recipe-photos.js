/* Bundled serving illustrations. Never written into users' recipe/photo data. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.RecipePhotos=api;})(typeof window==='undefined'?globalThis:window,function(){
  'use strict';
  const PHOTOS = {
"enriched-egg-beet-salad":{"src":"photos/egg-beet-salad.png","thumbnail":"photos/egg-beet-salad.png","depicts":"Egg, beet and watercress salad"},
"enriched-simple-french-toast":{"src":"photos/simple-french-toast.png","thumbnail":"photos/simple-french-toast.png","depicts":"Simple egg-and-milk French toast"},
"enriched-parsley-potato-salad":{"src":"photos/parsley-potato-salad.png","thumbnail":"photos/parsley-potato-salad.png","depicts":"Parsley potato salad with vinaigrette"},
"enriched-butter-baked-apples":{"src":"photos/butter-baked-apples.png","thumbnail":"photos/butter-baked-apples.png","depicts":"Simple butter-baked apples"},
"enriched-white-bean-onion-salad":{"src":"photos/white-bean-onion-salad.png","thumbnail":"photos/white-bean-onion-salad.png","depicts":"White bean and onion salad"},
"enriched-guatemalan-polvorones":{"src":"photos/guatemalan-polvorones.png","thumbnail":"photos/guatemalan-polvorones.png","depicts":"Guatemalan-style three-ingredient polvorones"},
  "heritage-pupusas-loroco": {"src":"photos/pupusas-loroco.png","thumbnail":"photos/pupusas-loroco.png","depicts":"Pupusas de queso con loroco"},
  "world-jerk-illustration": {"src":"photos/jamaican-jerk-chicken.png","thumbnail":"photos/jamaican-jerk-chicken.png","depicts":"Jamaican Jerk Chicken"},
  "starter-burgers": {
    "src": "photos/starter-burgers.webp",
    "thumbnail": "photos/starter-burgers-thumb.webp",
    "depicts": "Big-flavor Badia burgers"
  },
  "starter-sauce": {
    "src": "photos/starter-sauce.webp",
    "thumbnail": "photos/starter-sauce-thumb.webp",
    "depicts": "The big bowl burger sauce"
  },
  "apple-strawberry-cookies": {
    "src": "photos/apple-strawberry-cookies.webp",
    "thumbnail": "photos/apple-strawberry-cookies-thumb.webp",
    "depicts": "Apple & strawberry breakfast cookies"
  },
  "two-banana-bread": {
    "src": "photos/two-banana-bread.webp",
    "thumbnail": "photos/two-banana-bread-thumb.webp",
    "depicts": "Easy two-banana bread"
  },
  "tres-leches": {
    "src": "photos/tres-leches.webp",
    "thumbnail": "photos/tres-leches-thumb.webp",
    "depicts": "Tres leches · classic & coffee"
  },
  "condensed-yogurt-loaf": {
    "src": "photos/condensed-yogurt-loaf.webp",
    "thumbnail": "photos/condensed-yogurt-loaf-thumb.webp",
    "depicts": "Condensed milk & yogurt loaf"
  },
  "yogurt-drumsticks": {
    "src": "photos/yogurt-drumsticks.webp",
    "thumbnail": "photos/yogurt-drumsticks-thumb.webp",
    "depicts": "Saucy yogurt chicken drumsticks"
  },
  "garlic-dijon-thighs": {
    "src": "photos/garlic-dijon-thighs.webp",
    "thumbnail": "photos/garlic-dijon-thighs-thumb.webp",
    "depicts": "Garlic-Dijon air-fryer chicken thighs"
  },
  "sweet-garlic-wings": {
    "src": "photos/sweet-garlic-wings.webp",
    "thumbnail": "photos/sweet-garlic-wings-thumb.webp",
    "depicts": "Saucy sweet-garlic oven wings"
  },
  "tagine-thighs": {
    "src": "photos/tagine-thighs.webp",
    "thumbnail": "photos/tagine-thighs-thumb.webp",
    "depicts": "Moroccan-style chicken tagine bake"
  },
  "banana-pudding": {
    "src": "photos/banana-pudding.webp",
    "thumbnail": "photos/banana-pudding-thumb.webp",
    "depicts": "Banana pudding with biscuit topping"
  },
  "golden-onions": {
    "src": "photos/golden-onions.webp",
    "thumbnail": "photos/golden-onions-thumb.webp",
    "depicts": "Golden onions · quick & caramelized"
  },
  "sweet-carrots-onions": {
    "src": "photos/sweet-carrots-onions.webp",
    "thumbnail": "photos/sweet-carrots-onions-thumb.webp",
    "depicts": "Sweet stovetop carrots & onions"
  },
  "skillet-boneless-thighs": {
    "src": "photos/skillet-boneless-thighs.webp",
    "thumbnail": "photos/skillet-boneless-thighs-thumb.webp",
    "depicts": "Juicy skillet chicken thighs"
  },
  "airfryer-asparagus": {
    "src": "photos/airfryer-asparagus.webp",
    "thumbnail": "photos/airfryer-asparagus-thumb.webp",
    "depicts": "Simple air-fryer asparagus"
  },
  "eggless-pancakes": {
    "src": "photos/eggless-pancakes.webp",
    "thumbnail": "photos/eggless-pancakes-thumb.webp",
    "depicts": "Easy eggless pancakes"
  },
  "easy-oil-bread": {
    "src": "photos/easy-oil-bread.webp",
    "thumbnail": "photos/easy-oil-bread-thumb.webp",
    "depicts": "Easy loaf with regular oil"
  },
  "shrimp-linguine": {
    "src": "photos/shrimp-linguine.webp",
    "thumbnail": "photos/shrimp-linguine-thumb.webp",
    "depicts": "Lime & garlic shrimp linguine"
  },
  "chicken-vegetable-soup": {
    "src": "photos/chicken-vegetable-soup.webp",
    "thumbnail": "photos/chicken-vegetable-soup-thumb.webp",
    "depicts": "Chicken & vegetable soup"
  },
  "mac-cheese": {
    "src": "photos/mac-cheese.webp",
    "thumbnail": "photos/mac-cheese-thumb.webp",
    "depicts": "Creamy macaroni · dairy & soy versions"
  },
  "coleslaw": {
    "src": "photos/coleslaw.webp",
    "thumbnail": "photos/coleslaw-thumb.webp",
    "depicts": "Creamy everyday coleslaw"
  },
  "egg-bites": {
    "src": "photos/egg-bites.webp",
    "thumbnail": "photos/egg-bites-thumb.webp",
    "depicts": "Soft oven egg bites"
  },
  "oven-brisket": {
    "src": "photos/oven-brisket.webp",
    "thumbnail": "photos/oven-brisket-thumb.webp",
    "depicts": "Slow oven beef brisket"
  },
  "bread-pudding": {
    "src": "photos/bread-pudding.webp",
    "thumbnail": "photos/bread-pudding-thumb.webp",
    "depicts": "Simple bread pudding · fresh batch"
  }
};
  for (const value of Object.values(PHOTOS)) Object.freeze(value);
  Object.freeze(PHOTOS);
  const titleKey=s=>String(s||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const byTitle=new Map(Object.entries(PHOTOS).map(([id,entry])=>[titleKey(entry.depicts),{id,entry}]));
  function resolve(recipe) {
    if (!recipe || typeof recipe !== 'object') return null;
    if (typeof recipe.photo === 'string' && recipe.photo.trim()) return {kind:'personal',src:recipe.photo};
    const match = Object.prototype.hasOwnProperty.call(PHOTOS,recipe.id) ? {id:recipe.id,entry:PHOTOS[recipe.id]} : byTitle.get(titleKey(recipe.title));
    return match ? {...match.entry,kind:'generated',recipeId:match.id} : null;
  }
  return Object.freeze({resolve,entries:PHOTOS,count:Object.keys(PHOTOS).length});
});
