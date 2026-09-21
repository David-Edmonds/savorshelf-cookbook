"""Resumable full-content review groups. Groups are candidates, not duplicate verdicts."""
import collections,hashlib,json,pathlib,re,sqlite3
root=pathlib.Path(__file__).parent
out=root.parent.parent/'outputs/SavorShelf-Content-Repairs';out.mkdir(exist_ok=True)
source=root.parent.parent/'outputs/SavorShelf-Image-Tools/approved-export/Recipes.jsonl'
overrides={r['sourceId'] for r in json.loads((root/'content-overrides.json').read_text(encoding='utf-8'))}
alias_path=root/'recipe-aliases.json'
aliases={r['id'] for r in json.loads(alias_path.read_text(encoding='utf-8'))} if alias_path.exists() else set()
def normal(text):return ' '.join(re.findall(r'[a-z0-9]+',text.lower()))
def ingredient_name(i):
 text=normal(i['name'])
 return ' '.join(w for w in text.split() if w not in {'a','an','the','of','some','little','one','two','three','four','five','six','half','cup','cups','pound','pounds','ounce','ounces','teaspoon','tablespoon','teaspoons','tablespoons'})
def methods(steps):
 text=' '.join(steps).lower()
 return [tag for tag,pattern in [('bake',r'\b(?:bak\w*|oven)\b'),('boil',r'\b(?:boil\w*|simmer\w*)\b'),('fry',r'\b(?:fr[yi]\w*|saut\w*)\b'),('steam',r'\bsteam\w*\b'),('roast',r'\broast\w*\b'),('raw',r'\b(?:salad|uncooked|raw)\b'),('preserve',r'\b(?:pickle|ferment|steriliz|jar)\w*\b') ] if re.search(pattern,text)]
db=sqlite3.connect(out/'grouped-work.sqlite3')
db.executescript('''CREATE TABLE IF NOT EXISTS recipes(id TEXT PRIMARY KEY,body_hash TEXT NOT NULL,family TEXT NOT NULL,formula TEXT NOT NULL,status TEXT NOT NULL,record TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY,body_hash TEXT NOT NULL,decision TEXT NOT NULL,reason TEXT NOT NULL,evidence TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS family_idx ON recipes(family);CREATE INDEX IF NOT EXISTS formula_idx ON recipes(formula);''')
families=collections.Counter();exact=collections.Counter();total=0
for line in source.open(encoding='utf-8'):
 r=json.loads(line);names=sorted(ingredient_name(i) for i in r['recipe']['ingredients']);actions=methods(r['originalSteps'])
 core=[]
 joined=' '.join(names)
 for tag,pattern in [('chicken',r'\bchicken\b'),('beef',r'\b(?:beef|veal)\b'),('pork',r'\b(?:pork|bacon|ham)\b'),('fish',r'\b(?:fish|cod|salmon|trout|herring|tuna)\b'),('shellfish',r'\b(?:shrimp|prawn|crab|lobster|oyster|mussel)\w*\b'),('rice',r'\brice\b'),('potato',r'\bpotato\w*\b'),('flour',r'\b(?:flour|pastry|dough)\b'),('egg',r'\begg\w*\b'),('legume',r'\b(?:bean|lentil|pea|chickpea)\w*\b'),('fruit',r'\b(?:apple|pear|peach|plum|cherry|cherries|berry|berries|currant|quince|orange|lemon)\w*\b')]:
  if re.search(pattern,joined):core.append(tag)
 family=hashlib.sha256(json.dumps([core or names[:2],actions]).encode()).hexdigest()[:20]
 # Exact full ingredient/method equivalence ignores names, but never ignores quantities.
 formula=hashlib.sha256(json.dumps([sorted(normal(s) for s in r['originalIngredients']),[normal(s) for s in r['originalSteps']]]).encode()).hexdigest()
 status='merged' if r['id'] in aliases else 'adapted' if r['appReady'] or r['id'] in overrides else 'pending'
 db.execute('INSERT INTO recipes VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET body_hash=excluded.body_hash,family=excluded.family,formula=excluded.formula,status=excluded.status,record=excluded.record',(r['id'],r['bodySha256'],family,formula,status,line.strip()))
 if status=='pending':families[family]+=1
 exact[formula]+=1;total+=1
db.commit()
groups=[]
for family,count in families.most_common():
 rows=[json.loads(r[0]) for r in db.execute("SELECT record FROM recipes WHERE family=? AND status='pending' ORDER BY id",(family,))]
 groups.append({'family':family,'count':count,'methods':methods(rows[0]['originalSteps']),'ingredients':[i['name'] for i in rows[0]['recipe']['ingredients']],'ids':[r['id'] for r in rows]})
(out/'groups.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
duplicates=[{'fingerprint':key,'ids':[r[0] for r in db.execute('SELECT id FROM recipes WHERE formula=?',(key,))]} for key,count in exact.items() if count>1]
(out/'exact-recipe-candidates.json').write_text(json.dumps(duplicates,indent=2),encoding='utf-8')
report={'records':total,'pending':sum(families.values()),'groups':len(families),'multiRecipeGroups':sum(n>1 for n in families.values()),'pendingInMultiRecipeGroups':sum(n for n in families.values() if n>1),'exactFullTextCandidateGroups':len(duplicates),'automaticallyMerged':0}
(out/'grouping-summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report));print(json.dumps([{'family':g['family'],'count':g['count'],'methods':g['methods']} for g in groups[:8]],ensure_ascii=False))
