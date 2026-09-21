"""Individually read potato/rice family repairs and reviewed recipe-level aliases."""
import json,pathlib,sqlite3
root=pathlib.Path(__file__).parent
c=sqlite3.connect(root.parent.parent/'outputs/SavorShelf-Content-Repairs/grouped-work.sqlite3')
records=json.loads((root/'content-overrides.json').read_text(encoding='utf-8'));byid={r['sourceId']:r for r in records}
aliases={
 'historical-09bd1518ee3bf7452ac96e49':'historical-8272043c07584e5edfc8c702',
 'historical-a4bbc8c41a8e3b554dab029d':'historical-5d992a2b07fdbb2743fb8c63',
 'historical-d5ea3d462f3aece2b256d7ac':'historical-7908fdad84292603f94d4bbe',
 'historical-e9cb9c480591a4bfa01fe3ba':'historical-5e9ab6b63125023c04e050b4'}
def original(id):return json.loads(c.execute('select record from recipes where id=?',(id,)).fetchone()[0])
def ing(key,amount,unit,name,sub):return dict(key=key,amount=amount,unit=unit,name=name,substitution=sub)
water=lambda n:ing('water',n,'ml','cooking water','Use drinking water; stock changes the flavor and salt level. Rinsing water is separate and is discarded.')
salt=lambda n:ing('salt',n,'g','fine salt','Reduce or omit if preferred. Different salts can be exchanged by weight, not necessarily by spoon volume.')
def add(id,title,servings,minutes,description,ingredients,steps,notes,reference):
 s=original(id);r=dict(s['recipe']);r.update(id=id,title=title,description=description,category='Sides',servings=servings,yieldUnit='side servings',minutes=minutes,totalMinutes=minutes,ingredients=ingredients,steps=steps,notes=notes+' Quantities not stated by the source, equipment guidance, yield and timing are modern estimates. Not kitchen-tested.',sourceStatus='adapted',source=s['recipe']['source']+' SavorShelf measured adaptation. Technique reference: '+reference,versionNote='Modern measured adaptation',updatedAt='2026-09-21T00:00:00Z')
 r['sourceAliases']=[old for old,new in aliases.items() if new==id]
 for old in r['sourceAliases']:r['source']+=' Equivalent source retained: '+original(old)['recipe']['source']
 byid[id]={'sourceId':id,'bodySha256':s['bodySha256'],'recipe':r}
