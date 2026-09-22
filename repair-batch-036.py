"""Complete Wallace mayonnaise formulas and preserve source variations and duplicate credits."""
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

WARMEND='Serve promptly. If preparing ahead, cool the sauce promptly in a shallow container, cover and refrigerate at 4°C (40°F) or colder within 2 hours; use within 1 day.'
r=add(84,'Wallace Hot Mayonnaise Sauce',6,15,'A small yolk-and-oil sauce is thickened over hot water with vinegar and lemon, then seasoned for serving warm.',[yolks(3),oil(45),vinegar(15),lemon(5),water(60),salt(.25),pepper(.125)],
 ['Whisk {{yolks}} in a heatproof bowl. Add {{oil}} a few drops at a time while whisking until smoothly blended. Gradually whisk in {{vinegar}}, {{lemon}} and {{water}}, using warm water rather than pouring boiling water directly onto the yolks.',
 'Set the bowl over gently simmering water, keeping its base above the water. Whisk constantly until the sauce thickens and reaches 71°C (160°F), then immediately remove from heat. Do not let the sauce boil or the eggs scramble.',
 'Whisk in {{salt}} and {{pepper}} and serve warm in small portions with cooked fish or vegetables.',WARMEND],
 'The 1914 and 1928 entries reproduce the same formula and method. Modern tablespoons and a quarter cup become 45 ml oil, 15 ml vinegar and 60 ml water. The teaspoon lemon juice appears in both ingredient lists but is omitted from both methods; it is explicitly incorporated with the other liquids here. Salt, pepper, six small servings and time are supplied. The optional parsley is retained as a full variation. Temperature checking and controlled warm-water addition are modern handling details.');eggsource(r);r['source']+=' Egg-dish endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
variant(r,'parsley','With chopped parsley',copy.deepcopy(r['ingredients'])+[I('parsley',3,'g','fresh parsley, finely chopped','Use the same weight of finely chopped chives.')],r['steps'][:-1]+['Stir in {{parsley}} immediately before serving.']+[WARMEND])
merge(82,r,'Same complete hot-mayonnaise formula across the 1914 and 1928 Wallace books, including three yolks, three tablespoons oil, vinegar, lemon and hot water; parsley option retained.')

def creamitems():return [I('cream',90,'ml','cold whipping cream, at least 35% fat, measured before whipping','Use the same volume of cold heavy cream.'),I('whippedportion',120,'ml','whipped cream reserved from the cream above; not an additional purchase','Measure after whipping; liquid cream and whipped cream volumes are not interchangeable.')]
CREAMPREP='Whip {{cream}} in a separate chilled bowl until soft peaks hold. Gently spoon into a measuring jug without pressing it down and reserve {{whippedportion}}. Refrigerate any extra whipped cream separately and use within 1 day.'
CREAMEND='Fold the measured whipped cream into the sauce just before serving. Keep covered at 4°C (40°F) or colder and use within 1 day; the cream gradually loses volume. Refrigerate within 2 hours of preparation.'

r=add(83,'Wallace Boiled Mayonnaise Dressing',6,20,'Yolks, mustard, vinegar and lemon are cooked gently, then enriched with oil and a little cream.',[yolks(3),vinegar(30),lemon(30),I('mustard',.5,'tsp','prepared smooth mustard','Use the same amount of prepared Dijon mustard.'),salt(.5),pepper(.0625),I('sugar',.25,'tsp','white sugar','Use the same amount of caster sugar.'),oil(30),I('thincream',15,'ml','pouring cream for thinning','Use the complete lemon-thinned variation instead.')],
 ['Whisk {{yolks}}, {{mustard}}, {{salt}}, {{pepper}}, {{sugar}}, {{vinegar}} and {{lemon}} in a heatproof bowl. Set over gently simmering water, keeping the bowl above the water. Whisk constantly until thickened and at least 71°C (160°F), then remove from heat immediately.',
 'Gradually whisk in {{oil}} off the heat until smooth. Stir in {{thincream}} just before serving to loosen the sauce.',WARMEND],
 'The printed recipe 633 differs between its Finnish and English columns: Finnish gives three tablespoons oil or butter, English two. This base follows the English two-tablespoon oil amount, 30 ml; full variations retain the Finnish 45 ml amount and both butter quantities. Three yolks, two tablespoons each vinegar and lemon, and half teaspoon each mustard and salt are retained. Pepper, sugar and 15 ml thinning liquid are modern working amounts. Prepared mustard is the chosen form because the source does not specify powder. The full one-yolk-and-flour economy alternative, omitted from the extracted entry, is included. Six small condiment servings and timing are estimates.');eggsource(r);r['source']+=' Egg-dish endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='oil':i['amount']=45
