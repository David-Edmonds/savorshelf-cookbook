"""Complete Beeton and Viennese mayonnaise dishes and preserve source variations."""
import pathlib,json,sqlite3,copy
root=pathlib.Path(__file__).parent
out=root.parent.parent/'outputs/SavorShelf-Content-Repairs'
db=sqlite3.connect(out/'grouped-work.sqlite3')
rows=json.loads((out/'dressing-candidates.json').read_text(encoding='utf-8'))

records={r['sourceId']:r for r in json.loads((root/'content-overrides.json').read_text(encoding='utf-8'))}
aliases={r['id']:r for r in json.loads((root/'recipe-aliases.json').read_text(encoding='utf-8'))}
newids=[]
def src(n):return json.loads(db.execute('select record from recipes where id=?',(rows[n]['id'],)).fetchone()[0])
def I(k,a,u,n,s):return dict(key=k,amount=a,unit=u,name=n,substitution=s)
def oil(a):return I('oil',a,'ml','olive oil','Use the same volume of a mild sunflower or rapeseed oil.')
def vinegar(a,kind='white wine'):return I('vinegar',a,'ml',kind+' vinegar','Use the same volume of cider vinegar for a different flavor.')
def salt(a=.5):return I('salt',a,'tsp','fine salt','Reduce or omit to taste.')
def pepper(a=.25):return I('pepper',a,'tsp','ground black pepper','Use the same amount of ground white pepper, or omit.')
def parsley(a=1):return I('parsley',a,'tsp','fresh parsley, finely chopped','Use the same amount of finely chopped chives.')
def tk(k):return '{{'+k+'}}'
STORE='Use promptly, or cover and refrigerate at 4°C (40°F) or colder for up to 3 days. Whisk again before serving; oil and vinegar naturally separate. This is a fresh dressing, not a shelf-stable preserve.'
NOTE=' Spoon measures use the app’s modern 15 ml tablespoon and 5 ml teaspoon. Yields, missing quantities and preparation times are modern estimates, not recovered historical measurements. Not kitchen-tested. Scaling changes ingredient amounts, not preparation times.'
def add(n,title,y,t,desc,items,steps,notes):
 s=src(n);r=copy.deepcopy(s['recipe']);r.update(title=title,description=desc,category='Condiments',servings=y,yieldUnit='servings',minutes=t,totalMinutes=t,ingredients=items,steps=steps,sourceStatus='adapted',versionNote='Modern measured adaptation',updatedAt='2026-09-22T20:00:00Z',notes=notes+NOTE,source=s['recipe']['source']+' SavorShelf measured adaptation.');r.pop('variants',None);r['sourceAliases']=[]
 records[r['id']]=dict(sourceId=r['id'],bodySha256=s['bodySha256'],recipe=r);newids.append(r['id']);return r
def variant(r,id,label,items,steps):r.setdefault('variants',[]).append(dict(id=id,label=label,ingredients=items,steps=steps))
def yolks(a):return I('yolks',a,'','large pasteurized egg yolks','Use 18 g commercially pasteurized liquid egg yolk per yolk; do not substitute unpasteurized raw egg.')
def mustard(a):return I('mustard',a,'tsp','dry mustard powder','Use the same volume of prepared Dijon mustard for a milder flavor.')
def cayenne():return I('cayenne',.0625,'tsp','ground cayenne pepper','Omit for a mild mayonnaise.')
def lemon(a):return I('lemon',a,'ml','lemon juice','Use the same volume of lime juice for a different flavor.')
COLD='Transfer to a clean covered container and refrigerate immediately at 4°C (40°F) or colder. Use within 3 days, using a clean spoon each time. This is fresh homemade mayonnaise, not a shelf-stable preserve.'
def emulsion(keys):
 return ['Set a clean small bowl on a damp towel to steady it. Whisk '+', '.join(tk(k) for k in keys)+' until smooth.','Measure {{oil}} into a jug. Whisk continuously while adding it drop by drop at first. Once the mixture is thick and glossy, add the remaining measured oil in a very thin stream, whisking until fully incorporated. Stop pouring if oil pools on the surface and whisk until it blends in.','The finished mayonnaise should be smooth and creamy. If it separates, put 1 teaspoon cold drinking water in a clean bowl and whisk the separated mixture into it a few drops at a time; this small repair addition changes the yield slightly.',COLD]
