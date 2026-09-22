"""Complete nine Canadian dressings and salads from verified primary scans."""
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

r=add(158,'Canadian Sweet Mustard Dressing for Cabbage',24,45,'A sweet, tangy egg dressing is thickened with a little flour and enriched with cream and butter.',[vinegar(180),sugar(4),whole(1),salt(1),mustard(1),flour(1),cream(30),butter(50)],
 ['Whisk {{flour}} with {{cream}} in a small bowl until completely smooth. In a saucepan, whisk {{eggs}}, {{sugar}}, {{salt}} and {{mustard}}, then gradually whisk in {{vinegar}} and the flour-cream mixture.',
  'Add {{butter}} in small pieces and cook over low heat, whisking constantly, until the butter melts and the dressing thickens. Bring just to a gentle bubbling, cook for about 1 minute while whisking and check that the egg mixture has reached at least 71°C (160°F). Remove promptly; do not let it boil hard or catch on the pan.',COOL,
  'Stir the cold dressing and spoon over finely shredded cabbage just before serving, adding only enough to coat the amount of salad being prepared.',DAY],
 'The scanned Mrs. John Forsyth recipe gives three-quarter cup vinegar, four tablespoons sugar, one egg, one teaspoon salt, about one teaspoon each mustard and flour, two tablespoons cream and egg-size butter. The full scan confirms the 180 ml vinegar and flour mixed smooth with cream. The unstandardized butter size becomes a chosen 50 g; this is not a recovered weight. The terse mixing order is expanded to incorporate every ingredient. Twenty-four small dressing portions and total time including cooling are estimates.');tagged(r)

r=add(166,'Canadian Brown-Sugar Double-Boiler Dressing',24,50,'Brown sugar and mustard flavor a cooked egg dressing, with diluted vinegar and a little butter for a gentler texture.',[whole(2),sugar(4,brown=True),mustard(2),salt(1.5),cayenne(),butter(15),flour(1),vinegar(80),water(160)],
 ['Whisk {{flour}}, {{sugar}}, {{mustard}}, {{salt}} and {{cayenne}} in a heatproof bowl. Beat in {{eggs}}, then gradually whisk in {{vinegar}} and {{water}}. Add {{butter}} in small pieces.',
  'Set the bowl over gently simmering water with its base above the water. Whisk continuously until the butter melts and the dressing thickens enough to coat a spoon, about 8–12 minutes. It must reach at least 71°C (160°F); continue stirring gently for about 2 minutes after thickening so the flour is cooked. Do not boil the egg mixture hard.',COOL,
  'Stir before using and add to a prepared salad just before serving.',DAY],
 'The scanned Mrs. Bell recipe specifies one cup mixed vinegar and water with more water than vinegar, but no ratio. The chosen 80 ml vinegar plus 160 ml water totals a modern 240 ml cup and satisfies that instruction. Walnut-size butter is represented by a working 15 g. The two eggs, four tablespoons brown sugar, two teaspoons mustard, one-and-a-half teaspoons salt, one teaspoon flour and water-bath method are retained. Cayenne, twenty-four portions and timing are supplied.');tagged(r)

DI=[sugar(3),mustard(2),salt(.5),butter(50),yolks(1),flour(1,'tbsp'),milk(120),vinegar(15),I('white',30,'g','commercially pasteurized egg white suitable for whipping, about one large white','Use a pasteurized shell-egg white of the same weight; do not use unpasteurized raw white.')]
DS=['Mix {{flour}}, {{sugar}}, {{mustard}} and {{salt}} in a heatproof bowl. Whisk in {{yolks}} and {{milk}} until smooth, then add {{butter}} in small pieces.',
 'Set over gently simmering water, keeping the bowl above the water, and stir continuously until the butter melts and the mixture thickens, about 8–12 minutes. Check that it reaches at least 71°C (160°F), then stir gently for about 2 minutes after thickening to cook the flour. Remove from heat.',
 'Warm {{vinegar}} in a small pan until hot but not boiling and stir it gradually into the thick dressing.',COOL,
 'When the dressing is fully cold, whisk {{white}} in a clean bowl until it holds soft peaks. Fold it gently into the dressing. Keep cold and use the same day; the air will gradually subside.']
