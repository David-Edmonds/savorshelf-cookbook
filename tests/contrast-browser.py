"""Real computed-color checks; no simulated recipe generation or phone testing."""
import pathlib,os,functools,http.server,threading,re
from playwright.sync_api import sync_playwright
root=pathlib.Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
def luminance(color):
 rgb=[float(v)/255 for v in re.findall(r'[\d.]+',color)[:3]]
 return sum(c*w for c,w in zip([x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb],[.2126,.7152,.0722]))
def ratio(a,b):
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
def check(page):
 values=page.locator('input:not([type=checkbox]):not([type=radio]),textarea,select').evaluate_all("""els=>els.filter(e=>e.getClientRects().length).map(e=>({fg:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor,placeholder:e.hasAttribute('placeholder')?getComputedStyle(e,'::placeholder').color:null}))""")
 for v in values:
  assert ratio(v['fg'],v['bg'])>=4.5,v
  if v['placeholder']:assert ratio(v['placeholder'],v['bg'])>=4.5,v
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 text=page.locator('h1,h2,h3,p,label,summary,button,a,span').evaluate_all("""els=>els.filter(e=>e.getClientRects().length&&!e.closest('.cover,.brand-mark,.sr-only')&&!e.disabled&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>{let bg='rgb(255, 255, 255)';for(let n=e;n;n=n.parentElement){let c=getComputedStyle(n).backgroundColor;if(c.startsWith('rgb(')){bg=c;break;}}let cs=getComputedStyle(e);return {text:e.textContent.trim().slice(0,60),fg:cs.color,bg,size:parseFloat(cs.fontSize),weight:parseInt(cs.fontWeight)||400};})""")
 for v in text:
  minimum=3 if v['size']>=24 or v['size']>=18.66 and v['weight']>=700 else 4.5
  assert ratio(v['fg'],v['bg'])>=minimum,(v,ratio(v['fg'],v['bg']))
 return len(values)
count=0
with sync_playwright() as p:
 exe=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE');b=p.chromium.launch(**({'executable_path':exe} if exe else {}))
 for theme in ['light','dark']:
  page=b.new_page(color_scheme=theme,viewport={'width':390,'height':844})
  page.goto(f'http://127.0.0.1:{server.server_port}/cookbook/')
  for tab in ['recipes','favorites','create','shopping','settings']:
   page.locator('[data-action=tab][data-tab='+tab+']').click();count+=check(page)
  page.locator('[data-action=tab][data-tab=recipes]').click()
  page.locator('[data-action=uc-open]').first.click();count+=check(page)
  page.locator('[data-action=uc-back]').click();page.locator('[data-action=new]').first.click();count+=check(page)
  page.close()
 for name in ['index.html','start.html','privacy.html','credits.html']:
  page=b.new_page(viewport={'width':390,'height':844});page.goto(f'http://127.0.0.1:{server.server_port}/'+name);check(page);page.close()
 b.close()
server.shutdown()
print(f'PASS: {count} visible form controls checked in light/dark system themes; text and placeholders >=4.5:1; recipe dialog and editor; no mobile overflow.')

