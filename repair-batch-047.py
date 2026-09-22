"""Complete eight European and American dressings with full source variations."""
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

DAY='Cover and refrigerate promptly at 4°C (40°F) or colder. Use within 2 days and refrigerate within 2 hours of preparation.'
COOL='Transfer to a clean shallow bowl and set over a larger bowl of cold water, keeping water out of the dressing. Stir until no longer warm, then cover and refrigerate for about 30 minutes until cold.'
REF=' Modern egg cooking endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
def whole(n):return I('eggs',n,'','large eggs','Use the same number of large pasteurized shell eggs if preferred.')
def sugar(a,u='tbsp',brown=False):return I('sugar',a,u,'soft brown sugar' if brown else 'white sugar','Use the same volume of caster sugar; brown sugar gives a different flavor.' if not brown else 'Use the same volume of white sugar for a less caramel-like flavor.')
def butter(a):return I('butter',a,'g','unsalted butter','Use the same weight of salted butter and reduce the added salt.')
def milk(a):return I('milk',a,'ml','whole milk','Use the same volume of lactose-free dairy milk.')
def cream(a):return I('cream',a,'ml','pouring cream','Use the same volume of lactose-free dairy cream.')
def flour(a,u='tsp'):return I('flour',a,u,'plain wheat flour','Use the same volume of a plain gluten-free flour blend; thickening may vary.')
def tagged(r):r['source']+=REF;return r

def prepared(a,u='tsp'):return I('mustard',a,u,'prepared Dijon mustard','Use the same volume of another smooth prepared mustard.')
def coldserve():return 'Stir before using and spoon over the prepared salad just before serving.'
def bath():return 'Set the bowl over gently simmering water, keeping its base above the water. Whisk continuously until the dressing coats a spoon and reaches at least 71°C (160°F), about 8–12 minutes. Remove promptly without boiling the egg mixture hard.'

YOLK='Separate the firm cooked yolks and press through a fine sieve into a mixing bowl. Refrigerate the cooked whites for another dish and use within 2 days.'
HI=[eggs(2),water(1000),mustard(.5),vinegar(30),cream(240),salt(.25),pepper(.125),sugar(.5,'tsp')]
HS=boil()+[YOLK,'Mash {{mustard}}, {{salt}}, {{pepper}} and {{sugar}} into the sieved yolks. Work in {{vinegar}} until the paste is smooth.','Gradually stir in {{cream}}, a little at a time, until evenly combined. The cream is poured in without whipping. Serve cold over the prepared salad.',DAY]
r=add(180,'Wallace Cooked-Yolk Cream Dressing',20,30,'Hard-boiled yolks, mustard and vinegar form a smooth paste that is loosened gradually with cream.',HI,HS,
 'The full 1914 bilingual recipe has two hard-boiled yolks, half a teaspoon mustard, two tablespoons vinegar and one cup cream. It does not instruct whipping the cream. This adaptation uses modern 30 ml vinegar and 240 ml cream and supplies quarter teaspoon salt, one-eighth teaspoon pepper and half a teaspoon sugar. The unspecified mustard is represented by dry mustard. Egg boiling, handling the unused whites and short refrigerated storage are supplied. Twenty small dressing portions and timing are estimates. This differs from the later Wallace dressing in its acid formula and cream treatment.');tagged(r)

CI=[mustard(.5),salt(1),sugar(1,'tsp'),whole(2),cream(240),lemon(30),butter(28),pepper(.125)]
CS=['Mix {{mustard}}, {{salt}}, {{sugar}} and {{pepper}} in a heatproof bowl. Beat {{eggs}} separately, then whisk them in with {{lemon}} and {{cream}}.',bath(),'Remove from the heat and beat in {{butter}} in small pieces until fully melted and smooth.',COOL,coldserve(),DAY]
r=add(181,'Wallace Cooked Lemon-and-Butter Dressing',26,55,'Eggs and lemon thicken a cream dressing in a water bath, with butter beaten in after cooking.',CI,CS,
 'The 1928 source specifies half a teaspoon mustard, one teaspoon each salt and sugar, two whole eggs, one cup cream or milk, the juice of one lemon and two tablespoons butter. The measured base uses modern 240 ml cream, working 30 ml lemon juice and 28 g butter, with one-eighth teaspoon pepper supplied. Butter is added AFTER the egg mixture is cooked, as the source requires. Both dairy options have complete methods. Twenty-six small portions and the time including cooling are estimates.');tagged(r)
variant(r,'milk','Made with milk',[milk(240) if i['key']=='cream' else copy.deepcopy(i) for i in CI],[s.replace('{{cream}}','{{milk}}') for s in CS])