r=add(167,'Canadian Fluffy Milk-and-Mustard Dressing',20,55,'A cooked milk, yolk and butter dressing is finished with warm vinegar, cooled, then lightened with whipped pasteurized egg white.',DI,DS,
 'The scanned Mrs. I. C. Dickson recipe gives three tablespoons sugar, two teaspoons mustard, half a teaspoon salt, egg-size butter, one yolk, one tablespoon flour, eight tablespoons milk and one tablespoon heated vinegar. The butter is restored explicitly to the cooking method. A working 50 g butter, 120 ml milk and 15 ml vinegar are used. The white is folded in only after the dressing is cold; commercially pasteurized whipping white replaces the original unspecified raw white. Twenty portions and fifty-five minutes including cooling are estimates.');tagged(r);eggsource(r)

r=add(168,'Canadian Vinegar-and-Cream Egg Dressing',32,50,'A sharp vinegar-and-egg base is sweetened, gently cooked and finished with cream for a smooth salad dressing.',[vinegar(240),whole(2),sugar(120,'ml'),salt(1),pepper(.5),cream(120)],
 ['Beat {{eggs}}, {{sugar}}, {{salt}} and {{pepper}} in a heatproof bowl. Heat {{vinegar}} in a small saucepan until steaming but not boiling, then pour it very gradually into the eggs while whisking continuously.',
  'Set the bowl over gently simmering water with the bowl above the water. Whisk until the mixture coats a spoon and reaches 71°C (160°F), about 5–10 minutes; remove promptly before it scrambles. Pouring hot vinegar over eggs alone does not verify that the eggs are cooked.',
  'Gradually stir in {{cream}} until smooth.',COOL,'Stir and spoon over the prepared salad shortly before serving.',DAY],
 'The printed Mrs. Byron Jenvey formula has HALF a cup sugar and HALF a teaspoon pepper, not the extracted three-quarter cup and one-sixth teaspoon. The scan also confirms one cup vinegar, two eggs, one teaspoon salt and half a cup cream. Modern measures are 240 ml vinegar, 120 ml sugar measured by volume and 120 ml cream. The sugar has not been mislabeled as a liquid or converted to an unsupported gram weight. The source’s hot-vinegar tempering is retained and a complete water-bath cooking endpoint is added. Thirty-two small portions and timing are estimates.');tagged(r)

RI=[flour(1,'tbsp'),butter(14),milk(240),sugar(1),salt(.5),mustard(1),I('paprika',.25,'tsp','sweet paprika','Use the complete red-pepper variation for the source’s hotter option.'),whole(1),vinegar(120)]
RS=['Melt {{butter}} in a small saucepan over medium-low heat. Stir in {{flour}} and cook for about 1 minute without browning. Gradually whisk in {{milk}} until smooth. Bring to a gentle simmer and stir for 2 minutes to cook the flour.',
 'In a heatproof bowl, whisk {{eggs}}, {{sugar}}, {{salt}}, {{mustard}} and {{paprika}}. Whisk a few spoonfuls of the hot milk sauce into the egg mixture, then gradually return this mixture to the saucepan while stirring.',
 'Cook over low heat, stirring constantly, until thickened and at least 71°C (160°F). Remove from heat and gradually whisk in {{vinegar}}. Do not add the vinegar to the milk before making the sauce.',COOL,'Stir before spooning over the prepared salad.',DAY]
r=add(169,'Canadian Roux-Based Paprika Salad Dressing',28,50,'A milk-and-butter sauce is enriched with egg and mustard, then finished with paprika and vinegar after thickening.',RI,RS,
 'The scanned Mrs. M. B. Rawlston recipe specifies HALF a teaspoon salt and QUARTER a teaspoon paprika or red pepper, not three-quarter teaspoon amounts. Half a cup vinegar is also confirmed. The flour-and-butter milk sauce is made first, the seasoned egg is tempered in next, and vinegar is added last. A tablespoon butter is represented by a modern working 14 g; milk and vinegar are 240 ml and 120 ml. Twenty-eight small portions and timing are estimates.');tagged(r)
vi=copy.deepcopy(RI)
for i in vi:
 if i['key']=='paprika':i.update(key='redpepper',name='ground cayenne pepper, the hotter red-pepper option',substitution='Use the sweet-paprika base recipe for a mild dressing.')
variant(r,'red-pepper','With the source’s hotter red-pepper option',vi,[s.replace('{{paprika}}','{{redpepper}}') for s in RS])

