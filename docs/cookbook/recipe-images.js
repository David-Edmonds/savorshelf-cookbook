/* Local representative artwork; never changes saved photos or recipe identities. */
(function(root){
 'use strict';
 const labels=['Roasted chicken','Salmon','Shrimp pasta','Roast beef','Vegetable soup','Pancakes','Sliced bread','Cake','Roasted vegetables','Creamy sauce','Baked eggs','Vegetable rice'];
 function choose(recipe){
  const t=String(recipe.title||'').toLowerCase();
  if(/sauce|dressing|syrup|glaze|whipped cream/.test(t))return 9;
  if(/soup|stew|tagine/.test(t))return 4;
  if(/pancake|waffle|crepe/.test(t))return 5;
  if(/bread|biscuit|muffin|loaf|tortilla|flatbread/.test(t))return 6;
  if(/cake|pudding|leches|cookie|crumble|pie|chocolate|dessert/.test(t))return 7;
  if(/shrimp|prawn|pasta|linguine|macaroni/.test(t))return 2;
  if(/salmon|fish|tuna|seafood/.test(t))return 1;
  if(/chicken|turkey|wing|duck|poultry/.test(t))return 0;
  if(/beef|burger|brisket|steak|roast|lamb|pork|meatball/.test(t))return 3;
  if(/egg|frittata|casserole/.test(t))return 10;
  if(/vegetable|asparagus|carrot|cabbage|coleslaw|sprout|greens|beans/.test(t))return 8;
  return ({Breakfast:5,Desserts:7,Sides:8,Sauces:9})[recipe.category]??11;
 }
 root.RecipeImages={choose,labels};
 if(typeof module!=='undefined')module.exports=root.RecipeImages;
})(typeof window!=='undefined'?window:globalThis);