WI=[eggs(2),water(1000),prepared(.5),vinegar(15),lemon(30),I('cream',240,'ml','cold heavy whipping cream, measured before whipping','Use the same volume of lactose-free dairy whipping cream.'),salt(.25),pepper(.125),sugar(.5,'tsp')]
WS=boil()+[YOLK,'Mash {{mustard}}, {{salt}}, {{pepper}} and {{sugar}} into the sieved yolks. Gradually work in {{vinegar}} and {{lemon}} to make a smooth paste. Let the paste cool completely.','Whip {{cream}} in a chilled bowl until it holds soft peaks. Stir a spoonful into the cold yolk paste, then gently fold in the remaining measured cream. Serve cold over the prepared salad.',DAY]
r=add(182,'Wallace Lemon Dressing with Whipped Cream',24,35,'A paste of cooked yolks, prepared mustard, vinegar and lemon is lightened with softly whipped cream.',WI,WS,
 'The scanned bilingual page238 specifies HALF a teaspoon prepared mustard, not the extracted one-and-a-half teaspoons. Two hard-boiled yolks, one tablespoon vinegar, two tablespoons lemon juice and one cup cream are retained as modern 15 ml, 30 ml and 240 ml. Cream is measured liquid before whipping as an explicit working choice. The English method calls for whipped cream; the Finnish method says to add cream gradually without specifying whipping, so a complete unwhipped variation is retained. Salt, pepper and sugar are supplied. The separate oil-lemon-cream alternative has its own complete egg-free variation, not extra steps appended to the egg recipe. Twenty-four small portions and timing are estimates.');tagged(r)
variant(r,'unwhipped','With unwhipped cream, following the Finnish method',[cream(240) if i['key']=='cream' else copy.deepcopy(i) for i in WI],WS[:3]+['Gradually stir in {{cream}}, without whipping, until the dressing is smooth. Serve cold over the prepared salad.',DAY])
variant(r,'egg-free','The source’s separate egg-free oil and lemon dressing',[oil(120),lemon(110),cream(240),salt(.25),sugar(.5,'tsp')],['Whisk {{lemon}}, {{salt}} and {{sugar}} until the seasonings dissolve. Gradually whisk in {{oil}} until blended.','Add {{cream}} very gradually while whisking, then serve promptly over the prepared salad. This is a loose cream dressing; whisk again if it separates.',DAY])
r['notes']+=' In the egg-free alternative, the printed half cup oil becomes 120 ml and the scant half cup lemon juice is a working 110 ml; cream is 240 ml. Mustard and pepper are not in that separate source formula. At the shared 24-serving setting it makes larger portions than the whipped-yolk base.'

SI=[salt(.25),I('paprika',.0625,'tsp','sweet paprika','Use the same amount of smoked paprika for a different flavor, or omit.'),sugar(.5,'tsp'),vinegar(22.5),oil(60)]
SS=['Whisk {{salt}}, {{paprika}}, {{sugar}} and {{vinegar}} in a small bowl until the salt and sugar dissolve.','Just before serving, whisk in {{oil}} a little at a time. Spoon over the prepared green or potato salad and toss to coat. Serve immediately; whisk again if the oil separates.',STORE]
r=add(183,'Idun Paprika Salad Dressing',6,5,'A lightly sweet oil-and-vinegar dressing combines paprika with a small amount of sugar and salt.',SI,SS,
 'Idun recipe448 explicitly serves six. Quarter teaspoon salt, half a teaspoon sugar, one-and-a-half tablespoons vinegar and four tablespoons oil are retained using modern 22.5 ml vinegar and 60 ml oil. The few grains of paprika become a working one-sixteenth teaspoon. The source mixes spices with vinegar before adding oil just before serving. Its optional teaspoon French mustard for fish or lobster salad is preserved as a complete variation. Five minutes is an estimate; the six portions follow the printed yield. This is distinct from the earlier sweet paprika dressing in its oil-to-vinegar and seasoning ratios.')
variant(r,'french-mustard','With French mustard for fish or lobster salad',copy.deepcopy(SI)+[prepared(1)],['Whisk {{salt}}, {{paprika}}, {{sugar}}, {{mustard}} and {{vinegar}} in a small bowl until evenly mixed.','Just before serving, gradually whisk in {{oil}}. Spoon over the prepared chilled fish or lobster salad and toss gently. Serve immediately; whisk again if the oil separates.',STORE])

r=add(184,'Beeton Uncooked Milk-and-Mustard Dressing',8,10,'Prepared mustard and sugar are blended with oil, then milk and vinegar are added gradually for a thin, tangy dressing.',[prepared(1),sugar(1,'tsp'),oil(30),milk(60),vinegar(30),salt(.25),cayenne()],
 ['Mix {{mustard}} and {{sugar}} in a small bowl. Measure {{oil}} into a jug and beat it in drop by drop at first, then in a thin stream, until evenly blended.','Gradually beat in {{milk}}, then add {{vinegar}} a little at a time, stirring well after each addition. Keep the mixture cool. This is a thin dressing rather than a thick mayonnaise; acid may make the milk slightly grainy.','Stir in {{salt}} and {{cayenne}} last. Use promptly on the prepared salad, whisking again before serving.',DAY],
 'The complete recipe506 specifies mixed mustard, interpreted as prepared mustard, and one teaspoon sugar, two tablespoons oil, four tablespoons milk and two tablespoons vinegar. These liquid amounts become modern 30 ml, 60 ml and 30 ml. Salt and cayenne are supplied as quarter and one-sixteenth teaspoons. The oil, milk, vinegar and final seasoning order is retained. This method is uncooked and does not promise that gradual mixing will prevent all acid-related milk separation. Eight small dressing portions and ten minutes are estimates.')