potato_ref='https://idahopotato.com/dr-potato/best-way-to-boil-idaho-potatoes'
def potato(id,title,mode,grams=1000):
 small=mode in ['new','whole','change','twice'];amount=3000 if mode in ['change','twice'] else 1500
 name='small potatoes, scrubbed, about 3–4 cm across' if small else 'peeled potatoes, cut into equal 3 cm pieces'
 ingredients=[ing('potatoes',grams,'g',name,'Use a similarly sized potato with the same texture: waxy for intact pieces; floury for ricing. Large whole potatoes need longer cooking.'),water(amount),salt(15 if mode=='new' else 5)]
 prep='Prepare {{potatoes}}. Remove sprouts and damaged or green areas; discard extensively green potatoes. '
 if mode=='soak':prep+='Cover with separate cold rinsing water for 1 hour, then drain.'
 elif mode=='new':prep+='Scrape off loose skin under running water, then rinse.'
 elif mode=='rice':prep+='Use floury potatoes and rinse the cut pieces.'
 elif mode=='balls':prep+='Trim to similarly sized rounded pieces; rinse. Perfect spheres are not necessary.'
 else:prep+='Rinse clean.'
 if mode in ['change','twice']:
  steps=[prep,'Put the potatoes in a saucepan with {{water|0.5}}, enough to cover by about 1 cm. Bring to a boil, then carefully drain.',
   'Add the remaining cold {{water|0.5}} and {{salt}}. Bring back to a gentle boil and simmer until a thin knife reaches the centers easily, approximately 20–30 minutes after the second boil.',
   'Drain thoroughly. Return to the warm pan off the heat for 3–5 minutes so steam can escape. Peel when cool enough to handle and serve hot.']
  minutes=55;notes='The water-changing method is retained. The source’s suggestion to stop immediately at the second boil is replaced with a tenderness check.' if mode=='twice' else 'The source’s water change is retained; drying is shortened and uses an uncovered warm pan instead of cloth near a flame.'
 elif mode in ['new','balls','old','soak']:
  steps=[prep,'Bring {{water}} to a boil in a saucepan that holds the potatoes comfortably. '+('Add {{salt}}. ' if mode!='soak' else '')+'Carefully add the potatoes; water should just cover them. If necessary, add enough hot water to cover.',
   'Reduce to a gentle simmer. Cook about '+('15–20' if mode=='balls' else '20–25')+' minutes, until a thin knife enters the center without resistance. Do not use time alone as the test.',
   'Drain carefully and return to the warm pan off the heat. '+('Sprinkle with {{salt}} and gently shake. Cover and leave 5 minutes, as in the source.' if mode=='soak' else 'Leave uncovered for 2–3 minutes, gently shaking once, to release steam. Serve hot.')]
  minutes=100 if mode=='soak' else 40
  notes='The hot-water start and source-specific preparation are retained. Choose a pan and water level that keep the pieces submerged.'
 else:
  steps=[prep,'Place the potatoes in a saucepan with {{water}}'+(' and {{salt}}' if mode!='rice' else '')+'. The water should cover them by about 1 cm; add enough cold water if the pan requires it.',
   'Bring to a boil, then simmer gently until tender to the center: about '+('25–35 minutes for these small whole potatoes.' if mode=='whole' else '15–20 minutes for 3 cm pieces.'),
   'Drain and let steam escape for 2–3 minutes. '+('While hot, press through a potato ricer into a serving dish. Sprinkle evenly with {{salt}} and serve without compacting the potato.' if mode=='rice' else 'Serve hot'+('; peel when cool enough to handle if desired.' if mode=='whole' else '.'))]
  minutes=50 if mode=='whole' else 35;notes='A tenderness test replaces dependence on the source’s fixed boiling time. '+('The riced presentation is retained without adding milk or butter.' if mode=='rice' else 'No butter or sauce is required for this base recipe.')
 desc={'plain':'Peeled potato pieces simmer from a cold-water start until tender, then drain and dry briefly before serving.','rice':'Cooked potatoes are pressed through a ricer into a light mound and seasoned with salt; this dish contains no rice.','balls':'Evenly cut potato pieces simmer in salted water and dry briefly in the warm pan, giving tender centers without added fat.','new':'Scraped new potatoes simmer gently and are drained well, keeping their delicate flavor and intact shape.','soak':'Peeled potatoes receive the source’s cold soak, then simmer until tender and finish with salt and a covered rest.','old':'Peeled mature potatoes simmer until tender, then dry briefly in the warm pan for a floury finish.','whole':'Small potatoes cook in their skins until tender, then drain and steam-dry before serving.','change':'Whole potatoes are brought to a boil, given fresh water, then gently cooked and dried before peeling.','twice':'This adaptation retains the source’s two-water approach but cooks the potatoes fully tender before draining and peeling.'}[mode]
 add(id,title,6 if grams==1500 else 4,minutes,desc,ingredients,steps,notes,potato_ref)
