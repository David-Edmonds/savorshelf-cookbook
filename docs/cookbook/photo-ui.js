/* SavorShelf 0.8: display-only local image integration. No migration or network. */
(function(){
  'use strict';
  const earlierArt=recipeArt;
  recipeArt=function(recipe,cls=''){
    const photo=RecipePhotos.resolve(recipe);
    // A user image is always rendered by the existing, unchanged image path.
    if(!photo || photo.kind==='personal') return earlierArt(recipe,cls);
    const detail=cls.split(/\s+/).includes('detail-cover');
    const alt='AI-generated serving suggestion: '+photo.depicts;
    const art=`<div class="cover photo bundled-photo ${esc(cls)}" data-photo-recipe="${esc(photo.recipeId)}"><img class="recipe-photo" data-savorshelf-generated="true" src="${esc(detail?photo.src:photo.thumbnail)}" alt="${esc(alt)}" width="${detail?960:320}" height="${detail?720:240}" loading="${detail?'eager':'lazy'}" decoding="async"><span class="photo-credit">${detail?'AI-generated illustration':'AI image'}</span></div>`;
    return art+(detail?'<p class="photo-caption">AI-generated serving suggestion. Toppings and appearance may differ from your version. Your own photo takes priority.</p>':'');
  };
  // Native local-image failures must not leave an unexplained broken-image glyph.
  document.addEventListener('error',function(event){
    const image=event.target;
    if(!image.matches?.('img[data-savorshelf-generated]'))return;
    const frame=image.closest('.bundled-photo');if(!frame)return;
    image.hidden=true;frame.classList.add('photo-unavailable');
    const credit=frame.querySelector('.photo-credit');if(credit)credit.textContent='Illustration unavailable';
  },true);
  render();
})();