r=add(185,'Beeton Peppery Cooked-Yolk Salad Dressing',12,30,'Four hard-boiled yolks make a rich mustard-and-cream dressing, sharpened with vinegar and seasoned with white pepper and cayenne.',[eggs(4),water(1200),prepared(1),I('pepper',.25,'tsp','ground white pepper','Use the same amount of ground black pepper.'),I('cayenne',.125,'tsp','ground cayenne pepper','Reduce or omit for a milder dressing.'),salt(.25),cream(60),vinegar(45)],
 boil()+['Separate the firm cooked yolks and pound in a mortar until smooth. Slice the cooked whites into rings and refrigerate them for the salad garnish.','Work {{mustard}}, {{pepper}}, {{cayenne}}, {{salt}} and {{cream}} into the yolk paste until evenly combined.','Add {{vinegar}} very gradually, stirring well after each addition, to loosen the dressing. The final thickness depends on egg size and cream; the measured adaptation makes a spoonable dressing. Spoon over the prepared salad and garnish with the reserved cooked-white rings.',DAY],
 'The full source has four hard-boiled yolks, one teaspoon mixed mustard, quarter teaspoon white pepper, half that amount of cayenne and four tablespoons cream. Modern cream is 60 ml; unmeasured vinegar and salt become working 45 ml and quarter teaspoon. The source’s cooked-white-ring garnish is restored from the following note. The egg-boiling method and short refrigeration guidance are supplied. Twelve small portions and timing are estimates.');tagged(r)

r=add(186,'Farmer Chicken-Stock Salad Dressing',40,75,'Reduced chicken stock adds savory depth to a cooked five-yolk mustard dressing, strained smooth and finished with cream and melted butter.',[I('stock',240,'ml','unsalted cooked chicken stock','Use the same volume of unsalted turkey stock for a different flavor.'),vinegar(120),yolks(5),prepared(2,'tbsp'),salt(1),pepper(.25),cayenne(),cream(120),I('butter',80,'ml','unsalted butter, measured after melting','Use the same volume of melted salted butter and reduce the added salt.')],
 ['Put {{stock}} in a small saucepan and simmer uncovered until reduced to half its starting volume, about 10–15 minutes. Measure the reduced stock in a heatproof jug; return it to the pan briefly if more reduction is needed. Let cool until lukewarm.','In a heatproof bowl, whisk {{yolks}}, {{mustard}}, {{salt}}, {{pepper}} and {{cayenne}}. Gradually whisk in {{vinegar}} and the reduced stock.',bath(),'Strain the hot dressing through a fine sieve into a clean bowl. Gradually stir in {{cream}} and {{butter}} until evenly combined.',COOL,coldserve(),DAY],
 'The source begins with half a cup rich chicken stock AFTER reduction. This adaptation supplies 240 ml unsalted cooked stock and reduces it to 120 ml; the starting amount is a modern choice. Half a cup each vinegar and cream become 120 ml, and one-third cup melted butter is retained as 80 ml measured after melting. Five yolks, two tablespoons prepared mustard, one teaspoon salt and quarter teaspoon pepper are retained; cayenne is supplied. Straining occurs before cream and melted butter are added, and cooling follows, as printed. Forty small portions and the 75-minute total including reduction and cooling are estimates.');tagged(r)

r=add(187,'White House French Dressing with Grated Onion',5,5,'Finely grated onion gives bite to a simple three-to-one olive-oil and vinegar dressing.',[pepper(.125),salt(.25),oil(45),I('onion',1,'tbsp','peeled onion, finely grated','Use the same amount of finely grated shallot.'),vinegar(15)],
 ['Mix {{pepper}} and {{salt}} in a small bowl. Stir in {{oil}} and {{onion}} until evenly combined.','Add {{vinegar}} and whisk vigorously. Immediately pour over the prepared salad and toss until evenly coated.',STORE],
 'The source specifies three tablespoons oil, one level tablespoon scraped onion and one tablespoon vinegar. Modern liquid measures are 45 ml and 15 ml. Its saltspoon measures are not a verified modern standard; this adaptation chooses quarter teaspoon salt and one-eighth teaspoon pepper. The full tablespoon onion and oil-before-vinegar order are retained. This differs from the existing tarragon-and-onion dressing, which has tarragon vinegar, parsley and extracted onion juice. Five small portions and timing are estimates.')

assert len(newids)==8 and len(merges)==0
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full European and American dressing formulas, corrected mustard amount and complete dairy and egg-free alternatives','repair-batch-047.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