# Two water-change sources converge on one modern fully-tender method.
byid.pop('historical-09bd1518ee3bf7452ac96e49',None)
potato('historical-3162c9b27e2456fbcd2e8591','Perunalunta (Riced Potatoes)','rice')
potato('historical-4ed07776bd7c100f03b9a6c2','Brambory vařené (Boiled Potatoes)','soak')
potato('historical-5d992a2b07fdbb2743fb8c63','Keitettyjä perunoita (Boiled Potato Pieces)','balls')
potato('historical-7908fdad84292603f94d4bbe','Nieuwe aardappelen koken (Boiled New Potatoes)','new',1500)
potato('historical-8272043c07584e5edfc8c702','Boiled Potatoes — Fresh-Water Method','change')
potato('historical-b5f107f05138db304f018b87','Oude aardappelen koken (Boiled Mature Potatoes)','old',1500)
potato('historical-c05a3f9107fa9a80b0506311','To Boil Potatoes — Peeled Pieces','plain')
potato('historical-c248ce777dd72a880671f99c','Boiled Potatoes in Their Skins','whole')
# Preserve the optional finish from one of the equivalent new-potato sources as a named variation.
r=byid['historical-7908fdad84292603f94d4bbe']['recipe'];r['variants']=[{'id':'butter-parsley','label':'Butter and parsley finish','ingredients':r['ingredients']+[ing('butter',30,'g','unsalted butter','Use the same weight of a dairy-free butter alternative.'),ing('parsley',5,'g','finely chopped parsley','Omit, or use the same weight of chives for a different flavor.')],'steps':r['steps']+['While the drained potatoes are hot, gently toss them with {{butter}} and {{parsley}}.']}]
rice_ref='https://www.tilda.com/blog/quick-guides/how-to-cook-the-perfect-basmati-rice/'
def rice(id,title,mode):
 grams=225 if mode=='curry' else 240;waterml=480 if mode=='absorb' else 2000
 items=[ing('rice',grams,'g','dry white basmati rice' if mode in ['soak','curry','absorb'] else 'dry long-grain white rice','Use another non-parboiled white long-grain rice and follow its doneness cues. Brown, parboiled and quick-cooking rice need different timings and liquid ratios.'),water(waterml),salt(4)]
 steps=['Rinse {{rice}} in a sieve under cold drinking water until the runoff is mostly clear.'+(' Cover with separate cold soaking water for 2 hours, then drain, retaining the source’s soak.' if mode=='soak' else '')]
 if mode=='absorb':
  steps+=['Combine the drained rice with {{water}} and {{salt}} in a small, heavy saucepan with a close-fitting lid. Bring to a boil.',
   'Cover, reduce to the lowest heat and cook about 12–15 minutes until the water is absorbed and the grains are tender. If still firm and dry, add 15–30 ml hot water and cook a few minutes longer.',
   'Remove from the heat and leave covered for 10 minutes, then separate the grains gently with a fork. Do not multiply cooking time when scaling; use a suitable pan.'];minutes=35;notes='The source’s draining/coals stage is replaced with a measured absorption method and covered rest. The old cup ratio is not claimed as an exact modern conversion.'
 else:
  steps+=['Bring {{water}} and {{salt}} to a boil in a saucepan. Add the drained rice and return to a gentle boil.',
   'Cook uncovered until the grains are tender but separate, checking from '+('7 minutes after soaking; usually 7–10 minutes.' if mode=='soak' else '10 minutes for basmati or 12 minutes for other long-grain white rice; allow up to 20 minutes if needed.'),
   'Drain in a fine sieve. '+('Rinse briefly with clean cool water to stop cooking, as in the source, then drain well. Add directly to hot soup and heat through before serving; soup is a separate recipe.' if mode=='soup' else 'Return to the warm pan off the heat for 3 minutes so excess moisture can evaporate. Gently loosen and serve separately from the main dish.')]
  minutes=150 if mode=='soak' else 30;notes='Rice type, batch size, water and salt quantities are supplied as modern choices. The source’s excess-water method is retained; rice-package timing and actual tenderness take priority over a historical fixed time.'
 desc={'soak':'Pre-soaked basmati rice is cooked in plenty of water and drained, producing separate grains to serve beside curry.','curry':'Basmati rice is boiled in salted water and drained for a plain, separate accompaniment to curry.','soup':'Plain rice is boiled, drained and briefly rinsed as a component to add to hot soup; this recipe does not make broth.','carolina':'Long-grain white rice is boiled in abundant salted water, drained and dried briefly for separate grains.','absorb':'White long-grain rice cooks in measured salted water and rests covered; this is a modern adaptation of the source’s boil-and-dry method.'}[mode]
 add(id,title,4,minutes,desc,items,steps,notes,rice_ref)
rice('historical-241f3d238a6aa69aa8f6d61e','Plain Rice to Serve with Curry','curry')
rice('historical-55b7dbbc2fab113cc67b867d','Rice for Soup (Lihalientä riisiryynejä seassa)','soup')
rice('historical-5e9ab6b63125023c04e050b4','Carolina Boiled Rice','carolina')
rice('historical-afcfb35f8bc1bdc0a661fb55','To Boil Rice — Modern Absorption Adaptation','absorb')
rice('historical-fa2a937023cf0063bf9fe246','Soaked Rice for Curry','soak')
alias_records=[{'id':old,'canonicalId':new,'bodySha256':original(old)['bodySha256'],'reason':'Full ingredients and cooking method reviewed together; equivalent base recipe. Source attribution and any distinct optional finish retained on canonical recipe.'} for old,new in aliases.items()]
alias_records[0]['reason']='Both source variants use a water change. Their modern repairs converge on the same measured formula and full-tenderness method; the premature second-boil stopping instruction is not retained. Both source credits remain.'
(root/'content-overrides.json').write_text(json.dumps(list(byid.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(alias_records,indent=2),encoding='utf-8')
print(json.dumps({'authoredRepairs':13,'reviewedMergedSources':4,'totalOverrides':len(byid)}))
