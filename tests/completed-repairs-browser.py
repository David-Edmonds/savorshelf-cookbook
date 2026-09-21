import pathlib,functools,http.server,threading,os,json
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
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root/'docs')));threading.Thread(target=server.serve_forever,daemon=True).start()
ids=[x['sourceId'] for x in json.loads((root/'content-overrides.json').read_text(encoding='utf-8'))]
with sync_playwright() as p:
 browser=p.chromium.launch();page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(os.environ.get('SAVORSHELF_TEST_URL',f'http://127.0.0.1:{server.server_port}/cookbook/'));page.wait_for_function(f"window.RecipeCatalog?.count==={expected['count']}",timeout=90000)
 before=page.evaluate("localStorage.getItem('our-table-v1')")
 page.evaluate('(ids)=>window.testEntries=ids.map(id=>allEntries().find(e=>e.id===id))',ids)
 for n in range(len(ids)):
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
 # A previously saved source ID remains active after its catalog duplicate is merged.
 result=page.evaluate('''async()=>{const alias='historical-09bd1518ee3bf7452ac96e49',canonical='historical-8272043c07584e5edfc8c702';const e=allEntries().find(e=>e.id===canonical);const r=(await (await fetch('catalog/'+e.chunk)).json()).find(r=>r.id===canonical);r.id=alias;r.notes='Personal alias note';r.rating=5;r.versionNames={original:'Family potatoes'};commit(s=>s.recipes.push(r));const entries=allEntries();return {kept:state.recipes.find(r=>r.id===alias).notes==='Personal alias note',hiddenDuplicate:!entries.some(e=>e.id===canonical),visibleSaved:entries.some(e=>e.id===alias&&e.kind==='Saved')};}''')
 assert result=={'kept':True,'hiddenDuplicate':True,'visibleSaved':True},result
 assert not errors,errors
 print(json.dumps({'status':'PASS','repairedRecipesOpened':len(ids),'substitutions':True,'dividedScalingInBrowser':True,'personalStorageUntouchedByBrowsing':True,'errors':errors}));browser.close()
server.shutdown()