variant(r,'finnish-oil','Finnish column — three tablespoons oil',vi,copy.deepcopy(r['steps']))
for a,id,label in [(28,'english-butter','English column — with butter'),(42,'finnish-butter','Finnish column — with butter')]:
 vi=copy.deepcopy(r['ingredients'])
 for i in vi:
  if i['key']=='oil':i.update(key='butter',amount=a,unit='g',name='unsalted butter, cut into small pieces',substitution='Use the corresponding oil variation if preferred.')
 variant(r,id,label,vi,[s.replace('Gradually whisk in {{oil}} off the heat','Whisk in {{butter}} a few pieces at a time off the heat') for s in r['steps']])
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='thincream':i.update(key='thinlemon',name='additional lemon juice for thinning',substitution='Use the cream-thinned base recipe for a less acidic sauce.')
variant(r,'lemon-thinned','Thinned with lemon juice',vi,[s.replace('{{thincream}}','{{thinlemon}}') for s in r['steps']])
ei=[i for i in copy.deepcopy(r['ingredients']) if i['key'] not in ['yolks','oil']]+[yolks(1),I('butter',28,'g','unsalted butter','Use the same weight of salted butter and reduce the added salt.'),I('flour',3,'g','plain wheat flour','Use the same weight of a plain gluten-free flour blend; thickening may differ.')]
es=['Melt {{butter}} in a small saucepan over gentle heat. Stir in {{flour}} and cook for 1 minute without browning. Gradually whisk in {{vinegar}} and {{lemon}}, then add {{mustard}}, {{salt}}, {{pepper}} and {{sugar}}. Simmer gently for 3 minutes, stirring until smooth.',
 'Whisk {{yolks}} in a heatproof bowl. Slowly whisk some of the hot sauce into the yolk, then return the mixture to the saucepan. Set over very gentle heat and stir continuously until it reaches 71°C (160°F), then remove immediately; do not boil.',
 'Stir in {{thincream}} just before serving.',WARMEND]
variant(r,'economy-cream','One-yolk flour version — cream finish',ei,es)
vi=copy.deepcopy(ei)
for i in vi:
 if i['key']=='thincream':i.update(key='thinlemon',name='additional lemon juice for thinning',substitution='Use the economy cream version for a less acidic sauce.')
variant(r,'economy-lemon','One-yolk flour version — lemon finish',vi,[s.replace('{{thincream}}','{{thinlemon}}') for s in es]);r['notes']+=' Butter working weights use 14 g per modern tablespoon. The economy variant chooses the English 28 g butter quantity and represents the source teaspoon flour by 3 g. Tempering and heating the added yolk replace simply stirring it into the cooked mixture off the heat. Economy portions are slightly smaller at the same serving count.'

r=add(86,'Wallace Mayonnaise Dressing No. 1',15,15,'A one-yolk mayonnaise combines olive oil, lemon juice, tarragon vinegar and mustard, with complete cream and colored variations.',[yolks(1),oil(180),lemon(15),I('vinegar',7.5,'ml','tarragon vinegar','Use the same volume of white wine vinegar.'),salt(.5),mustard(.5),cayenne()],
 ['Whisk {{yolks}} and {{mustard}} in a clean bowl. Measure {{oil}} into a jug and add a few drops at a time while whisking. Once the mixture thickens, continue in a thin stream, alternating with small additions of {{lemon}} and {{vinegar}} until all are incorporated.',
 'Whisk in {{salt}} and {{cayenne}} at the end. The sauce should be smooth and creamy. If oil pools, stop pouring and whisk until it blends in before continuing.',COLD],
 'The 1914 recipe and the 1928 recipe 631 share the same full base formula. Three-quarters of a modern 240 ml cup becomes 180 ml oil; half a tablespoon vinegar becomes 7.5 ml. One-sixteenth teaspoon cayenne is a supplied amount for the unspecified little cayenne. Fifteen small condiment servings and time are estimates. White, green and red versions retain the full source alternatives. The white variation makes more sauce at the same serving count because whipped cream increases its volume.');eggsource(r)
