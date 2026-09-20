import pathlib,functools,http.server,threading,os,json
from playwright.sync_api import sync_playwright,expect
root=pathlib.Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root/'docs')));threading.Thread(target=server.serve_forever,daemon=True).start()
ids=[x['sourceId'] for x in json.loads((root/'content-overrides.json').read_text(encoding='utf-8'))]
with sync_playwright() as p:
 browser=p.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('SAVORSHELF_TEST_URL',f'http://127.0.0.1:{server.server_port}/cookbook/'));page.wait_for_function('window.RecipeCatalog?.count===40893',timeout=90000)
 before=page.evaluate("localStorage.getItem('our-table-v1')")
 page.evaluate('(ids)=>window.testEntries=ids.map(id=>allEntries().find(e=>e.id===id))',ids)
 for n in range(3):
  page.evaluate('(n)=>RecipeCatalog.open(testEntries[n])',n);expect(page.locator('#modal .method-panel')).to_be_visible();assert page.locator('#modal .substitution').count()>0
  assert '{{' not in page.locator('#modal').inner_text();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
  page.locator('[data-action=uc-back]').first.click()
 assert page.evaluate("localStorage.getItem('our-table-v1')")==before
 page.evaluate('RecipeCatalog.open(testEntries[0])');expect(page.locator('[data-action=catalog-save]')).to_be_visible();page.locator('[data-action=catalog-save]').click()
 page.evaluate('(id)=>{view={type:"detail",id};detailYield=current().servings;render();}',ids[0])
 page.locator('#yield').fill('4');page.locator('#yield').dispatch_event('change')
 expect(page.locator('#app .ingredients-panel')).to_contain_text('56 g softened salted butter')
 expect(page.locator('#app .method-panel')).to_contain_text('28 g softened salted butter')
 assert page.evaluate('(id)=>state.recipes.filter(r=>r.id===id).length',ids[0])==1
 assert not errors,errors
 print(json.dumps({'status':'PASS','threeRepairedRecipesOpened':True,'substitutions':True,'dividedScalingInBrowser':True,'personalStorageUntouchedByBrowsing':True,'errors':errors}));browser.close()
server.shutdown()
