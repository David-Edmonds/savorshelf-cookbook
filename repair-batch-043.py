"""Complete Farmer mayonnaise formulas and preserve the cooked-yolk variation."""
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

DAY='Cover and refrigerate promptly at 4°C (40°F) or colder. Use within 1 day, keep cold until serving, and refrigerate within 2 hours of preparation.'
MI=[mustard(1),salt(1),I('sugar',1,'tsp','icing sugar','Use the same volume of fine white sugar, stirring until dissolved.'),cayenne(),yolks(2),lemon(30),vinegar(30),oil(360)]
MS=['Set a clean mixing bowl over a larger bowl of cool water, keeping water out of the sauce. Mix {{mustard}}, {{salt}}, {{sugar}} and {{cayenne}}, then whisk in {{yolks}} and {{vinegar|0.08333333333333333}}.',
 'Measure {{oil}}, {{lemon}} and the remaining {{vinegar|0.9166666666666666}} into separate small jugs. Keep the oil cool but fluid. Whisk in oil a few drops at a time, waiting until each addition blends in. As the sauce thickens, alternate a thin stream of oil with small additions of the measured lemon juice and remaining vinegar until all are incorporated.',
 'Stop pouring if oil begins to pool and whisk until it blends in. The completed dressing should be thick enough to hold its shape. Keep chilled, and fold it into meat or vegetables only just before serving because their moisture will loosen it.',COLD]
r=add(135,'Farmer Lemon and Vinegar Mayonnaise',30,20,'A thick two-yolk mayonnaise combines olive oil with equal parts lemon juice and vinegar, dry mustard and a touch of sugar.',MI,MS,
 'The full Farmer Mayonnaise Dressing I gives two yolks, one-and-a-half cups oil, two tablespoons each lemon and vinegar, and one teaspoon each mustard, salt and powdered sugar. Modern measures are 360 ml oil and 30 ml each acid. The initial half teaspoon vinegar is 2.5 ml reserved from the total, not an extra quantity. Cayenne, thirty small condiment servings and timing are supplied. Commercially pasteurized yolks replace unspecified raw eggs. The cooked-yolk Dressing II differs only by one mashed hard-boiled yolk and is preserved as a complete named variation with its original source ID and credit.');eggsource(r)
ii=copy.deepcopy(MI)+[eggs(1),water(750)]
is_=boil()+['Separate the firm cooked yolk and press it through a fine sieve. Refrigerate the cooked white separately for another dish and use within 2 days.']+[MS[0].replace('then whisk in','mix in the sieved cooked yolk, then whisk in')]+MS[1:]
variant(r,'cooked-yolk','Dressing II with an extra hard-boiled yolk',ii,is_)
variant(r,'extra-yolk-rescue','Extra-yolk method for a separated batch',copy.deepcopy(MI)+[I('rescueyolk',1,'','additional large pasteurized egg yolk for the rescue','Use 18 g commercially pasteurized liquid yolk.')],MS[:-1]+['Whisk {{rescueyolk}} in a second clean bowl. Add the prepared mayonnaise a few drops at a time while whisking, then in a thin stream once it is smooth. If rescuing a batch already made, begin at this step rather than making the base again. The ingredient list includes the base plus one rescue yolk; with an unbroken base it produces a richer sauce.']+[COLD])
merge(136,r,'Full ingredients and primary method match Dressing I with exactly one extra cooked yolk. Complete cooked-yolk variation retains the difference, preparation, source credit and original saved ID.')

ci=copy.deepcopy(MI)+[I('cream',80,'ml','cold heavy whipping cream, measured before whipping','Use the same volume of lactose-free dairy whipping cream.')]
cs=MS[:-1]+['In a chilled clean bowl, whip {{cream}} until it holds firm peaks, stopping before it becomes grainy. Fold the whipped cream into the finished mayonnaise gently until evenly combined.']+[DAY]
r=add(130,'Farmer Whipped-Cream Mayonnaise',34,25,'Firmly whipped cream is folded into lemon-and-vinegar mayonnaise for a lighter, softly textured dressing.',ci,cs,
 'The original adds one-third cup thick cream, beaten stiff, to Dressing I or II. The 80 ml cream is measured as liquid before whipping, not as 80 ml whipped foam. The complete Dressing I formula is included; Dressing II with a fully prepared cooked yolk is retained as an alternative. Modern measures, cayenne, thirty-four small servings and timing are working choices. The source’s same-day use instruction is preserved.');eggsource(r)
variant(r,'cooked-yolk','Whipped cream with Dressing II cooked-yolk base',copy.deepcopy(ii)+[copy.deepcopy(ci[-1])],is_[:-1]+cs[-2:])