variant(r,'white-cream','White mayonnaise with whipped cream',copy.deepcopy(r['ingredients'])+creamitems(),r['steps'][:-1]+[CREAMPREP,CREAMEND])
gi=copy.deepcopy(r['ingredients'])+[I('spinach',10,'g','fresh spinach leaves, washed and dried','Use the same weight of extra watercress.'),I('watercress',10,'g','fresh watercress leaves, washed and dried','Use the same weight of extra spinach.'),I('parsley',5,'g','fresh parsley leaves, washed and dried','Use the same weight of chervil.'),I('greenlemon',10,'ml','additional lemon juice for extracting the green color','Use the same volume of drinking water for less acidity.')]
gs=r['steps'][:-1]+['Finely chop {{spinach}}, {{watercress}} and {{parsley}}. Pound them with {{greenlemon}} in a mortar, or process in a small blender until thoroughly broken down. Press through a clean fine cloth over a bowl, collecting the juice and discarding the coarse fibers. Stir the extracted juice into the mayonnaise just before serving.','Cover and refrigerate at 4°C (40°F) or colder and use within 1 day.']
variant(r,'green-herbs','Green mayonnaise with strained herb juice',gi,gs)
ri=copy.deepcopy(r['ingredients'])+[I('tomato',30,'ml','plain unsalted canned tomato puree, passed through a fine sieve','Use the same volume of strained plain tomato passata.')]
rs=r['steps'][:-1]+['Stir {{tomato}} into the mayonnaise until evenly tinted. The natural color will be pale pink rather than bright red.','Cover and refrigerate at 4°C (40°F) or colder and use within 2 days.']
variant(r,'red-tomato','Tomato-tinted mayonnaise',ri,rs)
variant(r,'red-colored','Tomato mayonnaise with added red color',copy.deepcopy(ri)+[I('redcolor',2,'drops','food-safe red liquid coloring','Use the uncolored tomato variation if preferred.')],rs[:-1]+['Stir in {{redcolor}} for a stronger red tint.']+[rs[-1]])
r['notes']+=' The source half cup of cream is measured AFTER whipping, supplied as a reserved 120 ml portion from 90 ml liquid cream with any surplus accounted for. Herb, extracting juice and tomato quantities are supplied modern working amounts. The 1914 red version also suggests carmine; a separate optional food-coloring variation retains that presentation without making added color essential.'
merge(85,r,'Same full Wallace one-yolk mayonnaise formula and method as1928No631; 1914 cream, green-juice and red-color alternatives retained in canonical86.')
merge(89,r,'Repeated base extraction of the same1914Wallace mayonnaise paragraph, corresponding to1928No631; canonical86 retains the complete accompanying variations.')

r=add(87,'Wallace Mayonnaise Dressing No. 2',24,35,'A sieved hard-boiled yolk enriches lemon mayonnaise, which is folded with whipped cream just before serving.',[eggs(1),water(500),yolks(1),salt(1),mustard(.5),I('sugar',.125,'tsp','white sugar','Use the same amount of caster sugar.'),oil(360),lemon(60)]+creamitems(),
 boil()+['Separate the firm cooked yolk and press it through a fine sieve into a clean bowl. Refrigerate the cooked white for another dish within 2 days. Mix the sieved yolk with {{salt}}, {{mustard}} and {{sugar}}, then whisk in {{yolks}} until smooth.',
 'Measure {{oil}} into a jug and whisk it in a few drops at a time, then in a thin stream as the sauce thickens. Gradually whisk in {{lemon}} until smooth. Stop adding oil whenever it pools and whisk until it blends in before continuing.',CREAMPREP,CREAMEND],
 'Both entries reproduce Wallace recipe 632. The shorter entry omits the whipped cream, which appears in both languages of the full original and is restored here. One-and-a-half modern cups oil becomes 360 ml and four tablespoons lemon juice becomes 60 ml. A dash of sugar is standardized to one-eighth teaspoon. The original does not give a cream amount; 120 ml measured whipped cream is an explicit working addition, supplied from 90 ml liquid cream with surplus accounted for. Full hard-boiled egg preparation, twenty-four small condiment servings and timing are supplied.');eggsource(r)
merge(88,r,'Same complete Wallace No632 formula with cooked and raw yolks,1.5cups oil and4tablespoons lemon; canonical87 restores the whipped-cream finish omitted by88.')

assert len(newids)==4 and len(merges)==4
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Wallace primary-source formulas, complete measured variants and cooking/cream methods','repair-batch-036.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-merge',aliases[s['id']]['reason'],'repair-batch-036.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))
