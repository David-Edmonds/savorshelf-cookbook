"""Complete Hungarian whipped aspic sauce, cooked mayonnaise and pike-perch platter."""
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

r=add(79,'Hungarian Majonéz — Whipped Aspic and Oil Sauce',10,35,
 'Clear savory jelly is whisked with olive oil, lemon and vinegar into a pale coating for chilled cooked foods.',[
 I('stock',200,'ml','clear unsalted chicken stock','Use the same volume of clear unsalted fish or vegetable stock.'),I('gelatin',5,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the same weight of fish gelatin of similar setting strength; agar needs a different formula.'),oil(75),lemon(15),vinegar(15),pepper(.0625)],
 ['Put {{stock|0.25}} in a small bowl, sprinkle {{gelatin}} evenly over it and leave for 5 minutes. Heat {{stock|0.75}} until steaming, remove from heat and stir in the bloomed gelatin until fully dissolved. This supplies the melted aspic required by the original.',
 'Transfer the liquid aspic to a clean stainless-steel or glass bowl. Whisk in {{pepper}}, {{lemon}} and {{vinegar}}, then gradually add {{oil}} in a thin stream while whisking. Stand the bowl over ice water and continue whisking until pale, glossy and thick enough to spread. Keep ice water out of the sauce and remove the bowl from the bath before the mixture sets solid.',
 'Use while still soft to coat already-cooked, thoroughly chilled fish, poultry or vegetables. The sauce firms as the gelatin cools. If it becomes too firm before spreading, stand the bowl briefly over lukewarm water and stir to loosen; do not make it hot.',
 'Keep the sauce or coated food covered at 4°C (40°F) or colder. Use within 2 days and refrigerate within 2 hours of preparation. This is a refrigerated fresh sauce, not a shelf-stable preserve.'],
 'Original recipe 134 uses two coffee cups melted aspic and one small coffee cup oil. Those historical cup capacities are unspecified; 200 ml stock, 5 g modern gelatin and 75 ml oil are explicit working quantities, not verified cup conversions. Lemon, pepper, ten small condiment servings and time are supplied; a modern tablespoon vinegar becomes 15 ml. The complete aspic formula is included. Stainless steel or glass replaces the original brass bowl. The source gives serving examples with cold poultry, fish and calf brain; this entry is the standalone sauce. Its whipped texture depends on gelatin strength and temperature and has not been kitchen-tested.')

r=add(80,'Majonéz Új Módon — Hungarian Cooked Mayonnaise',20,35,
 'Egg yolks, olive oil and wine vinegar are whisked over hot water into a tangy cooked sauce, then cooled while stirring.',[
 yolks(8),oil(120),vinegar(120),lemon(15),salt(.5)],
 ['Whisk {{yolks}}, {{oil}}, {{vinegar}}, {{lemon}} and {{salt}} together in a heatproof bowl until evenly blended and lightly foamy.',
 'Set the bowl over gently simmering water, keeping its base above the water. Whisk continuously, reaching the edges of the bowl, until the mixture thickens and reaches 71°C (160°F). Lift the bowl off the heat as soon as it reaches that temperature; do not let the sauce boil or the eggs scramble.',
 'Set the bowl over cold water and stir until completely cool, keeping the cooling water out of the sauce. Serve as a sharp condiment with cooked chilled foods.',
 'Transfer to a clean covered container and refrigerate at 4°C (40°F) or colder. Use within 2 days and refrigerate within 2 hours of preparation. Stir before serving.'],
 'The full source recipe 327 specifies eight yolks, eight tablespoons oil and eight tablespoons fine wine vinegar with lemon juice. Modern 15 ml tablespoons give 120 ml each oil and vinegar. Lemon juice has no separate source quantity; 15 ml is an explicit modern addition, rather than silently replacing part of the stated vinegar. Half a teaspoon salt, twenty small condiment servings and thirty-five minutes including cooling are estimates. The source fifteen-minute claim is not a guaranteed preparation time. Its high vinegar proportion is retained; this is a distinctly sharp cooked sauce. Temperature checking is a modern addition.');eggsource(r);r['source']+=' Egg-dish cooking endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'

r=add(81,'Süllő Majonézzel — Cold Pike-Perch with Yolk Sauce',6,180,
 'Butter-braised pike-perch steaks are chilled and arranged in a ring with a cooked-yolk sauce and chopped savory jelly.',[
 I('fish',1500,'g','cleaned pike-perch or zander, cut by the fishmonger into steaks about 3 cm thick','Use the same weight of another firm white fish cut into similar pieces; cook to the same internal temperature.'),I('butter',40,'g','unsalted butter for braising','Use the same weight of a dairy-free cooking spread.'),water(60,'braisewater'),salt(.5),pepper(.125),eggs(4),water(1000),I('stock',285,'ml','clear unsalted fish stock for the aspic','Use the same volume of clear unsalted vegetable stock.'),I('gelatin',7,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the same weight of fish gelatin of similar setting strength.'),water(35,'bloomwater'),I('sauceaspic',60,'ml','liquid aspic reserved from the batch below; not an additional purchase','Use the complete pastry-garnish variation if less jelly is wanted.'),oil(100),lemon(20),vinegar(10)],
 ['Sprinkle {{gelatin}} over {{bloomwater}} and leave for 5 minutes. Heat {{stock}} until steaming, remove from heat and stir in the bloomed gelatin until dissolved. Measure {{sauceaspic}} from this liquid mixture into a small covered bowl for the sauce. Pour the remainder into a shallow dish, cover and refrigerate for about 2 hours until set. Keep the reserved sauce portion refrigerated too; it will be gently melted later.',
 'Pat {{fish}} dry and season with {{salt}} and {{pepper}}. Melt {{butter}} in a wide covered pan over gentle heat. Arrange the fish in one layer, add {{braisewater}}, cover and cook gently for about 15–20 minutes, until the thickest flesh reaches 63°C (145°F). Work in batches if needed, dividing the measured butter and water among the batches.',
 'Lift out the cooked fish and drain. Spread the pieces in a shallow covered container and refrigerate promptly, within 2 hours of cooking, until cold, about 45–60 minutes. Keep the pieces intact where possible.',
 *boil(),
 'Separate the firm cooked yolks and press them through a fine sieve into a clean bowl. Refrigerate the cooked whites separately for another dish within 2 days. Gently melt the reserved sauce aspic by standing its bowl in lukewarm water, then let it cool until barely warm and still liquid.',
 'Whisk {{oil}} into the sieved yolks in a thin stream. Gradually whisk in {{lemon}}, {{vinegar}} and the measured reserved aspic until smooth. Stand the bowl over cold water and stir just until the sauce is thick enough to spread; keep water out and do not let it set solid.',
 'Arrange the cold fish steaks in a ring on a chilled platter and spoon the yolk sauce over them. Chop the set garnish jelly finely and arrange around the rim. Keep refrigerated until serving. Check the fish carefully for bones as you portion it; discard all bones.',END],
 'The source recipe 349 gives about 1.5 kg fish, four cooked yolks, one coffee glass of oil, juice from a small lemon, a serving-spoon or ladle quantity of aspic, and a little vinegar. The translated standard cup and tablespoon are not verified source measures. This adaptation chooses 100 ml oil, 20 ml lemon, 60 ml liquid aspic and 10 ml vinegar explicitly, with complete gelatin preparation. Butter, seasoning, a small braising-water addition, six servings and timing are modern working choices. The water helps the covered fish cook gently without scorching the butter. The source permits chopped aspic or small pastry shapes around the rim; both are retained.');r['category']='Fish';r['source']+=' Fish cooking endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='stock':i['amount']=52.5
 if i['key']=='bloomwater':i['amount']=7.5
 if i['key']=='gelatin':i['amount']=1.5
vi.append(I('pastry',150,'g','ready-rolled puff pastry, kept chilled','Use the same weight of ready-rolled gluten-free puff pastry and follow its baking instructions.'))
vs=copy.deepcopy(r['steps']);vs[0]='Sprinkle {{gelatin}} over {{bloomwater}} and leave for 5 minutes. Heat {{stock}} until steaming, remove from heat and stir in the bloomed gelatin until dissolved. Measure {{sauceaspic}} from this small batch into a covered bowl and refrigerate for the sauce; no separate garnish jelly is needed.'
vs.insert(1,'Heat the oven to 200°C (390°F). Cut {{pastry}} into small rings or decorative shapes about 4 cm across. Arrange on a lined baking tray and bake for about 12–18 minutes, until puffed, golden and cooked through, following the pastry package if its directions differ. Cool on a rack.')
vs=[s.replace('Chop the set garnish jelly finely and arrange around the rim.','Arrange the cooled pastry shapes around the rim just before serving so they stay crisp.') for s in vs]
variant(r,'pastry-garnish','With small pastry shapes',vi,vs);r['notes']+=' The pastry variation uses modern ready-rolled puff pastry as the chosen small pastry garnish and reduces the aspic to the sauce portion only. The original does not specify a pastry dough formula.'

assert len(newids)==3
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Hungarian primary-source preparation, measured aspic components, cooking, chilling and garnish variation','repair-batch-035.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),totalOverrides=len(records),totalAliases=len(aliases))))