CI=[whole(2),mustard(1),salt(.5),butter(15),sugar(120,'ml'),pepper(.125),vinegar(120),milk(60)]
CS=['Whisk {{eggs}}, {{mustard}}, {{salt}}, {{sugar}} and {{pepper}} in a heatproof bowl. Gradually whisk in {{vinegar}} and add {{butter}} in small pieces.',
 'Set over gently simmering water, keeping the bowl above the water, and stir continuously until the butter melts and the dressing thickens enough to coat a spoon, about 8–12 minutes. Check that it reaches at least 71°C (160°F), then remove without boiling the egg mixture hard.',
 'Gradually stir in {{milk}} to loosen the dressing.',COOL,'Use to dress cold cooked chicken or another prepared salad just before serving.',DAY]
r=add(170,'Canadian Cooked Dressing for Chicken Salad',24,50,'A sweet mustard-and-vinegar egg dressing is thinned with milk or cream after cooking for use with cold chicken salad.',CI,CS,
 'The scanned Miss Florence Campbell recipe has HALF a teaspoon salt and HALF a cup sugar, not three-quarter amounts. The method’s half cup vinegar is restored explicitly before cooking. Nut-size butter becomes a working 15 g and the unspecified thinning milk or cream becomes 60 ml, with both options supplied in full. The modern half-cup sugar measure is 120 ml by volume, not a liquid ingredient or claimed weight. Pepper, twenty-four dressing portions and timing are supplied.');tagged(r)
vi=[cream(60) if i['key']=='milk' else copy.deepcopy(i) for i in CI]
variant(r,'cream','Thinned with cream',vi,[s.replace('{{milk}}','{{cream}}') for s in CS])

r=add(171,'Canadian Rich Cream-and-Mustard Dressing',60,55,'Cream, eggs, mustard and melted butter make a rich cooked dressing, with vinegar added gradually before a gentle water-bath cook.',[I('butter',45,'ml','unsalted butter, measured after melting','Use the same measured melted volume of salted butter and reduce the added salt.'),sugar(1),mustard(6),salt(3),I('starch',.5,'tsp','cornstarch','Use the same volume of arrowroot powder; thickening may vary.'),whole(4),cream(480),vinegar(220)],
 ['Melt enough butter to measure {{butter}}, then let it cool until just warm. In a heatproof bowl, mix {{sugar}}, {{mustard}}, {{salt}} and {{starch}}, then stir in the measured melted butter until smooth.',
  'Beat {{eggs}} separately and whisk them into the butter mixture gradually. Whisk in {{cream}}, then add {{vinegar}} a little at a time while whisking.',
  'Set the bowl over gently simmering water with its base above the water. Stir continuously, scraping the bottom and sides, until it thickens like pouring cream and reaches at least 71°C (160°F), about 12–18 minutes. Remove promptly; do not let the egg-and-cream mixture boil hard.',COOL,
  'Stir and use small portions to dress prepared salads; this is a strongly seasoned dressing.',DAY],
 'The full scanned Estelle M. Record recipe runs across pages172–173: three tablespoons MELTED butter, two tablespoons mustard, one tablespoon salt, half a teaspoon cornstarch, four eggs, one pint cream and one scant cup vinegar. Sugar appears only in the method and has no printed amount; this adaptation deliberately supplies one modern tablespoon, not a recovered measurement. Butter stays a melted volume of 45 ml. The pint is represented by two modern 240 ml cups, 480 ml, and scant cup vinegar by a chosen 220 ml; these are working modern measures, not proof of the book’s historical pint/cup capacity. The substantial source mustard and salt remain six and three modern teaspoons. Sixty small portions and timing are estimates.');tagged(r)

BI=[I('beets',800,'g','raw beetroot, similar-sized roots','Use the ready-cooked beet variation if preferred.'),water(1500,'beetwater'),vinegar(240),salt(.125),sugar(2,'tsp'),mustard(2),whole(1)]
BS=['Scrub {{beets}} and trim the leaves, leaving about 2 cm of stalk and the root tips intact. Put in a saucepan with {{beetwater}}, adding more drinking water only if necessary to cover. Bring to a boil, cover and simmer for about 35–60 minutes until a skewer enters the largest beet easily.',
 'Drain and cool just enough to handle safely, then rub or peel away the skins and trim the ends. Chop the cooked beetroot into small pieces, as the scanned recipe directs, and place in a clean shallow serving bowl.',
 'Whisk {{eggs}}, {{sugar}}, {{mustard}} and {{salt}} in a heatproof bowl, then gradually whisk in {{vinegar}}. Set over gently simmering water with the bowl above the water and stir continuously until lightly thickened and at least 71°C (160°F), about 5–10 minutes. Remove promptly rather than boiling the egg mixture hard.',
 'Pour the warm dressing over the chopped beetroot and toss gently. Let the shallow bowl lose its heat briefly over ice water, then cover and refrigerate promptly for about 1 hour until cold. Serve chilled.',DAY]
