"""Stage the existing app with original sample drafts and no private/imported corpus."""
from pathlib import Path
import shutil,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
def prepare(output):
 output=Path(output)
 if output.exists():
  # Delete only the fixed build staging directory, never user recipes or source.
  assert output.resolve()==(ROOT/'build/public-web').resolve()
  assert output.resolve().is_relative_to(ROOT.resolve())
  shutil.rmtree(output)
 shutil.copytree(ROOT/'web',output)
 globals={
 'central-american-data.js':('CENTRAL_AMERICAN_RECIPES',[]),
 'chatgpt-originals-data.js':('CHATGPT_RECIPE_ORIGINALS',{'schema':1,'completeChatHistory':False,'conversationCount':0,'turnCount':0,'entries':[]}),
 'culinary-catalog-data.js':('CULINARY_CATALOG',[]),
 'easy-web-data.js':('EASY_WEB_RECIPES',[]),
 'enriched-recipes-data.js':('ENRICHED_RECIPES',[]),
 'library-500-data.js':('SAVOR_LIBRARY_500',[]),
 'recovered-pack-data.js':('RECOVERED_RECIPE_PACK',{'app':'Our Table','displayName':'Leggacy','schema':1,'recipes':[]}),
 'southern-data.js':('SOUTHERN_RECIPES',[]),
 'tailored-data.js':('TAILORED_RECIPES',[]),
 'world-recipes-data.js':('WORLD_RECIPES',[]),
 'culinary-sources.js':('CULINARY_SOURCES',{})}
 for name,(key,value) in globals.items():(output/name).write_text('/* Public sample build: private/imported corpus deliberately excluded. */\nwindow.'+key+'='+json.dumps(value)+';\n','utf-8')
 recipes=[]
 def sample(id,title,category,servings,minutes,ingredients,steps):
  recipes.append({'id':'leggacy-sample-'+id,'familyKey':'leggacy-sample-'+id,'title':title,'category':category,'servings':servings,'minutes':minutes,'yieldUnit':'servings','description':'Original sample draft · not kitchen-tested. Save your own version after cooking.','ingredients':[dict(key=k,amount=a,unit=u,name=n,substitution=sub) for k,a,u,n,sub in ingredients],'steps':steps,'notes':'Original Leggacy sample draft, written for this app. Not kitchen-tested. Cooking time is approximate and does not scale automatically. Check ingredient labels for your needs.','source':'Left Field Studio · original sample draft','versionNote':'Untested sample','favorite':False,'rating':0,'pinned':False,'photo':'','history':[],'updatedAt':'2026-10-13T00:00:00.000Z','adaptations':{},'variants':[],'sourceStatus':'suggested','libraryRevision':3})
 sample('tomato-pasta','Simple tomato pasta','Dinner',2,25,[('pasta',180,'g','Dried pasta','Use the same mass of another pasta shape; follow its package timing.'),('tomatoes',400,'g','Canned chopped tomatoes','Use the same mass of crushed canned tomatoes; simmer to your preferred texture.'),('oil',1,'tbsp','Olive oil','Use the same volume of a neutral cooking oil.'),('garlic',2,'','Garlic cloves, peeled and finely chopped','Omit if preferred; the flavor will change.')],['Bring a pan of potable water to a boil and cook {{pasta}} according to its package instructions.','Warm {{oil}} over medium-low heat. Add {{garlic}} and cook briefly until fragrant without browning.','Add {{tomatoes}} and simmer gently for about 10 minutes, stirring occasionally.','Drain the cooked pasta and stir it into the sauce. Taste and season to your preference. Serve promptly.'])
 sample('oatmeal','Warm cinnamon oatmeal','Breakfast',2,12,[('oats',80,'g','Rolled oats','Quick oats can be used at the same mass; follow their package instructions.'),('water',400,'ml','Water','Use the same volume of suitable milk if preferred; check its ingredients.'),('cinnamon',0.25,'tsp','Ground cinnamon','Omit if preferred.')],['Combine {{oats}} and {{water}} in a saucepan.','Bring to a gentle simmer and cook according to the oats package directions, stirring until soft. Add a little extra water if needed.','Stir in {{cinnamon}}. Let cool to a comfortable eating temperature and serve.'])
 sample('roast-carrots','Roasted carrots','Sides',2,35,[('carrots',400,'g','Carrots, scrubbed and cut into even pieces','Parsnips can be used at the same mass; cooking time and flavor will differ.'),('oil',1,'tbsp','Olive oil','Use the same volume of a neutral cooking oil.')],['Heat the oven to 400°F (205°C).','Toss {{carrots}} with {{oil}} and spread in a single layer on a baking tray.','Roast until tender, usually 20–30 minutes, turning partway through. Check tenderness rather than multiplying cooking time when changing servings.','Season to your preference and serve.'])
 for name in ['seed.js','legacy-seed.js']:(output/name).write_text('/* Original, untested public samples. Existing saved recipes are never removed. */\nwindow.STARTER_RECIPES='+json.dumps(recipes,ensure_ascii=False)+';\n','utf-8')
 (output/'recovery.js').write_text('window.RECIPE_RECOVERY=[];\n','utf-8')
 # Keep the resolver API and all personal-photo behavior, omit bundled image mappings.
 (output/'recipe-photos.js').write_text('''(function(root){const api={entries:{},count:0,resolve:r=>r&&r.photo?{kind:'personal',src:r.photo}:null};if(typeof module==='object'&&module.exports)module.exports=api;else root.RecipePhotos=api;})(typeof window==='undefined'?globalThis:window);''','utf-8')
 for p in list(output.rglob('*')):
  if p.is_file() and p.suffix in ['.png','.webp','.jpg','.jpeg'] and not p.name.startswith('icon-'):p.unlink()
 # Newly drawn code-native sample artwork, with no imported image rights dependency.
 art='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240" role="img" aria-label="Simple bowl illustration"><rect width="320" height="240" fill="#eef2fc"/><ellipse cx="160" cy="116" rx="94" ry="26" fill="#fff9ef" stroke="#244fc4" stroke-width="5"/><path d="M66 116 Q80 208 160 208 Q240 208 254 116" fill="#fff9ef" stroke="#244fc4" stroke-width="5"/><path d="M95 116 Q160 144 225 116" fill="none" stroke="#aa822f" stroke-width="4"/><path d="M160 80 Q140 63 160 46 M192 80 Q172 63 192 46" fill="none" stroke="#244fc4" stroke-width="4" stroke-linecap="round"/></svg>'''
 (output/'sample-art.svg').write_text(art,'utf-8')
 for p in list(output.glob('*.js'))+list(output.glob('*.css')):
  if p.name.endswith('-data.js'):continue
  s=p.read_text('utf-8').replace('kitchen-art.png','sample-art.svg').replace('recipe-food-atlas.png','sample-art.svg');p.write_text(s,'utf-8')
 public='''/* Public presentation only: preserve saved state and historical identities. */
(function(){const art=recipeArt;recipeArt=function(r,cls=''){if(r.photo)return art(r,cls);return `<div class="cover ${cls}" style="background:#eef2fc"><img src="sample-art.svg" alt="Simple bowl illustration; not a photo of a tested dish" style="width:100%;height:100%;object-fit:contain"></div>`;};
const prior=settings;settings=function(){const box=document.createElement('div');box.innerHTML=prior();for(const action of ['browse-originals','export-originals','recovery-list'])for(const button of box.querySelectorAll('[data-action="'+action+'"]')){const panel=button.closest('section.panel');if(action==='export-originals'&&panel)panel.remove();else button.remove();}return box.innerHTML.replace('Your bundled collection includes recovered and rebuilt recipes. The history archive contains notes and partial requests, not a verified complete set of original recipes.','Three original sample drafts are included. They are not kitchen-tested. Your saved recipes remain yours.').replace('This is an update to your existing Leggacy app','This continues the existing SavorShelf / Our Table app');};render();})();'''
 (output/'public-samples.js').write_text(public,'utf-8')
 p=output/'index.html';s=p.read_text('utf-8').replace('</head>','<script src="public-samples.js" defer></script></head>');p.write_text(s,'utf-8')
 p=output/'leggacy.css';s=p.read_text('utf-8')+'\n.food-illustration{background:#eef2fc url("sample-art.svg") center/contain no-repeat!important}\n';p.write_text(s,'utf-8')
 assets=['./']+['./'+p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file() and p.name!='sw.js']
 (output/'sw.js').write_text("const CACHE='our-table-leggacy-public-0.25.0';const ASSETS="+json.dumps(assets)+";self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS))));self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('our-table-')&&k!==CACHE).map(k=>caches.delete(k))))));self.addEventListener('fetch',e=>{if(e.request.method==='GET')e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));});",'utf-8')
 report={'mode':'public-samples','sampleIds':[r['id'] for r in recipes],'sampleCount':len(recipes),'privateOriginalEntriesIncluded':0,'importedRecipeEntriesIncluded':0,'bundledFoodPhotosIncluded':0,'personalStorageUnchanged':True,'kitchenTested':False,'finalLogoSupplied':False}
 (ROOT/'build/public-content.json').write_text(json.dumps(report,indent=2),'utf-8')
 return output
if __name__=='__main__':print(prepare(ROOT/'build/public-web'))
