"""Build public recipe chunks; preserve source wording instead of parsed guesses."""
import json, pathlib, hashlib, re, importlib.util
spec=importlib.util.spec_from_file_location("repairs",pathlib.Path(__file__).with_name("recipe-repairs.py"));repairs=importlib.util.module_from_spec(spec);spec.loader.exec_module(repairs)
root=pathlib.Path(__file__).parent
source=root.parent.parent/'outputs/SavorShelf-Image-Tools/approved-export/Recipes.jsonl'
out=root/'docs/cookbook/catalog'; out.mkdir(exist_ok=True)
overrides={r['sourceId']:r for r in json.loads((root/'content-overrides.json').read_text(encoding='utf-8'))}
rows=[]; index=[]; audit=[]
for line in source.open(encoding='utf-8'):
    row=json.loads(line)
    if row['id'] in overrides:
        override=overrides[row['id']];assert override['bodySha256']==row['bodySha256']
        row={**row,'recipe':override['recipe'],'description':override['recipe']['description'],'appReady':True}
    r=dict(row['recipe'])
    r['description']=row['description']
    if not row['appReady']:
        r['ingredients'],r['steps'],linked=repairs.repair(row)
        r['sourceIngredients']=row['originalIngredients'];r['sourceSteps']=row['originalSteps']
        audit.append({'id':row['id'],'parsedAmounts':sum(i['amount'] is not None for i in r['ingredients']),'ingredients':len(r['ingredients']),'linkedIngredients':len(linked),'remainingGaps':row['gaps'],'completed':False})
        r['servings']=1; r['yieldUnit']='source batch (yield unspecified)'
        r['notes']='Original ingredient amounts and method are preserved. Yield is unspecified; one batch means the complete source recipe, not one serving. Recognized amounts have been structured without changing their values. Unspecified amounts and older oven wording still need recipe-specific repair. Automatic scaling remains unavailable until the full recipe is checked.'
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

report=root.parent.parent/'outputs/SavorShelf-Content-Repairs';report.mkdir(exist_ok=True)
write(report/'progress.json',{'recipes':len(rows),'completedAdaptations':sum(not r.get('sourceWording') for r in rows),'remainingRecipes':len(audit),'recipesWithParsedAmounts':sum(r['parsedAmounts']>0 for r in audit),'parsedIngredients':sum(r['parsedAmounts'] for r in audit),'linkedIngredients':sum(r['linkedIngredients'] for r in audit),'allRequirementsComplete':False})
(report/'remaining.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in audit),encoding='utf-8')
