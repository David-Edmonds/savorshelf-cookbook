"""Complete Viennese green, herb and aspic sauces from scanned source formulas."""
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
def gel(a=5):return I('gelatin',a,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the manufacturer’s equivalent setting amount of leaf gelatin, soaking and draining it first; agar is not a gram-for-gram substitute.')
def stock(a=250):return I('stock',a,'ml','clear unsalted veal stock, chilled','Use the same volume of clear unsalted chicken stock for a different flavor.')
GELPREP=['Sprinkle {{gelatin}} over {{stock|0.2}} in a small bowl and leave for 5 minutes. Warm the remaining {{stock|0.8}} in a saucepan, remove from heat, then stir in the bloomed gelatin and its stock until fully dissolved. Do not boil. Let cool, stirring occasionally, until barely warm and still liquid.']

GREENITEMS=[eggs(6),water(1500),I('spinach',50,'g','fresh spinach leaves, washed','Use the same weight of young chard leaves, removing tough stems.'),I('parsley',5,'g','fresh parsley sprigs','Use the same weight of extra chervil.'),I('chervil',5,'g','fresh chervil sprigs','Use the same weight of extra parsley.'),water(1000,'greenwater'),I('greensalt',.5,'tsp','fine salt for blanching water','Reduce or omit; the water is discarded.'),I('tarragon',1,'tbsp','fresh tarragon leaves, finely chopped','Use the same volume of chopped chervil for a milder flavor.'),I('sponge',120,'g','plain uniced egg sponge cake, without filling','Use the complete homemade-sponge variation, or the same weight of a plain gluten-free egg sponge.'),water(250,'soakwater'),salt(.5),I('sugar',1,'tsp','white sugar','Reduce or omit to taste.'),vinegar(30),oil(60)]
GREENSTEPS=boil()+['Separate the firm cooked yolks and press them through a fine sieve into a mixing bowl. Refrigerate the cooked whites separately for another dish and use within 2 days.',
 'Bring {{greenwater}} and {{greensalt}} to a boil. Add {{spinach}}, washed {{parsley}} and {{chervil}} and blanch for about 1 minute until wilted. Drain, refresh under cold running drinking water, then squeeze firmly in a clean cloth to remove excess water.',
 'Put {{sponge}} in a shallow bowl and briefly moisten with {{soakwater}}. Lift out and gently squeeze in a clean cloth or fine sieve to remove excess water; discard the soaking liquid. Do not leave it soaking until it dissolves.',
 'Pound the squeezed greens with {{tarragon}}, the sieved cooked yolks and the damp sponge in a mortar until smooth, working in batches if needed. Press through a fine sieve, scraping the smooth mixture into a clean bowl. Cover and refrigerate until serving.',
 'Just before serving, stir in {{salt}}, {{sugar}}, {{vinegar}} and {{oil}} until smoothly combined. The finished sauce is thick and spoonable; the source delays salt and vinegar to help preserve the green color.',DAY]
r=add(118,'Viennese Green Sauce with Egg Sponge and Herbs',20,45,'Blanched greens, cooked yolks and softened egg sponge make a thick herb sauce, finished with oil, vinegar and a little sugar.',GREENITEMS,GREENSTEPS,
 'The scanned No273 specifies 12 deka Biscuit, 120 g, not twelve teaspoons; it calls for sugar, not the extracted pepper. In the same book No1498 defines Biscuit-Torte as an egg, sugar and flour sponge, and No1503 uses Biscuit for pieces of that cake. Plain uniced egg sponge is therefore the chosen contextual interpretation, not an explicit cross-reference in No273 or an English buttery biscuit. Six cooked yolks and four modern tablespoons oil, 60 ml, are retained. A handful spinach becomes 50 g and the parsley/chervil sprigs become 5 g each. One unstandardized spoon of tarragon is represented by a modern tablespoon. Soaking/blanching water, salt, sugar, 30 ml vinegar, twenty small condiment servings and timing are working choices. The complete small sponge variation follows a sixth of the No1498 egg/flour/sugar proportions, with rounding and modern baking instructions.');eggsource(r)
vi=[i for i in copy.deepcopy(GREENITEMS) if i['key']!='sponge']+[I('cakeeggs',2,'','large eggs for the sponge','Use two large pasteurized shell eggs if preferred.'),I('cakesugar',47,'g','caster sugar for the sponge','Use the same weight of fine white sugar.'),I('cakeflour',40,'g','plain wheat flour','Use the same weight of a plain gluten-free baking blend; the sponge may be more fragile.'),I('cakebutter',3,'g','butter for greasing the tin','Use the same weight of neutral oil.'),I('spongeportion',120,'g','cooled sponge reserved from the cake below; not an additional purchase','Weigh after baking and cooling; keep any extra cake separately.')]
CAKE=['Heat the oven to 180°C (350°F). Line the base of a small round tin, about 15 cm across at the base yield, with baking paper and lightly grease with {{cakebutter}}. Separate {{cakeeggs}} into two clean bowls.',
 'Beat the cake yolks with {{cakesugar}} until thick and pale. With clean beaters, whisk the cake whites to firm peaks. Fold the whites gently into the yolk mixture in two additions, sifting {{cakeflour}} over it and folding just until no dry flour remains.',
 'Transfer to the tin and bake for about 18–25 minutes until golden, springy and a skewer inserted into the center comes out clean. Cool in the tin for 5 minutes, turn out onto a rack and cool completely. Weigh out {{spongeportion}} for the sauce; wrap any extra plain sponge for another use. Allow about 45 additional minutes for baking and cooling.']
variant(r,'homemade-sponge','With a small homemade egg sponge',vi,CAKE+[s.replace('{{sponge}}','the weighed reserved sponge') for s in GREENSTEPS])

FRICASSEEITEMS=[eggs(6),water(1500),yolks(3),oil(250),lemon(60),salt(.5),I('pepper',.125,'tsp','ground white pepper','Use the same amount of ground black pepper, or omit.'),stock(),gel()]
FRICASSEESTEPS=boil()+['Separate the hard-boiled yolks, press through a fine sieve and place in a clean mixing bowl. Refrigerate the cooked whites separately for use in another dish within 2 days. Whisk {{yolks}} into the sieved cooked yolks until smooth.']+GELPREP+['Measure {{oil}} into a jug. Whisk it into the yolk mixture a few drops at a time, then in a very thin stream once the sauce begins to thicken. Stop pouring if oil pools and whisk until it blends in.',
 'Stir {{lemon}} into the prepared liquid aspic, which must be barely warm and still fluid. Gradually whisk this mixture into the mayonnaise in small additions until smooth. Do not add hot aspic or a solid block of jelly.',
 'Stir in {{salt}} and {{pepper}}. Cover and refrigerate for about 1 hour until thickened and cold, then stir briefly before spooning over cold cooked fish, meat or vegetables.',DAY]
r=add(119,'Viennese Cold Fricassee Sauce with Aspic',24,120,'Cooked and pasteurized yolks form a rich mayonnaise that is lightened with lemon and liquid stock jelly, then chilled until thick.',FRICASSEEITEMS,FRICASSEESTEPS,
 'The actual scanned recipe is No271, cold fricassee sauce with aspic; it is not an anchovy or green sauce. It specifies six cooked yolks, three raw yolks and 125–250 ml oil. This base chooses 250 ml and retains 125 ml as a full variation. The continuation on page64 supplies the missing 250 ml melted aspic, now made in full from stock and a chosen 5 g approximately 200 Bloom gelatin. Juice of two lemons is standardized to 60 ml. The historical acid alternatives include concentrated vinegar essence, dissolved citric acid or strong tarragon vinegar. Full modern alternatives use ordinary 5% wine or tarragon vinegar, or a measured food-grade citric-acid solution; these are working choices, not verified equivalents of the unspecified old concentrations. Salt, pepper, twenty-four condiment servings and timing are supplied.');eggsource(r)
vi=copy.deepcopy(FRICASSEEITEMS)
for i in vi:
 if i['key']=='oil':i['amount']=125
variant(r,'lower-oil','With the lower oil amount',vi,copy.deepcopy(FRICASSEESTEPS))
for kind in ['white wine','tarragon']:
 vi=copy.deepcopy(FRICASSEEITEMS)
 for i in vi:
  if i['key']=='lemon':i.update(key='acid',name=kind+' vinegar, ordinary food-grade, about 5% acidity',substitution='Use the lemon-juice base recipe instead; do not substitute concentrated vinegar essence.')
 variant(r,kind.replace(' ','-')+'-vinegar','With ordinary '+kind+' vinegar',vi,[s.replace('{{lemon}}','{{acid}}') for s in FRICASSEESTEPS])
vi=[i for i in copy.deepcopy(FRICASSEEITEMS) if i['key']!='lemon']+[I('citric',3,'g','food-grade citric acid crystals','Use the lemon-juice base recipe instead; do not use cleaning-grade acid.'),water(60,'acidwater')]
vs=[s.replace('Stir {{lemon}} into the prepared liquid aspic','Dissolve {{citric}} completely in {{acidwater}}, then stir that solution into the prepared liquid aspic') for s in FRICASSEESTEPS]
variant(r,'citric-solution','With a measured citric-acid solution',vi,vs);r['notes']+=' The citric variation chooses 3 g food-grade citric acid in 60 ml water; it is not a measurement recovered from the source’s unspecified drops of solution.'

WHIPPEDITEMS=[stock(),gel(),oil(62.5),lemon(15),vinegar(10,'tarragon'),salt(.25),I('pepper',.0625,'tsp','ground white pepper','Omit for a milder sauce.'),I('nutmeg',.0625,'tsp','freshly grated nutmeg','Omit if preferred.')]
WHIPPEDSTEPS=GELPREP+['Place the bowl of liquid aspic over a larger bowl of ice water, keeping water out of the aspic. Whisk continuously or use an electric whisk on medium speed as it cools. Continue until pale, foamy and thick enough to hold soft peaks, about 10–20 minutes depending on bowl and cooling rate. Do not leave it unattended to set into a solid block.',
 'Measure {{oil}} into a jug and beat it in a few drops at a time, then in a very thin stream, keeping the mixture cool. Gradually beat in {{lemon}} and {{vinegar}}, followed by {{salt}}, {{pepper}} and {{nutmeg}}.',
 'Transfer the aerated sauce to a clean bowl, cover and refrigerate for about 30 minutes to firm. Serve cold with cooked fish or shellfish. If the aspic sets solid before it has been whipped, gently rewarm it just until fluid and start the cooling-and-whisking step again before adding oil.',DAY]
r=add(129,'Viennese Whipped Aspic and Oil Sauce',16,75,'Clear stock jelly is whipped until airy, then enriched with a little oil, lemon, tarragon vinegar and nutmeg for a cold seafood sauce.',WHIPPEDITEMS,WHIPPEDSTEPS,
 'The scanned No272 calls for 250 ml clear hot aspic and one-sixteenth litre oil, 62.5 ml. The extracted vinegar and cream were misread: neither is the main liquid, and there is no horseradish. The complete aspic uses 250 ml stock and a chosen 5 g approximately 200 Bloom gelatin. Lemon, tarragon vinegar, salt, white pepper and nutmeg are the actual seasonings, with working quantities supplied. Whipping while the gelatin cools is essential to the source method. Sixteen small condiment servings and timing are estimates. This egg-free sauce is distinct from the yolk-rich aspic fricassee sauce.');r['source']+=' Scanned original page64, recipe272.'

# No274 calls its base raw-yolk mayonnaise but cites No269, which also contains cooked yolks.
HERBITEMS=[I('tarragonherb',3,'g','fresh tarragon leaves','Use the same weight of extra chervil for a milder flavor.'),I('parsleyherb',5,'g','fresh parsley leaves','Use the same weight of extra chervil.'),I('chervilherb',3,'g','fresh chervil leaves','Use the same weight of extra parsley.'),I('sorrel',5,'g','fresh sorrel leaves','Use the same weight of baby spinach plus a few drops of lemon juice to taste.'),I('mint',2,'g','fresh garden mint leaves, a modern substitute for the historical Gundelkraut','Use the complete ground-ivy variation for the source herb.'),I('juniper',5,'','culinary juniper berries','Omit for a less resinous sauce; use berries sold for cooking.'),I('herbbutter',40,'g','unsalted butter, softened','Use the same weight of salted butter and reduce the added sauce salt.'),I('herboil',15,'ml','olive oil for pounding the herbs','Use the same volume of sunflower oil.')]
HERBSTEPS=['Wash and thoroughly dry {{tarragonherb}}, {{parsleyherb}}, {{chervilherb}}, {{sorrel}} and {{mint}}. Chop finely. Crush {{juniper}} in a mortar, add the herbs and pound with {{herbbutter}} and {{herboil}} until finely blended.',
 'Press the herb mixture through a fine sieve into a clean bowl, working it firmly with a spoon and discarding tough fibrous fragments. Stir the smooth herb butter gradually into the finished mayonnaise just before serving.',DAY]
base=copy.deepcopy(records[rows[124]['id']]['recipe'])
r=add(127,'Viennese Herb and Juniper Mayonnaise',28,35,'A fine herb butter with juniper, sorrel and tarragon is worked into mayonnaise for a rich cold sauce.',copy.deepcopy(base['ingredients'])+HERBITEMS,base['steps'][:-1]+HERBSTEPS,
 'The scanned No274 gives 4 deka butter, 40 g, not four teaspoons, plus one tablespoon oil and five juniper berries. It says Gundelkraut, interpreted as ground ivy (Glechoma hederacea), not the extracted burnet. The base uses a clearly labelled 2 g mint substitution for that less common herb; a full food-grade ground-ivy version retains the source option. Herb sprigs and unspecified sorrel become working weights. The text requests raw-yolk mayonnaise but cites No269, which combines cooked and raw yolks. This base follows the description using the full adapted No268; a complete alternative follows the cited No269. The optional tablespoon French mustard and lower oil amount are retained. Twenty-eight small condiment servings and time are estimates.');eggsource(r);r['source']+=' Botanical name context: https://virtuelle-gaerten.uni-hohenheim.de/4DACTION/W_Init/HG_Taxon_de?TaxonID=939796 and https://www.rhs.org.uk/plants/8034/glechoma-hederacea/details .'
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='mint':i.update(key='groundivy',name='food-grade ground-ivy leaves (Glechoma hederacea), supplied for culinary use',substitution='Use the mint-substitution base recipe instead.')
variant(r,'ground-ivy','With the source ground-ivy herb',vi,[s.replace('{{mint}}','{{groundivy}}') for s in r['steps']])
variant(r,'mustard','With French mustard',copy.deepcopy(r['ingredients'])+[I('mustard',1,'tbsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.')],r['steps'][:-1]+['Stir in {{mustard}} just before serving.']+[DAY])
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='oil':i['amount']=125
variant(r,'lower-oil','With the lower oil amount in the base mayonnaise',vi,copy.deepcopy(r['steps']))
mixed=copy.deepcopy(records[rows[123]['id']]['recipe'])
variant(r,'cited-mixed-yolks','With the cited cooked-and-raw-yolk mayonnaise',mixed['ingredients']+copy.deepcopy(HERBITEMS),mixed['steps'][:-1]+HERBSTEPS)

assert len(newids)==4 and len(merges)==0
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full scanned Viennese sauces with corrected ingredients, complete gelatin/egg/sponge components and source variations','repair-batch-041.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