def eggsource(r):r['source']+=' Raw-yolk handling uses commercially pasteurized egg: https://www.foodsafety.gov/people-at-risk .';return r
def eggs(a):return I('eggs',a,'','large eggs for hard boiling','Use large pasteurized shell eggs if preferred; cook until the yolks are firm.')
def water(a,k='water'):return I(k,a,'ml','drinking water','Use the same volume of drinking water, topping up to cover as directed.')
def boil():return ['Put {{eggs}} in a saucepan with {{water}}, adding more water only if needed to cover by about 2 cm. Bring to a boil, cover, remove from heat and stand for 12 minutes. Cool under cold running water, peel and cut open; the yolks must be firm throughout.']
END='Keep covered at 4°C (40°F) or colder until serving. Refrigerate leftovers within 2 hours and use within 2 days. Do not leave the platter at room temperature for more than 2 hours.'
REF=' Cooking endpoints: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures . Variety meats: https://ask.fsis.usda.gov/article/What-are-the-recommended-cooking-times-for-veal .'
def finish(r):r['category']='Main dishes';r['source']+=REF;return eggsource(r)

merges=[];updatedids=[]
def merge(n,r,reason):
 s=src(n);aliases[s['id']]=dict(id=s['id'],canonicalId=r['id'],bodySha256=s['bodySha256'],reason=reason)
 if s['id'] not in r['sourceAliases']:r['sourceAliases'].append(s['id']);r['source']+=' Equivalent source retained: '+s['recipe']['source']
 records.pop(s['id'],None);merges.append(s)

DAY='Cover and refrigerate promptly at 4°C (40°F) or colder. Use within 1 day. Keep cold until serving and refrigerate within 2 hours of preparation.'
BEETONITEMS=[yolks(2),oil(90),vinegar(60),salt(.25),I('pepper',.125,'tsp','ground white pepper','Use the same amount of finely ground black pepper for a speckled sauce.'),I('stock',15,'ml','prepared unsalted white veal stock, chilled','Use the same volume of unsalted chicken stock for a different flavor.'),I('cream',30,'ml','pouring cream, chilled','Use the same volume of lactose-free dairy cream.')]
BEETONSTEPS=['Whisk {{yolks}}, {{salt}} and {{pepper}} in a clean bowl set on a damp towel. Measure {{oil}} and {{vinegar}} into separate small jugs.',
 'Whisk in a few drops of oil, then a few drops of vinegar. Continue alternating very small additions while whisking constantly, waiting for each addition to blend in before adding more. Use all the measured oil and vinegar. Do not pour in a large quantity at once; this is a relatively loose, acidic mayonnaise.',
 'Gradually whisk in {{stock}} and {{cream}} until smooth. Keep the sauce cold and spoon it over the prepared salad only at serving time.',DAY]
r=add(113,'Beeton Mayonnaise with Cream and White Stock',12,20,'A lightly creamy, vinegar-forward mayonnaise is finished with a little pale stock for cold chicken, fish or salad.',BEETONITEMS,BEETONSTEPS,
 'Beeton No468 gives two yolks, six tablespoons oil, four tablespoons vinegar, one tablespoon white stock and two tablespoons cream. Modern 15 ml tablespoons produce 90, 60, 15 and 30 ml respectively. The original does not specify vinegar strength; ordinary food-grade wine vinegar is a modern choice, not an asserted historical acidity. Salt, pepper, twelve small condiment servings and time are supplied. Prepared white veal stock replaces the cross-reference to stock No107; it is a measured pantry ingredient. The original parsley juice, lobster roe and flavored-vinegar options are retained as complete variations. This sauce is naturally softer than an oil-heavy mayonnaise.');eggsource(r)