r=add(172,'Canadian Chopped Beet Salad with Mustard Dressing',8,140,'Tender chopped beetroot is dressed with a tangy cooked egg-and-mustard sauce and chilled before serving.',BI,BS,
 'The scanned Maggie Ebbs recipe says beet cooked and CHOPPED, not the extracted sliced. It gives one cup vinegar, a pinch of salt, one dessertspoon each sugar and mustard and one egg, but no beet quantity. This complete salad uses a chosen 800 g raw beetroot and full cooking instructions. A dessertspoon is represented by two modern teaspoons, 10 ml, as an explicit working measure. Poaching water, salt, eight side servings and total time including chilling are supplied. A measured water-bath egg cook replaces the terse boil-all-together instruction.');tagged(r);r['category']='Salads'
vi=[i for i in copy.deepcopy(BI) if i['key']!='beetwater']
for i in vi:
 if i['key']=='beets':i.update(amount=700,name='plain cooked peeled beetroot, chilled and drained',substitution='Use the fresh-beet base recipe instead; pickled beetroot would add extra acidity.')
variant(r,'cooked-beets','Starting with cooked beetroot',vi,['Chop {{beets}} into small pieces and put in a clean shallow bowl. Keep refrigerated while preparing the dressing.']+BS[2:])

LI=[vinegar(120),water(120),sugar(120,'ml'),butter(5),whole(2),mustard(1),salt(.5),pepper(.5),I('pastevinegar',5,'ml','additional white wine vinegar for the mustard paste','Use the same volume of cider vinegar.'),I('cabbage',800,'g','green cabbage, trimmed weight','Use the complete lettuce variation if preferred.')]
LS=['Put {{vinegar}}, {{water}}, {{sugar}} and {{butter}} in a small saucepan. Heat gently, stirring until the sugar dissolves and the butter melts, then bring just to a simmer.',
 'Beat {{eggs}} in a heatproof bowl. In a small dish, mix {{mustard}}, {{salt}} and {{pepper}} with {{pastevinegar}} to make a smooth paste, then whisk the paste into the eggs.',
 'Whisk the hot vinegar mixture into the eggs slowly in a thin stream. Return to the saucepan and stir over low heat until lightly thickened and at least 71°C (160°F). Remove promptly without boiling hard.',COOL,
 'Wash {{cabbage}}, remove the core and shred finely. Just before serving, toss the cold dressing with the shredded cabbage until evenly coated. Serve immediately for crisp cabbage.',DAY]
r=add(173,'Canadian Cabbage Salad with Sweet Cooked Dressing',8,50,'Finely shredded cabbage is tossed with a chilled sweet-and-tangy egg dressing flavored with mustard and black pepper.',LI,LS,
 'The scanned Mrs. G. A. Scott recipe specifies HALF a cup each vinegar, water and white sugar, and HALF a teaspoon each salt and black pepper. This corrects the extracted three-quarter cup water, full cup sugar and three-quarter teaspoon pepper. The three half-cups become 120 ml each, with sugar explicitly a dry ingredient measured by volume. The additional little vinegar for the mustard paste becomes a working 5 ml; it is not silently added to the main vinegar quantity. The source names lettuce or cabbage, then directs finely chopped cabbage; a chosen 800 g cabbage makes a complete eight-serving salad and a full lettuce version preserves the alternative. Five grams butter and timing are modern choices.');tagged(r);r['category']='Salads'
vi=copy.deepcopy(LI)
for i in vi:
 if i['key']=='cabbage':i.update(key='lettuce',amount=600,name='tender lettuce leaves, trimmed weight',substitution='Use the cabbage base recipe instead.')
vs=LS[:-2]+['Wash {{lettuce}}, dry thoroughly and tear into bite-size pieces. Toss with the cold dressing immediately before serving, adding it gradually so the leaves remain lightly coated. Refrigerate any extra dressing separately for use within 2 days.']+[DAY]
variant(r,'lettuce','With lettuce instead of cabbage',vi,vs)

assert len(newids)==9 and len(merges)==0
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Canadian source scans correct fractions and complete cooking methods, quantities and alternatives','repair-batch-045.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