gi=copy.deepcopy(MI)+[I('greenparsley',15,'g','fresh parsley leaves, washed and dried','Use the same weight of extra watercress for a different herb balance.'),I('watercress',30,'g','cultivated watercress, washed and dried','Use the same weight of baby spinach for a milder green sauce.')]
gs=['Tear {{greenparsley}} and {{watercress}} into small pieces and pound thoroughly in a mortar until very wet and finely broken down. Transfer to a clean piece of fine cheesecloth over a small bowl and squeeze firmly to collect the green juice. Discard the squeezed fibrous residue; do not add water to increase the yield.']+MS[:-1]+['Stir the freshly expressed herb juice into the finished mayonnaise gradually until evenly colored. The natural color intensity varies with the greens; this is not a food-dye formula.']+[DAY]
r=add(131,'Farmer Parsley and Watercress Mayonnaise',32,30,'Freshly expressed parsley and watercress juice colors a full lemon-and-vinegar mayonnaise and adds a fresh, peppery herb flavor.',gi,gs,
 'The source calls the full Dressing I base and juice expressed from parsley and watercress in a one-to-two ratio, with no weights. This adaptation chooses 15 g parsley and 30 g watercress, preserving that ratio. Pounding and squeezing through cloth are the actual method; the greens are not simply stirred in chopped. Modern quantities, thirty-two small servings and timing are estimates.');eggsource(r)

ri=copy.deepcopy(MI)+[I('roe',15,'g','raw lobster roe obtained chilled from a fishmonger','Use the parsley-and-watercress recipe instead if lobster roe is unavailable; it makes a different sauce.'),water(75,'roewater')]
rs=['Place {{roe}} and {{roewater}} in a small saucepan. Bring to a gentle simmer and stir for about 3–5 minutes until the roe turns bright red and is firm and opaque throughout. Drain thoroughly, cool promptly, then pound and press through a fine sieve. Refrigerate the cooked roe until needed.']+MS[:-1]+['Stir the sieved cooked lobster roe into the finished mayonnaise just before serving. The roe gives a natural pink-red tint, which varies with the roe and sauce quantities.']+[DAY]
r=add(141,'Farmer Lobster-Coral Mayonnaise',32,30,'Cooked lobster roe is sieved into lemon-and-vinegar mayonnaise for a naturally pink-red seafood dressing.',ri,rs,
 'The red mayonnaise instruction is the final sentence of the Green Mayonnaise passage, not a separate fully quantified formula. It adds sieved lobster coral to mayonnaise; the complete adjacent Dressing I is the chosen base. The source does not print a roe weight or cooking procedure. A working 15 g roe, 75 ml cooking water, full preparation, thirty-two small portions and timing are supplied. Coral means lobster roe here, not shell, tomalley or red food coloring. This is distinct from the parsley/watercress sauce.');eggsource(r);r['source']+=' Seafood cooking context: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'

pi=[I('potato',100,'g','small floury potato, skin on, about one very small potato','Use the same weight of another floury baking potato.'),mustard(1),salt(1),I('sugar',1,'tsp','icing sugar','Use the same volume of fine white sugar.'),vinegar(30),oil(180)]
ps=['Heat the oven to 200°C (390°F). Scrub {{potato}}, prick the skin a few times and place directly on a baking tray without foil. Bake for about 35–50 minutes until the center is completely tender when pierced; size and variety affect the time.',
 'While just cool enough to handle, split the baked potato, scoop the flesh into a bowl and discard the skin. Mash thoroughly, then mix in {{mustard}}, {{salt}} and {{sugar}}. Stir in {{vinegar|0.5}} and press the mixture through a fine sieve into a clean bowl.',
 'Let the smooth potato mixture cool to room temperature, about 10 minutes. Measure {{oil}} and the remaining {{vinegar|0.5}} separately. Whisk in oil very slowly, a few drops at first, alternating with small additions of the remaining vinegar until all are incorporated and the sauce is creamy. Stop pouring if oil pools and whisk until it blends in.',
 'Cover and refrigerate promptly at 4°C (40°F) or colder until serving; use within 2 days. Stir before serving. This is a fresh egg-free potato dressing, not a shelf-stable commercial mayonnaise.']
r=add(140,'Farmer Egg-Free Baked-Potato Mayonnaise',18,70,'Smooth baked potato binds olive oil, vinegar, mustard and a little sugar into a creamy egg-free dressing.',pi,ps,
 'The original calls a very small baked potato, one teaspoon each mustard, salt and sugar, two tablespoons vinegar and three-quarter cup oil. The potato is a working 100 g raw weight and includes its complete baking method. Modern liquid measures are 30 ml vinegar and 180 ml oil. Half the vinegar is mixed in before sieving and half alternates with the oil, as printed. Eighteen small servings and the total including baking and cooling are estimates. No egg is added, so this is distinct from the egg-based formulas.')

assert len(newids)==5 and len(merges)==1
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Farmer base and component recipes with measured variants and source-preserving consolidation','repair-batch-043.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-duplicate','Identical full base plus preserved complete cooked-yolk variation','repair-batch-043.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