vi=copy.deepcopy(BEETONITEMS)+[I('parsley',10,'g','fresh parsley leaves','Use the same weight of watercress leaves for a different green flavor.'),water(10,'herbwater')]
variant(r,'parsley-juice','With parsley juice',vi,['Wash {{parsley}}, drain, then pound finely in a mortar with {{herbwater}}. Squeeze through a clean fine cloth into a small bowl, discarding the fibrous pulp. Reserve all the strained juice.']+BEETONSTEPS[:-1]+['Gradually stir the reserved herb juice into the sauce just before serving.']+[DAY])
vi=copy.deepcopy(BEETONITEMS)+[I('roe',10,'g','raw lobster roe obtained chilled from a fishmonger','Use the parsley-juice variation if lobster roe is unavailable.'),water(50,'roewater')]
variant(r,'lobster-roe','With cooked lobster roe',vi,['Place {{roe}} with {{roewater}} in a small saucepan. Bring to a gentle simmer and stir for about 3–5 minutes until the roe changes to bright red and is firm and opaque throughout. Drain thoroughly, cool promptly, then pound and press through a fine sieve; refrigerate the cooked roe until needed.']+BEETONSTEPS[:-1]+['Stir all the sieved cooked roe into the finished mayonnaise just before serving.']+[DAY]);r['source']+=' Seafood cooking guidance: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
for kind in ['tarragon','cucumber']:
 vi=copy.deepcopy(BEETONITEMS)
 for i in vi:
  if i['key']=='vinegar':i.update(name=kind+'-flavored vinegar, prepared and food-grade',substitution='Use the same volume of white wine vinegar for the plain version.')
 variant(r,kind+'-vinegar','With '+kind+' vinegar',vi,copy.deepcopy(BEETONSTEPS))

CHICKENITEMS=[I('chicken',1500,'g','whole oven-ready chicken, giblets removed','Use the complete cold-roast-chicken variation for leftovers.'),I('roastoil',15,'ml','olive oil for roasting','Use the same volume of sunflower oil.'),I('roastsalt',.5,'tsp','fine salt for the chicken','Reduce or omit to taste.'),I('roastpepper',.25,'tsp','ground black pepper for the chicken','Use the same amount of ground white pepper, or omit.'),eggs(4),water(1200),I('lettuce',400,'g','small young lettuces, about four heads, trimmed weight','Use the same weight of little-gem lettuce.'),I('cress',30,'g','watercress, washed and trimmed','Use the same weight of baby rocket.'),I('endive',100,'g','endive leaves, trimmed','Use the same weight of chicory or tender romaine leaves.')]+copy.deepcopy(BEETONITEMS)
ROAST=['Heat the oven to 190°C (375°F). Pat {{chicken}} dry with paper towel without washing it. Rub with {{roastoil}}, {{roastsalt}} and {{roastpepper}}, then place breast-side up in a roasting tin.',
 'Roast for about 75–95 minutes for the base bird, until a thermometer reaches 74°C (165°F) in the thickest breast and thigh, away from bone. Begin checking early and continue until every checked part reaches the endpoint; size and oven affect timing.',
 'Rest for 15 minutes, then divide into serving joints with clean utensils. Spread in shallow containers and refrigerate promptly until cold, about 1–2 hours. Do not leave the whole bird on the counter to cool. Keep covered once chilled.']
ASSEMBLE=['Wash {{lettuce}}, {{cress}} and {{endive}} thoroughly and dry well. Halve the small lettuces lengthwise, leaving the bases intact enough to hold the leaves together. Slice the cold hard-boiled eggs into rings; alternatively, leave them whole and trim a small piece of white from the bottom so they stand securely, serving the trimmings alongside.',
 'Arrange the cold roast chicken joints in a low mound on a chilled deep platter. Surround with the halved lettuces, watercress, endive and eggs. Spoon all the mayonnaise over the chicken only at the moment of serving.',DAY]
r=add(112,'Beeton Cold Roast Chicken à la Mayonnaise',6,240,'Cold roast chicken is dressed at the table with cream-and-stock mayonnaise and surrounded by young lettuces, eggs, watercress and endive.',CHICKENITEMS,ROAST+boil()+BEETONSTEPS[:-1]+ASSEMBLE,
 'Beeton No962 begins with a cold roast fowl and refers to mayonnaise No468. A full modern roasting, temperature-checking and prompt chilling method is supplied for a chosen 1.5 kg bird, and the complete plain No468 sauce is included. Four hard-boiled eggs are retained, with both ring and standing-whole garnishes explained. Four of the source’s four-to-five young lettuces become 400 g trimmed lettuce; watercress and endive are specified at 30 g and 100 g. Six servings and timing including chilling are estimates. For the source’s two-fowl presentation, use the app’s 2× ingredient scale and roast the birds until each independently reaches the endpoint; cooking time does not automatically double.');finish(r)
