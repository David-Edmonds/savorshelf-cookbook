"""Complete Viennese egg starters and their cooked and uncooked mayonnaise components."""
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

DAY='Keep covered at 4°C (40°F) or colder and use within 1 day. Refrigerate within 2 hours of preparation and keep cold until serving.'
COOKEDITEMS=[yolks(4),vinegar(15,'tarragon'),lemon(15),water(15,'basewater'),oil(200),salt(.5),I('mustard',1,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.')]
COOKEDSTEPS=['Whisk {{yolks}}, {{vinegar}}, {{lemon}} and {{basewater}} in a heatproof bowl. Set over gently simmering water with the bowl above the water, and whisk continuously until the mixture thickens and reaches 71°C (160°F). Remove immediately; do not boil or scramble the yolks.',
 'Set the bowl in a larger bowl of cold water, keeping water out of the sauce, and stir until the yolk mixture is cool but still smooth, about 10 minutes. Do not leave it on the counter for a prolonged cooling period.',
 'Gradually whisk in {{oil}}, a few drops at first and then a thin stream as the sauce thickens. Stir in {{salt}} and {{mustard}}. Pause pouring if oil pools and whisk until it blends in.',COLD]
r=add(121,'Viennese Mayonnaise with a Cooked Yolk Base',20,35,'A gently cooked lemon-and-tarragon yolk base is cooled before oil and mustard are whisked in.',COOKEDITEMS,COOKEDSTEPS,
 'The two Neues Wiener Menu- und Kochbuch passages describe the same four-yolk cooked base. This version follows the eggs-with-mayonnaise passage: one spoon each tarragon vinegar, lemon juice and water, interpreted as modern 15 ml tablespoons. Oil, salt and mustard were unmeasured; 200 ml oil, half teaspoon salt and one teaspoon prepared mustard are explicit modern working quantities. The other passage uses plain vinegar and adds more vinegar after cooling; a complete variation retains that difference, with a chosen extra 15 ml. Its cold-water rescue is also retained as a full method. Cooking over a water bath to a measured endpoint replaces direct heat on the stove. Twenty small condiment servings and timing are estimates.');eggsource(r);r['source']+=' Egg-dish cooking endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
vi=copy.deepcopy(COOKEDITEMS)
for i in vi:
 if i['key']=='vinegar':i.update(name='white wine vinegar for the cooked base',substitution='Use the same volume of cider vinegar.')
vi.append(I('finishvinegar',15,'ml','additional white wine vinegar for finishing','Use the same volume of cider vinegar.'))
vs=COOKEDSTEPS[:-1]+['Gradually whisk in {{finishvinegar}} after the oil to make the more acidic finishing-vinegar version.']+[COLD]
variant(r,'extra-vinegar','Other source passage — vinegar finish',vi,vs)
variant(r,'cold-water-rescue','Cold-water method for a separated batch',copy.deepcopy(vi)+[water(15,'rescuewater')],vs[:-1]+['Slowly trickle {{rescuewater}}, cold, down the side of the bowl while whisking the finished mayonnaise continuously. This is the source’s rescue addition; if starting with an already prepared separated batch, do not make it again. The ingredient list includes the full vinegar-finish base plus the rescue water. Added water makes the sauce slightly looser even when used with a smooth batch.']+[COLD])
merge(128,r,'Same four-yolk cooked mayonnaise base from the same book; plain-vinegar finishing and cold-water rescue differences retained as complete named methods.')

RAWITEMS=[yolks(3),oil(150),lemon(15),I('mustard',.5,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.'),salt(.25),I('pepper',.0625,'tsp','ground white pepper','Use the complete pepper-free variation if preferred.')]
RAWSTEPS=['Whisk {{yolks}} in a clean bowl on a damp towel. Measure {{oil}} into a jug and whisk it in a few drops at a time until the mixture begins to thicken; continue in a thin stream until all the oil is incorporated.',
 'Gradually whisk in {{lemon}}, then stir in {{mustard}}, {{salt}} and {{pepper}}. Stop pouring whenever the mixture starts to separate and whisk until it blends in.',COLD]
r=add(122,'Viennese Three-Yolk Lemon Mayonnaise',14,20,'A simple three-yolk mayonnaise takes lemon juice after the oil, then a little mustard, salt and optional white pepper.',RAWITEMS,RAWSTEPS,
 'The full Menu14 passage gives three yolks and 1.5 decilitres oil, 150 ml, with juice from half a lemon. The lemon is standardized to a working 15 ml; mustard, salt, pepper, fourteen small condiment portions and time are supplied. The original order—oil first, lemon next, seasoning last—is retained. Commercially pasteurized yolks and covered refrigeration replace an unspecified raw-egg and ice-storage method. The optional pepper-free version and extra-yolk rescue are supplied in full. This uncooked formula is distinct from the four-yolk cooked-base sauce.');eggsource(r)
variant(r,'no-pepper','Without white pepper',[i for i in copy.deepcopy(RAWITEMS) if i['key']!='pepper'],[s.replace(', {{salt}} and {{pepper}}',' and {{salt}}') for s in RAWSTEPS])
variant(r,'extra-yolk-rescue','Extra-yolk method for a separated batch',copy.deepcopy(RAWITEMS)+[I('rescueyolk',1,'','additional large pasteurized egg yolk for the rescue','Use 18 g commercially pasteurized liquid yolk.')],RAWSTEPS[:-1]+['Whisk {{rescueyolk}} in a second clean bowl, then whisk the prepared mayonnaise into it very slowly, a few drops at first and a thin stream once smooth. If rescuing a batch already made, start here rather than making the base again. The ingredient list includes the full base plus the rescue yolk; this also makes a richer four-yolk sauce if used with an unbroken batch.']+[COLD])

# Filled eggs: the source's warm/cold distinction describes making the sauce, not serving it hot.
EGGITEMS=[eggs(6),water(1500),I('greens',80,'g','lamb’s lettuce (mâche), trimmed','Use the complete head-lettuce variation if preferred.'),I('saladoil',15,'ml','olive oil for the greens','Use the same volume of sunflower oil.'),I('saladvinegar',10,'ml','white wine vinegar for the greens','Use the same volume of cider vinegar.'),I('saladsalt',.125,'tsp','fine salt for the greens','Reduce or omit to taste.'),I('pickle',60,'g','pickled cucumber, drained, about one small pickle','Use the same drained weight of cornichons.'),I('anchovies',8,'g','anchovy fillets, drained, about two fillets','Use the same weight of finely sliced smoked sprat for a different flavor.'),I('capers',40,'g','capers, drained','Use the complete caviar-garnish variation if preferred.'),I('chives',20,'g','fresh chives','Use the same weight of finely sliced spring-onion greens.'),I('garnishlemon',60,'g','lemon for garnish, about one small lemon','Use the same weight of lime for a different garnish.'),I('mayoreserve',120,'ml','mayonnaise reserved from the batch made below; not an additional purchase','Measure the finished sauce and refrigerate any extra separately.')]
def cookedhalf():
 a=copy.deepcopy(COOKEDITEMS)
 for i in a:i['amount']/=2
 return a
def eggsteps(raw=False):
 sauce=RAWSTEPS[:-1] if raw else COOKEDSTEPS[:-1]
 return boil()+['Halve the cold hard-boiled eggs lengthwise. Carefully remove the yolks without tearing the whites, chop the firm yolks and refrigerate both parts while making the sauce.']+sauce+['Measure {{mayoreserve}} from the finished sauce and keep chilled for filling the eggs. Cover any unused mayonnaise separately, refrigerate promptly at 4°C (40°F) or colder and use within 3 days.',
 'Wash {{greens}} and dry thoroughly. Just before serving, toss with {{saladoil}}, {{saladvinegar}} and {{saladsalt}}. Arrange around the edge of a chilled serving dish.',
 'Divide the reserved mayonnaise among the egg-white halves and arrange them in the center of the dish. Slice {{anchovies}} into thin strips and place on the filled halves. Wash and finely snip {{chives}}, then scatter over them.',
 'Thinly slice {{pickle}} and washed {{garnishlemon}}. Arrange between the eggs with the chopped cooked yolks. Drain {{capers}} and scatter over the platter to finish. Serve cold.',DAY]
r=add(117,'Viennese Eggs Filled with Mayonnaise',6,75,'Hard-boiled egg halves are filled with mayonnaise and presented with dressed greens, anchovy, chives, capers, pickle and lemon.',EGGITEMS+cookedhalf(),eggsteps(),
 'The full original supplies six eggs, 80 g lamb’s lettuce or two lettuce heads, one pickle, two anchovies, 40 g capers and 20 g chives. Lemon slices and chopped cooked yolks appear in the method and are restored explicitly. Pickle, anchovy and lemon weights, salad dressing and a 120 ml mayonnaise filling are modern working quantities. The base uses half the complete adapted four-yolk cooked sauce; its surplus is accounted for. The uncooked Menu14 sauce is retained as a full alternative. “Warm or cold stirred mayonnaise” describes how the sauce is made, not a requirement to serve the eggs warm. Full head-lettuce and caviar garnishes preserve the other source options. Six servings of two filled halves and total time are estimates.');finish(r);r['category']='Starters'
variant(r,'uncooked-sauce','With the uncooked-yolk mayonnaise',copy.deepcopy(EGGITEMS)+copy.deepcopy(RAWITEMS),eggsteps(True))
vi=copy.deepcopy(EGGITEMS+cookedhalf())
for i in vi:
 if i['key']=='greens':i.update(amount=200,name='small head-lettuce leaves, trimmed, about two heads',substitution='Use the same weight of tender romaine leaves.')
variant(r,'head-lettuce','With head lettuce',vi,eggsteps())
vi=copy.deepcopy(EGGITEMS+cookedhalf())
for i in vi:
 if i['key']=='capers':i.update(key='caviar',amount=20,name='chilled caviar or prepared fish roe, ready to eat',substitution='Use the caper-garnish base recipe instead.')
vs=[s.replace('Drain {{capers}} and scatter over the platter to finish.','Spoon {{caviar}} over the filled eggs just before serving.') for s in eggsteps()]
variant(r,'caviar','With caviar instead of capers',vi,vs);r['notes']+=' The caviar quantity was not printed; 20 g is a modern garnish choice, not a conversion from the 40 g caper amount.'

# No557: poached calf brain in small serving shells with chopped aspic.
BRAINITEMS=[I('brain',400,'g','fresh calf brain prepared for food by an inspected butcher, outer membrane removed','Use the same weight of prepared lamb brains, cooking to the same endpoint; size may change the time.'),water(1500,'poachwater'),I('poachvinegar',30,'ml','white wine vinegar for the poaching liquid','Use the same volume of cider vinegar.'),I('poachsalt',1,'tsp','fine salt for the poaching liquid','Reduce to taste; most remains in the discarded liquid.'),I('stock',200,'ml','clear unsalted veal stock, chilled','Use the same volume of clear unsalted chicken stock.'),I('gelatin',4,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the manufacturer’s equivalent setting quantity of leaf gelatin, soaking and draining it first; agar is not a gram-for-gram substitute.'),I('aspicvinegar',5,'ml','white wine vinegar for the aspic','Use the same volume of cider vinegar.'),I('mayo',20,'ml','prepared mayonnaise, refrigerated','Use the complete homemade-sauce variation if preferred.')]
BRAINSTEPS=['Sprinkle {{gelatin}} over {{stock|0.2}} in a small bowl and leave for 5 minutes. Warm the remaining {{stock|0.8}} in a saucepan, remove from the heat, and stir in the bloomed gelatin until completely dissolved. Stir in {{aspicvinegar}}. Pour into a shallow container, cool briefly and refrigerate for at least 2 hours until firmly set.',
 'Bring {{poachwater}}, {{poachvinegar}} and {{poachsalt}} to a gentle simmer. Keep {{brain}} chilled until adding it to the liquid. Check that the tough outer membrane has been removed; if any remains, lift it away carefully with clean fingertips or a small knife before poaching.',
 'Lower the prepared brain into the liquid and poach gently for about 15–25 minutes, until firm and the thickest part reaches 71°C (160°F). Do not rely on time alone, and avoid a vigorous boil that would break up the delicate pieces.',
 'Lift out with a slotted spoon, drain well and place in a shallow clean container. Cool only until safe to handle, cut into bite-size pieces and refrigerate promptly until fully cold, about 45–60 minutes. Do not cool the whole pot of cooking liquid on the counter.',
 'Chop the set aspic into small pieces. Divide the cold brain among four small food-safe serving shells or shallow ramekins at the base yield, heaping it slightly in the center. Arrange all the chopped aspic around the portions.',
 'Cover and refrigerate the assembled shells for 15 minutes before serving. Divide {{mayo}} among them, about one modern teaspoon per shell at the base yield, spooning it over the brain just before serving.',DAY]
r=add(116,'Viennese Cold Calf Brain with Aspic and Mayonnaise',4,180,'Gently poached calf brain is chilled in small serving dishes with chopped veal-stock jelly and a teaspoon of mayonnaise.',BRAINITEMS,BRAINSTEPS,
 'The full scanned Wiener Kochbuch No557 calls for a peeled brain cooked in salt water and vinegar, chilled pieces in shells, chopped aspic and one coffee-spoon mayonnaise per shell. The printed final chilling interval is one-quarter hour, 15 minutes—not the extracted 1.5 hours. Brain weight, four portions, poaching water, salt and vinegar, and a complete 200 ml aspic with 4 g approximately 200 Bloom gelatin are modern working choices. A modern 5 ml teaspoon represents each unstandardized coffee-spoon. Full preparation, a measured cooking endpoint, prompt refrigeration and aspic setting time are supplied. The prepared mayonnaise is a modern shortcut; the full homemade variation follows half the book’s adapted No268, with a measured portion and surplus accounted for.');finish(r);r['category']='Starters'
HM=[yolks(3),oil(125),lemon(15),salt(.25),I('pepper',.0625,'tsp','ground white pepper','Omit for a milder sauce.')]
HS=['Whisk {{yolks}} in a clean bowl. Measure {{oil}} and {{lemon}} separately. Add oil a few drops at a time while whisking continuously, then in a thin stream as it thickens, alternating small additions of the measured lemon juice. Stir in {{salt}} and {{pepper}} when smooth.',
 'Measure {{mayoreserve}} from the finished mayonnaise for the shells. Cover any unused sauce separately, refrigerate promptly at 4°C (40°F) or colder and use within 3 days.']
vi=[i for i in copy.deepcopy(BRAINITEMS) if i['key']!='mayo']+HM+[I('mayoreserve',20,'ml','mayonnaise reserved from the homemade batch below; not an additional purchase','Use the prepared-mayonnaise base recipe for a quicker version.')]
variant(r,'homemade-mayonnaise','With homemade Viennese mayonnaise',vi,HS+[s.replace('{{mayo}}','the measured reserved mayonnaise') for s in BRAINSTEPS]);r['notes']+=' Allow about 15 additional active minutes for the homemade sauce, which can be made while the aspic sets.'

assert len(newids)==4 and len(merges)==1
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Viennese primary recipes with measured cooked/raw sauces, fillings, poaching and aspic','repair-batch-040.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-merge',aliases[s['id']]['reason'],'repair-batch-040.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

