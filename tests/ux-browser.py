import pathlib,os,json,functools,http.server,threading
from playwright.sync_api import sync_playwright,expect
root=pathlib.Path(__file__).resolve().parents[1]
def browser_options():
 path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE');return {'executable_path':path} if path else {}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(**browser_options());page=b.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}/cookbook/');page.wait_for_function('window.RecipeCatalog?.count===40884',timeout=90000);expect(page.locator('#cookbook-count')).to_contain_text('42,336')
 original=page.evaluate("localStorage.getItem('our-table-v1')")
 builds=page.evaluate('CookbookExperience.metrics.indexBuilds')
 # Filtering retains native select focus and the open disclosure.
 page.locator('#cookbook-refine').evaluate('(e)=>e.open=true');page.locator('[data-refine-group=origin]').evaluate('(e)=>e.open=true')
 country=page.locator('[data-cookbook-facet=country]');country.focus();country.select_option(label='El Salvador')
 assert country.evaluate('(e)=>document.activeElement===e')
 assert page.locator('[data-refine-group=origin]').evaluate('(e)=>e.open')
 search=page.locator('#cookbook-search');search.fill('nonsenseunlikelydishxxxx');expect(page.locator('.empty-results')).to_be_visible()
 page.locator('[data-action=uc-clear-search]').click();expect(search).to_be_focused();expect(country).to_have_value('El Salvador')
 page.locator('[data-action=uc-clear-one][data-facet=country]').click();expect(country).to_be_focused();expect(country).to_have_value('')
 page.locator('[data-action=uc-filter][data-filter=Saved]').click();expect(page.locator('[data-filter=Saved]')).to_have_attribute('aria-pressed','true')
 page.locator('[data-action=uc-filter][data-filter=All]').click();page.wait_for_function('window.RecipeCatalog?.count===40884',timeout=90000);expect(page.locator('#cookbook-count')).to_contain_text('42,336')
 search.fill('polvorones');expect(page.locator('#cookbook-results')).to_contain_text('polvorones',ignore_case=True)
 page.locator('[data-action=uc-clear-search]').click()
 page.locator('#cookbook-refine').evaluate('(e)=>e.open=false')
 # Pagination goes to the results, not the filter/header area.
 page.locator('[data-action=uc-next]').click();expect(page.locator('#cookbook-count')).to_contain_text('2 / 1764')
 assert page.evaluate('scrollY')>200
 card=page.locator('[data-action=uc-open]').nth(2);card.scroll_into_view_if_needed();key=card.get_attribute('data-key');y=page.evaluate('scrollY');card.click()
 expect(page.locator('#modal')).to_be_visible();page.locator('[data-action=uc-back]').click();expect(page.locator('#modal')).not_to_be_visible()
 expect(page.locator('#cookbook-count')).to_contain_text('2 / 1764');page.wait_for_timeout(150)
 assert abs(page.evaluate('scrollY')-y)<5,(y,page.evaluate('scrollY'))
 assert page.evaluate('document.activeElement.dataset.key')==key
 # Stored browse state is restored; the user's actual recipes remain untouched.
 page.reload();expect(page.locator('#cookbook-count')).to_contain_text('2 / 1764')
 assert page.evaluate("localStorage.getItem('our-table-v1')")==original
 # Bounded result DOM, reusable index, and responsive layouts across navigation.
 timings=[]
 for query in ['chicken','rice','pupusa','beans','']:
  page.locator('#cookbook-search').fill(query);page.wait_for_timeout(200);timings.append(page.evaluate('CookbookExperience.metrics.lastSearchMs'))
 assert page.locator('#cookbook-results .card').count()<=24
 assert page.evaluate('CookbookExperience.metrics.indexBuilds')==builds
 for width in [320,390,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for tab in ['recipes','favorites','create','shopping','settings']:
   page.locator('[data-action=tab][data-tab='+tab+']').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,tab)
 page.locator('[data-action=tab][data-tab=recipes]').click();page.evaluate('scrollTo(0,0)')
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(root/'tests/ux-mobile.png'))
 page.set_viewport_size({'width':1280,'height':900});page.screenshot(path=str(root/'tests/ux-desktop.png'))
 assert page.evaluate("localStorage.getItem('our-table-v1')")==original
 page.evaluate('navigator.serviceWorker.ready');page.reload();page.context.set_offline(True);page.reload();page.wait_for_function('window.RecipeCatalog?.count===40884',timeout=90000);expect(page.locator('#cookbook-count')).to_contain_text('42,336');assert page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--ux-ink').trim()")=='#19394a';page.context.set_offline(False)
 assert not errors,errors
 print(json.dumps({'status':'PASS','checks':'Filter focus, open groups, query clear, chips, scopes, pagination, recipe return focus and scroll, reload state, unchanged saved recipes, 24-card rendering, reused index, five tabs at four widths, no browser errors','localSearchMs':timings},indent=2));b.close()


server.shutdown()