vi=[i for i in copy.deepcopy(CHICKENITEMS) if i['key'] not in ['chicken','roastoil','roastsalt','roastpepper']]+[I('roastchicken',1,'','small whole cooked roast chicken, already chilled, about 1 kg cooked bone-in weight','Use an equivalent quantity of properly refrigerated roast chicken joints.')]
variant(r,'cold-roast','With an already chilled roast chicken',vi,['Divide {{roastchicken}} into neat serving joints with clean utensils. Keep chilled until assembly; use properly refrigerated cooked chicken. Allow about 40 minutes for the eggs, sauce and garnishes when the chicken is already cold.']+boil()+BEETONSTEPS[:-1]+ASSEMBLE)

# The scanned Wiener Kochbuch gives oil ranges and concentrated vinegar, not litres of oil.
def vienneseitems(n=6,o=250,l=30):return [yolks(n),oil(o),lemon(l),salt(.5),I('pepper',.125,'tsp','ground white pepper','Use the same amount of ground black pepper, or omit.')]
VIENNESE=['Whisk {{yolks}} in a clean bowl set over a larger bowl of cool water, keeping water out of the yolks. Measure {{oil}} and {{lemon}} separately.',
 'Add oil a few drops at a time while whisking constantly. Once smoothly blended, continue in a very thin stream, alternating small additions of the measured lemon juice. Pause adding liquid whenever the sauce begins to separate and whisk until smooth.',
 'When all the measured oil and lemon juice are incorporated, stir in {{salt}} and {{pepper}}.',COLD]
def acidvariants(r,items,steps,low,acidamount=30):
 for lowoil,acid,id,label in [(True,False,'lower-oil','Lower oil amount'),(False,True,'wine-vinegar','With ordinary wine vinegar'),(True,True,'lower-oil-vinegar','Lower oil amount with wine vinegar')]:
  vi=copy.deepcopy(items)
  for i in vi:
   if i['key']=='oil' and lowoil:i['amount']=low
   if i['key']=='lemon' and acid:i.update(key='vinegar',amount=acidamount,name='ordinary white wine vinegar, about 5% acidity',substitution='Use the complete lemon-juice version instead; do not use concentrated vinegar essence.')
  vs=[s.replace('{{lemon}}','{{vinegar}}').replace('lemon juice','wine vinegar') if acid else s for s in steps]
  variant(r,id,label,vi,vs)
def rescuetwo(r,items,steps):
 vi=copy.deepcopy(items)+[I('rescueyolks',2,'','additional large pasteurized egg yolks for the rescue','Use 36 g commercially pasteurized liquid egg yolk.')]
 variant(r,'extra-yolk-rescue','Two-yolk method for a separated batch',vi,steps[:-1]+['Whisk {{rescueyolks}} in a second clean bowl, then slowly whisk the prepared mayonnaise into them, a few drops at first and a thin stream once smooth. If rescuing an already prepared base, begin with this step and do not make the base again. The ingredient list includes the full original batch plus the rescue addition; this also makes a richer sauce if used with a batch that has not separated.']+[COLD])
r=add(124,'Viennese Six-Yolk Mayonnaise',24,20,'A yolk-rich mayonnaise combines slowly added oil and lemon juice for serving with cold poultry or delicate fish.',vienneseitems(),VIENNESE,
 'The two source entries reproduce Wiener Kochbuch No268. The scanned oil range is one-eighth to one-quarter litre, 125–250 ml; the base chooses 250 ml and a full variation retains 125 ml. Six yolks are retained. Juice from one lemon becomes a modern working 30 ml. The historical alternative is two tablespoons concentrated vinegar essence of unspecified strength; the full vinegar variation instead uses a chosen 30 ml ordinary wine vinegar, not a claim of equal acidity. Salt, pepper, twenty-four small condiment servings and time are supplied. The source’s cold cooked poultry and delicate-fish serving suggestions replace mistranslated ham/fatty-fish descriptions. A two-extra-yolk rescue, described in the following recipe for this sauce too, is retained as a full method.');eggsource(r);acidvariants(r,r['ingredients'],VIENNESE,125);rescuetwo(r,r['ingredients'],VIENNESE)
