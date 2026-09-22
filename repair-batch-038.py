"""Complete sardine canapes, egg aspic and Swedish mayonnaise formulas."""
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

def gelatin(k,a):return I(k,a,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the manufacturer’s equivalent setting amount of leaf gelatin, soaking and draining the leaves first; do not replace gram-for-gram with agar.')
def cream(a):return I('cream',a,'ml','cold whipping cream, at least 35% fat, measured before whipping','Use the same volume of cold heavy cream.')
DAY='Keep covered at 4°C (40°F) or colder and serve within 1 day. Refrigerate within 2 hours of preparation and keep cold until serving. Do not leave out for more than 2 hours.'

SMALLMAYO=[yolks(1),oil(60),vinegar(5),lemon(5),I('mustard',.125,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.'),salt(.125),I('mayopart',60,'ml','mayonnaise reserved from the batch made here; not an additional purchase','Measure the finished mayonnaise; refrigerate any surplus separately.')]
SMALLSTEPS=['Whisk {{yolks}}, {{mustard}}, {{salt}}, {{vinegar}} and {{lemon}} in a clean bowl set on a damp towel. Add {{oil}} a few drops at a time while whisking, then in a thin stream once thickened, pausing if oil pools. Whisk until smooth.',
 'Measure out {{mayopart}} from the finished mayonnaise and refrigerate until needed. Cover any extra mayonnaise separately, refrigerate immediately at 4°C (40°F) or colder and use within 3 days.']
CANAPECOMMON=[I('bread',180,'g','soft white bread, crusts trimmed, about twelve small pieces','Use the same weight of soft wholemeal or gluten-free bread.'),I('anchovy',12,'g','anchovy paste','Mash the same weight of drained anchovy fillets to a smooth paste.'),I('sardines',120,'g','canned sardines, drained, about twelve small pieces','Use the same drained weight of canned sprats, checking for bones.'),I('milk',75,'ml','whole milk','Use the same volume of lactose-free whole milk.'),cream(45),I('whippedpart',45,'ml','whipped cream reserved from the cream above; not an additional purchase','Measure after whipping; liquid and whipped cream volumes are different.'),I('coatingsalt',.0625,'tsp','fine salt for the coating','Omit if the fish and mayonnaise already supply enough salt.'),gelatin('extrajelly',.5),water(5,'extrawater'),I('color',1,'','drop of red food coloring','Omit for an uncolored decoration.')]
WHIP='Whip {{cream}} in a chilled bowl until soft peaks hold. Gently spoon into a measuring jug without compressing it and reserve {{whippedpart}}. Cover any surplus whipped cream and refrigerate separately for use within 1 day.'
CANAPESTART='Cut {{bread}} into twelve small pieces at the base yield, keeping similar piece size when scaling. Drain {{sardines}} thoroughly and check for unwanted bones; divide the fish among the pieces after spreading the bread as directed.'
CANAPEEND=['Bloom {{extrajelly}} in {{extrawater}} in a small heatproof cup for 5 minutes. Stand the cup in hot water and stir until the gelatin dissolves; let it cool until only barely warm. Mix into the reserved coating along with {{color}}. Chill briefly, stirring, until thick enough to pipe. Pipe small dots or lines over the coated canapés, using all the reserved mixture.',
 'Arrange on a tray, cover without touching the decoration and refrigerate for at least 1 hour until the coating is set. Serve cold on the day they are made; the bread softens as it stands.',DAY]
def canapeitems(early=False):
 a=copy.deepcopy(SMALLMAYO+CANAPECOMMON)+[gelatin('jelly',3),I('decopart',40 if early else 60,'ml','coating reserved from the mixture below for decoration; not an additional purchase','Measure from the prepared coating before spreading the rest.')]
 if not early:a += [water(75,'jellywater'),I('butter',24,'g','softened butter','Use the same weight of a firm dairy-free spread.')]
 return a
def canapesteps(early=False):
 pre=SMALLSTEPS+[CANAPESTART]+(['Spread the bread pieces evenly with {{anchovy}} and lay the sardine pieces on top.'] if early else ['Blend {{anchovy}} with {{butter}}, spread evenly on the bread pieces and lay the sardine pieces on top.'])
 jelly=['Sprinkle {{jelly}} over {{milk}} in a small saucepan. Let bloom for 5 minutes, then warm gently, stirring until completely dissolved. Do not boil.'] if early else ['Sprinkle {{jelly}} over {{jellywater}} in a small saucepan. Let bloom for 5 minutes, then warm gently, stirring until dissolved. This makes the measured melted gelatin mixture; it is not dry gelatin measured by tablespoons. Add {{milk}} and warm just until evenly mixed. Do not boil.']
 return pre+jelly+[WHIP,'Cool the milk-gelatin mixture, stirring, until it begins to thicken but is still smooth and fluid. Gradually whisk in the reserved mayonnaise and {{coatingsalt}}, then fold in the measured whipped cream. Do not wait until the gelatin is a solid block; if it sets too far before adding mayonnaise, warm it gently just until fluid and cool again.',
 'Measure {{decopart}} from this coating into a small bowl for the decoration. Spread all the remaining coating evenly over the sardines and bread; place in the refrigerator while finishing the decoration.']+CANAPEEND
r=add(91,'Wallace Sardine Canapés with Set Mayonnaise',12,120,'Small anchovy-butter sandwiches carry sardines beneath a light milk, mayonnaise and whipped-cream coating, finished with a pink piped decoration.',canapeitems(),canapesteps(),
 'The 1928 Finnish text specifies five tablespoons melted gelatin, not five tablespoons dry powder. This adaptation makes that liquid component with 75 ml water and a chosen 3 g powdered gelatin, then adds the printed 75 ml milk, 60 ml mayonnaise and upper-end 45 ml whipped cream. Powder strength, bread and fish weights, anchovy butter, salt, decoration reserve and extra gelatin are modern working choices, not recovered leaf-weight conversions. The 1914 source uses gelatin leaves directly in milk and anchovy paste without butter; its full variation omits the extra water and butter and uses a chosen 3 g powder in the milk. Five historical leaves have no verified gram weight. Both versions preserve the cream fold and extra gelatin/color decoration. Cooling just until thickened replaces allowing a firm block before mixing. Twelve small canapés and timing including setting are estimates.');eggsource(r);r['category']='Starters';r['yieldUnit']='canapés'
variant(r,'1914-milk','1914 version — gelatin in milk, no anchovy butter',canapeitems(True),canapesteps(True))
for early,id,label in [(False,'prepared-mayo','With prepared mayonnaise'),(True,'1914-prepared-mayo','1914 version with prepared mayonnaise')]:
 vi=[i for i in canapeitems(early) if i['key'] not in {x['key'] for x in SMALLMAYO}]+[I('preparedmayo',60,'ml','prepared mayonnaise made with pasteurized egg','Use the same volume of an egg-free commercial mayonnaise; its texture may differ.')]
 vs=['Measure {{preparedmayo}} into a bowl and keep refrigerated until the coating is ready.']+canapesteps(early)[2:]
 variant(r,id,label,vi,vs)
merge(90,r,'Same Wallace sardine-canape dish across editions; the full 1914 direct-milk gelatin and butter-free anchovy version is retained as a named variation, with full coating and decoration methods.')

# Idun No10: individual egg slices with shrimp, set mayonnaise and clarified aspic.
ASPICITEMS=[eggs(3),water(1000),I('shrimp',12,'','small raw peeled shrimp, about 90 g total, deveined','Use twelve small cooked peeled shrimp; skip poaching and keep chilled.'),water(500,'shrimpwater'),yolks(2),oil(150),salt(.5),cayenne(),I('mustard',.25,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.'),vinegar(15,'tarragon'),lemon(15),water(15,'mayohotwater'),gelatin('mayogel',2),water(10,'mayogelwater'),I('stock',500,'ml','unsalted veal stock, liquid and chilled','Use the same volume of unsalted chicken stock for a different flavor.'),gelatin('aspicgel',10),I('aspicvinegar',5,'ml','white wine vinegar for the aspic','Use the same volume of cider vinegar.'),I('whites',60,'g','pasteurized liquid egg whites, about two whites, for clarification','Use whites from two large pasteurized shell eggs.'),water(15,'whitewater'),I('eggparsley',3,'g','small fresh parsley sprigs for the egg slices','Use the same weight of chervil sprigs.'),I('garnishparsley',3,'g','fresh parsley for the serving platter','Use the complete lettuce-garnish variation instead.')]
ASPICSTEPS=boil()+['Cut each peeled hard-boiled egg into four even slices at the base yield; reserve the trimmed white ends for another dish. Keep the slices cold.',
 'Bring {{shrimpwater}} to a simmer. Add {{shrimp}} and cook for about 2–3 minutes until pearly and opaque throughout. Drain, cool promptly in a shallow container in the refrigerator and keep chilled.',
 'Whisk {{yolks}}, {{salt}}, {{cayenne}} and {{mustard}} in a clean bowl. Measure {{oil}}, {{vinegar}} and {{lemon}} separately. Add the oil a few drops at a time, whisking until thick, then continue in a thin stream, alternating small additions of the vinegar and lemon juice. Gradually whisk in {{mayohotwater}}, freshly boiled and allowed to stop bubbling; this addition does not pasteurize the sauce.',
 'Sprinkle {{mayogel}} over {{mayogelwater}} in a small heatproof cup, bloom for 5 minutes, then stand the cup in hot water and stir until dissolved. Cool until barely warm, whisk in a spoonful of the mayonnaise, then stir this back into the remaining mayonnaise. Cover and refrigerate for about 45–60 minutes until it holds a soft piped shape; do not let it become a solid block.',
 'Sprinkle {{aspicgel}} over {{stock|0.1}} in a small bowl and leave for 5 minutes. Whisk {{whites}} with {{whitewater}} just until loosened, without making a foam. Place the remaining {{stock|0.9}} in a saucepan with {{aspicvinegar}} and the loosened whites.',
 'Heat the stock gently, stirring at first to prevent the whites sticking. Once the whites coagulate and rise, stop stirring and bring just to a gentle simmer. Cover, remove from the heat and let stand for 15 minutes. Strain slowly through a sieve lined with a clean damp fine cloth, without pressing the solids. If cloudy, pass through the rinsed cloth again.',
 'Stir the bloomed gelatin and its stock into the warm strained stock until completely dissolved. Measure the finished liquid and top up with hot drinking water only to the original listed stock volume if evaporation or straining has reduced it. Let cool, stirring occasionally, until no longer warm but still liquid.',
 'Use a shallow tray approximately 18 by 24 cm at the base yield, large enough to arrange the egg slices with gaps for cutting. Arrange the cold egg slices in the tray. Wash {{eggparsley}} and place a small sprig and one chilled shrimp on each slice. Pipe the thickened mayonnaise in a ring around each yolk, dividing all of it among the slices.',
 'Spoon a thin layer of the cool liquid aspic over the decorated slices and chill for 10 minutes to anchor the toppings. Pour the rest gently around and over them without disturbing the mayonnaise. Refrigerate for at least 3 hours until firmly set.',
 'Use a round cutter slightly wider than each egg slice to cut circles with a border of aspic. Lift carefully with a thin spatula onto a chilled serving platter. Cut the remaining aspic into small pieces and arrange alongside; wash and add {{garnishparsley}}. Serve two decorated slices per portion at the base yield.',DAY]
r=add(106,'Idun Eggs and Shrimp in Aspic',6,300,'Hard-boiled egg slices and shrimp are decorated with piped mayonnaise, then set in clear veal-stock jelly for a cold starter.',ASPICITEMS,ASPICSTEPS,
 'Both entries reproduce Idun No10. The original oil measure is 1.5 decilitres, 150 ml, not an unspecified number of parts. The full egg and shrimp cooking, mayonnaise, setting and stock-clarifying methods are supplied. Two pasteurized yolks and 60 g pasteurized whites replace separating raw shell eggs; eggshells are omitted from clarification. Gelatin uses explicit modern working weights: 2 g for the mayonnaise and 10 g per 500 ml stock for a firm cuttable aspic, at approximately 200 Bloom. Historical leaf sizes are not verified equivalents. The mayonnaise gelatin blooms in a modern 10 ml water rather than the source’s 7.5 ml; stock for the aspic bloom is reserved from the total, not extra. Cayenne, parsley and tray dimensions are supplied. Six portions of two slices follow the original twelve decorated slices. Time includes setting and can vary with refrigerator temperature.');finish(r);r['category']='Starters'
vi=copy.deepcopy(ASPICITEMS)
for i in vi:
 if i['key']=='garnishparsley':i.update(key='garnishlettuce',amount=50,unit='g',name='small tender lettuce leaves for the platter',substitution='Use the same weight of small romaine leaves.')
variant(r,'lettuce-garnish','With lettuce around the platter',vi,[s.replace('{{garnishparsley}}','{{garnishlettuce}}') for s in ASPICSTEPS])
merge(105,r,'Same full Idun No10 egg slices, shrimp, set mayonnaise and clarified aspic method; duplicate extraction with oil unit corrected and complete components supplied.')

IDUNITEMS=[yolks(2),I('salt',5,'g','fine salt','Reduce to taste; the source explicitly gives 5 g.'),cayenne(),I('mustard',.25,'tsp','prepared Dijon mustard','Use the complete mustard-free variation if preferred.'),vinegar(15,'tarragon'),oil(200),lemon(15),water(15,'hotwater')]
IDUNSTEPS=['Whisk {{yolks}}, {{salt}}, {{cayenne}} and {{mustard}} in a clean bowl on a damp towel until smooth. Gradually whisk in {{vinegar}} before adding the oil.',
 'Measure {{oil}} into a jug. Whisk in a few drops at first, then a very thin stream once the sauce begins to thicken. Pause pouring if oil pools and whisk until fully incorporated.',
 'Whisk in {{lemon}}. Gradually whisk in {{hotwater}}, freshly boiled and allowed to stop bubbling. This loosens the mayonnaise; it does not pasteurize raw yolks, so commercially pasteurized yolks are specified.',
 'Cover and refrigerate at 4°C (40°F) or colder for 4–5 hours to firm before serving. The sauce is softer than a mayonnaise made with less water.',COLD]
r=add(108,'Idun Tarragon-Lemon Mayonnaise',18,315,'A softly textured mayonnaise combines tarragon vinegar with lemon and a small hot-water finish, then chills before serving.',IDUNITEMS,IDUNSTEPS,
 'All three entries reproduce Idun No442. The full original gives optional French mustard, 5 g salt, 200 ml oil, 15 ml vinegar, a range of 7.5–15 ml lemon juice and 15 ml boiling water. This base chooses the upper lemon amount and includes the optional mustard; complete alternatives retain the lower lemon amount, no mustard and the all-lemon version. Vinegar is added before oil, as printed. Modern refrigeration replaces the instruction to keep it cool but not on ice. Eighteen small condiment servings and active time are estimates; the displayed total includes five hours chilling. The full extra-yolk/vinegar rescue is supplied as a separate method.');eggsource(r)
vi=copy.deepcopy(IDUNITEMS)
for i in vi:
 if i['key']=='lemon':i['amount']=7.5
variant(r,'less-lemon','With the lower lemon amount',vi,copy.deepcopy(IDUNSTEPS))
vi=[i for i in copy.deepcopy(IDUNITEMS) if i['key']!='mustard'];vs=[s.replace(', {{cayenne}} and {{mustard}}', ' and {{cayenne}}') for s in IDUNSTEPS]
variant(r,'no-mustard','Without mustard',vi,vs)
vi=copy.deepcopy(vi)
for i in vi:
 if i['key']=='vinegar':i.update(key='firstlemon',name='lemon juice for the initial yolk mixture',substitution='Use the vinegar base recipe if preferred.')
variant(r,'all-lemon','Mustard-free, with lemon instead of vinegar',vi,[s.replace('{{vinegar}}','{{firstlemon}}') for s in vs])
vi=copy.deepcopy(IDUNITEMS)+[I('rescueyolk',1,'','additional large pasteurized egg yolk for the rescue','Use 18 g commercially pasteurized liquid yolk.'),I('rescuevinegar',7.5,'ml','additional tarragon vinegar for the rescue','Use the same volume of white wine vinegar.')]
variant(r,'extra-yolk-rescue','Extra-yolk method for a separated batch',vi,IDUNSTEPS[:3]+['In a second clean bowl, whisk {{rescueyolk}} with {{rescuevinegar}}. Add the prepared mayonnaise a few drops at a time, whisking continuously, then in a very thin stream once it holds together. This method uses the full base batch plus the two additional rescue ingredients; if rescuing mayonnaise already made, do not make the base again. It also makes a richer three-yolk sauce if the base has not separated.']+IDUNSTEPS[3:])
merge(107,r,'Same Idun No442 formula and full method; shorter extraction omits optional mustard, which is retained with complete no-mustard/lemon alternatives and rescue method.')
merge(109,r,'Same Idun No442 printed recipe and measured formula; duplicate extraction, with optional mustard correctly distinguished from cayenne.')

HEMMETITEMS=[yolks(2),salt(.125),mustard(.75),oil(500),vinegar(60),water(7.5)]
HEMMETSTEPS=['Set a mixing bowl on a damp towel inside a larger bowl containing cold water, keeping water out of the mixing bowl. Whisk {{yolks}}, {{salt}} and {{mustard}} until smooth.',
 'Measure {{oil}}, {{vinegar}} and {{water}} into separate small jugs. Whisk continuously while adding the oil a few drops at a time until an emulsion forms. Continue with a thin stream of oil, alternating small additions of the measured vinegar. Add the measured water in occasional drops as the sauce thickens, until all three liquids are incorporated.',
 'Keep whisking until smooth and glossy. If oil starts to pool, stop pouring and whisk until it blends in before adding more.',COLD]
r=add(110,'Hemmets Rich Mustard Mayonnaise',36,20,'A rich, oil-forward mayonnaise uses English mustard and gradually added vinegar, with a little water to loosen the emulsion.',HEMMETITEMS,HEMMETSTEPS,
 'Both entries reproduce Hemmets kokbok No433. The printed formula is two yolks, half a litre oil, three to four tablespoons vinegar or lemon juice and half a tablespoon water. This base chooses four modern tablespoons vinegar, 60 ml; full variations retain 45 ml vinegar and both lemon amounts. A pinch of salt becomes one-eighth teaspoon and a small teaspoon dry English mustard becomes a chosen three-quarters teaspoon. Cool-water mixing replaces ice water to avoid solidifying olive oil. Thirty-six small condiment servings and timing are estimates, rather than the original twelve larger portions. This differs substantially from Idun No442 in its oil-to-yolk ratio and method and is retained separately.');eggsource(r)
for acid,a,id,label in [('vinegar',45,'less-vinegar','Three tablespoons vinegar'),('lemon',60,'lemon','Four tablespoons lemon juice'),('lemon',45,'less-lemon','Three tablespoons lemon juice')]:
 vi=copy.deepcopy(HEMMETITEMS)
 for i in vi:
  if i['key']=='vinegar':
   i['amount']=a
   if acid=='lemon':i.update(key='lemon',name='lemon juice',substitution='Use the corresponding vinegar variation if preferred.')
 variant(r,id,label,vi,[s.replace('{{vinegar}}','{{lemon}}').replace('measured vinegar','measured lemon juice') if acid=='lemon' else s for s in HEMMETSTEPS])
merge(111,r,'Same full Hemmets No433 formula and method with two yolks and 500ml oil; three/four tablespoon vinegar and lemon alternatives retained as complete variations.')

assert len(newids)==4 and len(merges)==5
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full primary recipes, modern gelatin components, measured methods and source alternatives','repair-batch-038.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-merge',aliases[s['id']]['reason'],'repair-batch-038.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

