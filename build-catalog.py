"""Build public recipe chunks; preserve source wording instead of parsed guesses."""
import json, pathlib, hashlib, re
root=pathlib.Path(__file__).parent
source=root.parent.parent/'outputs/SavorShelf-Image-Tools/approved-export/Recipes.jsonl'
out=root/'docs/cookbook/catalog'; out.mkdir(exist_ok=True)
rows=[]; index=[]
for line in source.open(encoding='utf-8'):
    row=json.loads(line); r=dict(row['recipe'])
    r['description']=row['description']
    if not row['appReady']:
        r['ingredients']=[{'key':f'source-{n}','amount':None,'unit':'','name':s,'substitution':''} for n,s in enumerate(row['originalIngredients'])]
        r['steps']=list(row['originalSteps'])
        r['servings']=1; r['yieldUnit']='source batch (yield unspecified)'
        r['notes']='Original ingredient amounts and method are preserved. Yield is unspecified; one batch means the complete source recipe, not one serving. Source quantities do not scale automatically. Unspecified amounts and older oven wording have not been converted or verified.'
        r['sourceWording']=True
    r['minutes']=r.get('minutes') or 0
    r['catalogId']=row['id']
    rows.append(r)
    chunk=f'{(len(rows)-1)//250:03}.json'
    ingredients=[{'name':i['name'],'amount':i['amount']} for i in r['ingredients']]
    methods=' '.join(m for m,p in [('bake',r'\b(bake|roast|oven)\b'),('simmer',r'\b(skillet|stovetop|simmer|saucepan|saute)\b'),('air fry',r'\bair fry'),('slow cooker',r'\b(slow cooker|crockpot)\b'),('grill',r'\bgrill')] if re.search(p,' '.join(r['steps']),re.I))
    meta={k:r[k] for k in ['id','title','description','category','servings','yieldUnit','minutes','country','cuisine','cuisineTags'] if k in r}
    meta.update(ingredients=ingredients,steps=[methods],sourceWording=r.get('sourceWording',False))
    index.append([r['id'],r['title'],r['description'],r.get('category',''),r['minutes'],r['servings'],r.get('yieldUnit','servings'),r.get('country',''),r.get('cuisineTags',[]),[[i['name'],i['amount']] for i in ingredients],methods,chunk,bool(r.get('sourceWording'))])
def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
for start in range(0,len(rows),250): write(out/f'{start//250:03}.json',rows[start:start+250])
write(out/'index.json',index)
write(out/'manifest.json',{'count':len(rows),'chunks':(len(rows)+249)//250,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceWording':sum(bool(r.get('sourceWording')) for r in rows),'adaptations':sum(not r.get('sourceWording') for r in rows)})
print('Built',len(rows),'recipes;',sum(p.stat().st_size for p in out.glob('*.json')),'bytes')