merge(125,r,'Same Wiener Kochbuch No268 six-yolk mayonnaise; full scanned 125–250ml oil range, lemon/vinegar choice and rescue method retained. Different translated serving suggestions do not create a distinct sauce.')

mixeditems=[eggs(4),water(1200)]+vienneseitems(4,250,60)
MIXED=boil()+['Separate the hard-boiled yolks and press them through a fine sieve into a clean mixing bowl. Refrigerate the cooked whites separately and use within 2 days in another dish. Whisk {{yolks}} into the sieved cooked yolks until smooth.',
 'Measure {{oil|0.5}} into a small jug and whisk it into the yolks a few drops at a time, then in a thin stream once blended. Do not add the acid yet.',
 'Measure the remaining {{oil|0.5}} and {{lemon}} separately. Continue whisking, alternating very small additions of oil and lemon juice until both are incorporated. Stop pouring if oil pools and whisk until it blends in.',
 'Stir in {{salt}} and {{pepper}}.',COLD]
r=add(123,'Viennese Mayonnaise with Cooked and Raw Yolks',28,45,'Sieved hard-boiled yolks enrich a smooth mayonnaise whose lemon juice is added only after half the oil has been incorporated.',mixeditems,MIXED,
 'The scanned No269 specifies four cooked yolks, four raw yolks and one-eighth to one-quarter litre oil, 125–250 ml—not 1.75 litres. This base selects 250 ml; a complete variation retains 125 ml. Juice of two lemons is standardized to a working 60 ml. The vinegar alternative uses a chosen 60 ml ordinary 5% wine vinegar instead of the historical unspecified-strength concentrate, with no equivalence claim. The original instruction to add acid only after half the oil is preserved with linked half-portions that scale together. Full hard-boiled egg preparation and the two-yolk rescue are supplied. Salt, pepper, twenty-eight small condiment servings and timing are estimates.');eggsource(r);acidvariants(r,r['ingredients'],MIXED,125,60);rescuetwo(r,r['ingredients'],MIXED)

BUTTERITEMS=[I('butter',60,'g','unsalted butter, softened but not melted','Use the same weight of salted butter and reduce the added salt.')]+vienneseitems(4,125,60)
BUTTERSTEPS=['Beat {{butter}} in a deep bowl until very soft and fluffy. Beat in {{yolks}} gradually, then continue beating until thoroughly smooth and aerated, about 5–10 minutes.',
 'Set the bowl over cool water to keep the mixture cool without making the butter hard. Measure {{oil}} and {{lemon}} separately and beat them in a few drops at a time, alternating additions and waiting for each to blend in.',
 'Beat in {{salt}} and {{pepper}}. Cover and refrigerate promptly at 4°C (40°F) or colder. The butter makes this sauce firm when cold; stir briefly before serving and use within 3 days.']
r=add(115,'Viennese Butter Mayonnaise',20,25,'Soft butter and pasteurized yolks form a rich lemon mayonnaise that firms gently when chilled.',BUTTERITEMS,BUTTERSTEPS,
 'The scanned No270 gives 6 deka butter, 60 g, not six teaspoons; four raw yolks; one-sixteenth to one-eighth litre oil, 62.5–125 ml, not up to 1.25 litres; and juice from two lemons, not oranges. The base chooses 125 ml oil and a modern working 60 ml lemon juice. Full variations retain the lower oil amount, ordinary vinegar, mustard and herbs. The historical two-spoon vinegar-essence alternative is represented by a chosen 60 ml ordinary 5% wine vinegar, not a recovered concentrate equivalence. Covered refrigeration corrects the extraction’s uncovered instruction. Cool-water mixing is used to avoid setting the butter hard while emulsifying. Salt, white pepper, optional herb/mustard amounts, twenty small portions and timing are supplied.');eggsource(r);acidvariants(r,r['ingredients'],BUTTERSTEPS,62.5,60)
