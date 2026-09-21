import pathlib,json,functools,http.server,threading,os
from playwright.sync_api import sync_playwright,expect
root=pathlib.Path(__file__).resolve().parents[1]
expected=json.loads((root/'docs/cookbook/catalog/manifest.json').read_text(encoding='utf-8'))
visible_count=expected['count']+1452
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if os.environ.get('SAVORSHELF_BASELINE_INDEX') and self.path.endswith('/catalog/index.json'):
   data=(root/'tests/catalog-baseline.json').read_bytes();self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(data);return
  super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=os.environ.get('SAVORSHELF_TEST_URL',f'http://127.0.0.1:{server.server_port}/cookbook/')
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(url,wait_until='domcontentloaded');page.wait_for_function(f"window.RecipeCatalog?.count==={expected['count']}",timeout=90000)
 count=page.locator('#cookbook-count').inner_text()
 baseline=page.evaluate("(()=>{view={type:'detail',id:state.recipes[0].id};detailYield=current().servings;render();const style=getComputedStyle(document.querySelector('.recipe-header h1'));const result={font:style.fontFamily,size:style.fontSize};view={type:'home'};render();return result;})()")
 before=page.evaluate("localStorage.getItem('our-table-v1')")
 assert page.locator('#cookbook-results .card').count()==24
 page.locator('#cookbook-search').fill('A Cake without Butter');expect(page.locator('#cookbook-results')).to_contain_text('A Cake without Butter')
 page.get_by_role('button',name='A Cake without Butter',exact=False).first.click()
 expect(page.locator('#modal .recipe-header h1')).to_have_text('A Cake without Butter',timeout=30000)
 expect(page.locator('#modal')).to_contain_text('Beat well 5 eggs.')
 expect(page.locator('#modal .ingredients-panel')).to_contain_text('6 oz flour (≈170.1 g)')
 expect(page.locator('#modal .method-panel')).to_contain_text('6 oz flour (≈170.1 g)')
 assert page.locator('#modal .recipe-content-grid .ingredients-panel').count()==1
 assert page.locator('#modal .recipe-content-grid .method-panel').count()==1
 assert page.locator('#modal .recipe-header-art .cover').count()==1
 assert page.locator('#modal .recipe-header h1').evaluate('(e)=>({font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize})')==baseline
 page.locator('[data-catalog-ingredient]').first.check()
 expect(page.locator('#catalog-ingredient-progress')).to_contain_text('1 of')
 page.screenshot(path=str(root/'tests/catalog-design-mobile.png'))
 assert 'five 5 eggs' not in page.locator('#modal').inner_text()
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
 page.locator('[data-action=uc-back]').first.click()
 assert page.evaluate("localStorage.getItem('our-table-v1')")==before
 page.get_by_role('button',name='A Cake without Butter',exact=False).first.click();expect(page.locator('[data-action=catalog-save]')).to_be_visible()
 page.locator('[data-action=catalog-save]').click()
 assert page.evaluate("state.recipes.some(r=>r.title==='A Cake without Butter')")
 page.get_by_role('button',name='A Cake without Butter',exact=False).first.click()
 assert page.locator('#yield').count()==0
 expect(page.locator('#app')).to_contain_text('Automatic scaling is unavailable')
 page.locator('[data-action=uc-back]').first.click()
 original=json.loads(before);after=page.evaluate('state.recipes')
 for r in original['recipes']:assert r==next(x for x in after if x['id']==r['id'])
 # Preserve personal metadata through catalog reload and ordinary saving.
 page.evaluate("commit(s=>{const r=s.recipes.find(r=>r.title==='A Cake without Butter');r.notes='Personal note';r.rating=4;r.versionNames={original:'My version'};})")
 saved=page.evaluate("localStorage.getItem('our-table-v1')");page.reload();page.wait_for_function(f"window.RecipeCatalog?.count==={expected['count']}",timeout=90000)
 assert page.evaluate("localStorage.getItem('our-table-v1')")==saved
 assert page.evaluate("state.recipes.filter(r=>r.title==='A Cake without Butter').length")==1
 page.locator('[data-action=uc-clear-search]').click()
 page.locator('[data-action=uc-next]').click();expect(page.locator('#cookbook-count')).to_contain_text('2 /')
 assert page.locator('#cookbook-results .card').count()==24
 page.evaluate('navigator.serviceWorker.ready');page.reload();page.wait_for_function(f"window.RecipeCatalog?.count==={expected['count']}",timeout=90000)
 page.context.set_offline(True);page.reload();page.wait_for_function(f"window.RecipeCatalog?.count==={expected['count']}",timeout=90000)
 assert page.evaluate("localStorage.getItem('our-table-v1')")==saved
 page.context.set_offline(False)
 assert not errors,errors
 result={'status':'PASS','url':url,'count':count,'catalog':expected['count'],'sourceWordingDetail':True,'saveAndPersonalDataPreserved':True,'pagination':True,'widths':[320,390,768,1280],'offlineReload':True,'browserErrors':errors,'physicalPhone':False}
 print(json.dumps(result));(root/'tests/catalog-validation.json').write_text(json.dumps(result,indent=2));b.close()
server.shutdown()