variant(r,'mustard','With mustard',copy.deepcopy(BUTTERITEMS)+[I('mustard',1,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.')],BUTTERSTEPS+['Stir in {{mustard}} just before serving.'])
variant(r,'herbs','With fresh herbs',copy.deepcopy(BUTTERITEMS)+[I('herbs',5,'g','fresh parsley, chervil or chives, finely chopped','Use any one of these herbs or a mixture totaling the same weight.')],BUTTERSTEPS+['Wash, dry and finely chop {{herbs}}, then stir into the sauce just before serving.'])

# Consolidate the generic whole-asparagus recipe with the already completed tips recipe.
r=records[rows[41]['id']]['recipe'];r['title']='Asparagus with Mayonnaise';r['description']='Tender asparagus tips or whole spears are chilled and served with mayonnaise.';r['notes']=r['notes'].replace('Only the tips are part of this recipe;','The base recipe uses only the tips;')
ai=[I('asparagus',300,'g','whole asparagus spears, trimmed weight','Use the same weight of green or white asparagus; peeling and cooking time differ.'),water(1500),I('poachsalt',.5,'tsp','fine salt for the asparagus water','Reduce or omit to taste.'),I('mayo',60,'ml','prepared mayonnaise, kept refrigerated','Use the complete Viennese homemade-sauce variation instead.')]
ASPARAGUS=['Wash {{asparagus}} and trim off woody ends. Peel white asparagus from just below the tip downwards; peel only the tough lower stems of thick green asparagus. Leave the spears whole, tying loosely in small bundles with food-safe string if helpful.',
 'Bring {{water}} and {{poachsalt}} to a boil in a wide pan. Add the spears and simmer until tender but still holding their shape, about 4–7 minutes for green asparagus or 8–12 minutes for white asparagus. Check the thickest stem with a knife; thickness determines the time.',
 'Drain, remove any string and refresh under cold running drinking water. Drain thoroughly, pat dry and refrigerate for about 15 minutes until cold.',
 'Arrange the cold spears on a platter and spoon {{mayo}} over them, or serve the same measured sauce separately.',END]
variant(r,'viennese-spears','Viennese whole-spears version',ai,ASPARAGUS)
vi=[i for i in copy.deepcopy(ai) if i['key']!='mayo']+[I('mayoreserve',60,'ml','mayonnaise reserved from the homemade batch below; not an additional purchase','Use the prepared-mayonnaise whole-spears variation for a quicker version.')]
for i in vienneseitems(3,125,15):
 i['key']='mayo'+i['key']
 if i['key']=='mayosalt':i['amount']=.25
 if i['key']=='mayopepper':i['amount']=.0625
 vi.append(i)
vs=[]
for s in VIENNESE[:-1]:
 for k in ['yolks','oil','lemon','salt','pepper']:s=s.replace(tk(k),tk('mayo'+k))
 vs.append(s)
vs+=['Measure {{mayoreserve}} from the finished mayonnaise and refrigerate it for this dish. Cover the unused sauce separately, refrigerate promptly at 4°C (40°F) or colder and use within 3 days.']+[s.replace('{{mayo}}','the measured reserved mayonnaise') for s in ASPARAGUS]
variant(r,'viennese-homemade','Viennese whole spears with homemade mayonnaise',vi,vs)
r['notes']+=' The whole-spears variation preserves Wiener Kochbuch No292 and its preparation reference No291. It repeats the same cooked-and-chilled asparagus with mayonnaise, so it is consolidated here rather than appearing as a second dish. The new variation supplies 300 g spears, 60 ml sauce and complete green/white peeling and cooking, making two side portions in about 35 minutes. Its homemade sauce follows half the adapted No268 formula, with a measured portion used and surplus accounted for; allow about 15 additional minutes. All original saved IDs and source credits remain attached.';updatedids.append(r['id']);merge(114,r,'Same cooked-and-chilled asparagus served with mayonnaise; full Viennese whole-spears preparation and a self-contained local-book mayonnaise version retained alongside the Dutch tips recipe.')

assert len(newids)==5 and len(merges)==2 and len(updatedids)==1
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids+updatedids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Beeton and scanned Viennese recipes, corrected units and complete cooking and named variations','repair-batch-039.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-merge',aliases[s['id']]['reason'],'repair-batch-039.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),updatedAdaptations=len(updatedids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

