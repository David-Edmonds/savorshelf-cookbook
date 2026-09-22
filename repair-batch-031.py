"""Complete cream and Polish sauces; preserve low-oil variations and duplicate sources."""
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

# Compare the full yolk/oil proportions and method, preserving the explicit acid and garnish differences.
r=records[rows[29]['id']]['recipe'];updatedids.append(r['id'])
vi=[yolks(2),oil(30),vinegar(15),salt(.125),pepper(.0625)]
vs=['Whisk {{yolks}} in a small clean bowl. Add {{oil}} a few drops at a time while whisking until evenly blended. This original low-oil formula makes a soft, yolk-rich sauce rather than a stiff mayonnaise.','Whisk in {{salt}} and {{pepper}}, then slowly add {{vinegar}} and mix until smooth. Serve in small portions with cooked chilled fish, poultry or salad.',COLD]
variant(r,'atrutel-white-vinegar','Atrutel white-vinegar version',vi,vs)
for id,label,key,a,name in [('atrutel-capers','Atrutel caper version','capers',5,'drained capers, finely chopped'),('atrutel-parsley','Atrutel parsley version','parsley',2,'fresh parsley leaves, finely chopped')]:
 variant(r,id,label,copy.deepcopy(vi)+[I(key,a,'g',name,'Use the other named Atrutel garnish variation if preferred.')],vs[:-1]+['Fold in '+tk(key)+' just before serving.']+[COLD])
r['notes']+=' Atrutel recipe 32 uses the same two-yolk/two-tablespoon-oil formula and specifies a tablespoon of white vinegar after the oil. Its full 15 ml vinegar-after-oil version and caper or parsley variations are retained separately from the earlier 10 ml working-acid versions. The 5 g capers and 2 g parsley are supplied modern garnish amounts.'
merge(58,r,'Same two-yolk to two-tablespoon-oil low-oil formula and acid finish as canonical29; explicit15ml white vinegar after oil and both caper/parsley options retained as complete named variations.')

def baseitems(acid='vinegar',withmustard=True):
 a=[yolks(1),oil(240),vinegar(10) if acid=='vinegar' else lemon(10),salt(.5),cayenne()]
 if withmustard:a.append(mustard(.5))
 return a
def basesteps(acid='vinegar',withmustard=True):
 return ['Whisk {{yolks}}, {{salt}} and {{cayenne}}'+(' with {{mustard}}' if withmustard else '')+' in a clean bowl. Measure {{oil}} into a jug. Add it a few drops at a time while whisking; once thick, continue in a thin stream. Alternate the later oil additions with small additions of '+tk(acid)+' until all is incorporated and the sauce is smooth. Stop pouring if oil pools and whisk until it blends in.']
def creamitems(liquid,portion):return [I('cream',liquid,'ml','cold whipping cream, at least 35% fat, measured before whipping','Use the same volume of cold heavy cream; do not use pouring cream that cannot be whipped.'),I('whippedportion',portion,'ml','whipped cream reserved from the cream above; not an additional purchase','Measure after whipping; this is not the same volume of liquid cream.')]
def creamsteps():return ['Whip {{cream}} in a chilled bowl until soft peaks hold. Gently spoon into a measuring jug without pressing it down and reserve {{whippedportion}}. The liquid cream is supplied in excess because whipping volume varies. Refrigerate any extra whipped cream separately and use within 1 day.']
CREAMEND='Serve immediately with chilled cooked foods or salad. Keep at 4°C (40°F) or colder and refrigerate leftovers within 2 hours; use within 1 day. The cream will gradually lose volume, so mix only when ready to serve.'

r=add(59,'Greenbaum Mayonnaise with Whipped Cream',25,20,'Homemade mustard mayonnaise is lightened with measured whipped cream for a soft, airy salad dressing.',baseitems()+creamitems(300,480),basesteps()+creamsteps()+['Fold the measured whipped cream into the mayonnaise with a broad spoon until evenly blended, without beating out the air.'],
 'The source specifies one pint of already-whipped cream but no amount of prepared dressing. This modern batch uses the full original Greenbaum one-yolk mayonnaise formula as the dressing portion and represents the whipped pint by 480 ml. The liquid cream amount allows a measured whipped portion with any extra accounted for; liquid and whipped volumes are not interchangeable. About 750 ml total, or twenty-five small 30 ml servings, is a working yield. The named French-dressing version preserves the original alternative.');r['steps'].append(CREAMEND);eggsource(r)
fi=[salt(1.5),pepper(.75),I('sugar',3,'tsp','white sugar','Use the same amount of caster sugar.'),I('paprika',.1875,'tsp','sweet paprika','Omit if preferred.'),vinegar(90),oil(180)]+creamitems(300,480)
fs=['Whisk {{salt}}, {{pepper}}, {{sugar}}, {{paprika}} and {{vinegar}} until the sugar dissolves. Gradually whisk in {{oil}} until blended. This French dressing is a vinaigrette and can separate; whisk again immediately before combining.']+creamsteps()+['Fold the measured whipped cream into the French dressing a little at a time and serve immediately. This version is tangier and less stable than the mayonnaise version.']+[CREAMEND]
variant(r,'french-cream','With French dressing and whipped cream',fi,fs);r['notes']+=' The French version uses three times the book’s full French dressing formula (two tablespoons vinegar to four tablespoons oil, with its seasonings) to provide a comparable dressing portion. That multiplication is a modern batch choice; twenty-five servings are approximate for either version.'

r=add(60,'Greenbaum White Mayonnaise',12,20,'Mustard-free lemon mayonnaise is gently folded with whipped cream for a paler, lighter dressing.',baseitems('lemon',False)+creamitems(90,120),basesteps('lemon',False)+creamsteps()+['Fold the measured whipped cream into the lemon mayonnaise until evenly blended; do not beat vigorously.']+[CREAMEND],
 'The complete usual Greenbaum mayonnaise formula is expanded here, with lemon replacing vinegar and mustard omitted exactly as the white variation directs. The source half cup is represented by 120 ml measured AFTER whipping. The 90 ml liquid cream supplies a little extra so the whipped portion can be measured. Twelve condiment servings and about 390 ml finished sauce are modern estimates. The egg-white variation is lighter in volume and gives smaller servings at the same serving count.');eggsource(r)
ei=baseitems('lemon',False)+[I('eggwhite',15,'g','commercially pasteurized liquid egg white labeled suitable for whipping','Use about half the white of a large pasteurized shell egg, weighed; untreated raw egg white is not a substitute.')]
es=basesteps('lemon',False)+['In a separate small, completely clean grease-free bowl, whisk {{eggwhite}} until it holds stiff peaks. A small hand whisk is helpful for this small quantity. Fold it gently into the finished lemon mayonnaise just before serving.']+[CREAMEND.replace('The cream will gradually lose volume','The foam will gradually lose volume')]
variant(r,'whipped-egg-white','With whipped pasteurized egg white',ei,es);r['notes']+=' The alternative half egg white is standardized to 15 g, a modern working weight. Use a pasteurized product specifically suitable for whipping; some liquid egg products will not foam well.'

r=add(67,'Sos Majonezowy bez Oliwy — Cooked Butter and Yolk Sauce',4,20,'A small cooked egg-yolk and butter sauce is cooled and finished with vinegar, following a Polish oil-free mayonnaise method.',[
 yolks(1),I('butterfirst',7,'g','unsalted butter for the first addition','Use the same weight of salted butter and omit the added salt.'),I('butterlast',14,'g','unsalted butter for the second addition, cut into small pieces','Use the same weight of salted butter and omit the added salt.'),water(10,'saucewater'),salt(.125),cayenne(),vinegar(15)],
 ['Set a small heatproof bowl over a saucepan of gently simmering water, keeping its base above the water. Whisk {{yolks}} with {{saucewater}} and {{butterfirst}} in the bowl until the butter melts and the mixture begins to thicken.',
 'Whisk in {{salt}} and {{cayenne}}, then add {{butterlast}} in small pieces, stirring continuously until smooth. Heat gently while stirring until the sauce reaches 71°C (160°F), checking with a small-tip thermometer. Lift the bowl off the heat as soon as that temperature is reached; do not let the sauce boil.',
 'Stir over a bowl of cold water for a few minutes until cool but still fluid, keeping water out of the sauce. Gradually whisk in {{vinegar}}. Serve promptly in small spoonfuls with cooked vegetables or fish.',
 'Cover and refrigerate at 4°C (40°F) or colder if not using immediately, and use within 1 day. The butter will firm in the refrigerator; stand the covered portion briefly at room temperature and stir before serving. Refrigerate within 2 hours.'],
 'The printed source page 236 confirms HALF A TABLESPOON of butter first, not the half teaspoon in the extraction, followed by another tablespoon. Modern working weights of 7 g and 14 g are supplied. A small 10 ml water addition supports controlled heating of the yolk without immediately scrambling it; this addition and the thermometer endpoint are modern adaptations. The source vinegar-after-cooling order is retained. This is a small, buttery sauce rather than a high-oil mayonnaise. Four small spoonful servings and time are estimates.');eggsource(r);r['source']+=' Egg-dish endpoint: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'

r=add(68,'Sos Majonezowy Ostry — Sharp Polish Mayonnaise',8,15,'Mustard and cayenne season a yolk-rich mayonnaise finished with both vinegar and lemon for a distinctly sharp salad dressing.',[yolks(2),salt(.5),cayenne(),mustard(1),oil(120),vinegar(45),lemon(15)],
 ['Whisk {{yolks}} with {{salt}}, {{cayenne}} and {{mustard}} in a clean bowl until smooth. Measure {{oil}} into a jug and add it drop by drop while whisking; once blended and thickening, continue in a very thin stream until all is incorporated.',
 'Whisk in {{vinegar}} gradually, then slowly add {{lemon}}. Mix well after each addition. The fairly high acid proportion gives a sharp, pourable dressing rather than a stiff mayonnaise. Serve in small portions with salad or cooked chilled vegetables.',COLD],
 'The source’s half filiżanka of oil is represented by a modern working 120 ml, not a verified conversion of that historical cup. Three modern tablespoons vinegar become 45 ml; the juice of half a lemon becomes a working 15 ml. The original two yolks, half teaspoon salt, teaspoon dry mustard and both acids are retained. A pinch of red pepper is standardized to one-sixteenth teaspoon cayenne. Eight small condiment servings are estimated.');eggsource(r)

r=add(69,'Sos Majonezowy Provensal — Polish Provençal Mayonnaise',12,20,'Three egg yolks make a rich olive-oil mayonnaise, finished with vinegar and a small amount of sugar.',[yolks(3),salt(.5),I('oil',227,'g','olive oil, weighed','Use the same weight of a mild sunflower oil; this amount is a mass, not a volume.'),vinegar(30),I('sugar',1,'tsp','white sugar','Use the same amount of caster sugar.')],
 ['Whisk {{yolks}} and {{salt}} in a clean bowl until smooth. Weigh {{oil}} into a jug. Add it a few drops at a time while whisking continuously; when the mixture thickens, continue in a very thin stream until all the measured oil is incorporated.',
 'Slowly whisk in {{vinegar}}, then add {{sugar}} and stir until dissolved. The sauce should be smooth and creamy. If oil pools, stop adding it and whisk until it is incorporated before continuing. Serve in small portions with cooked chilled foods.',COLD],
 'The two imported records repeat the same single printed Sos Majonezowy Provensal paragraph. Half a funt of olive oil is represented by a modern working 227 g, corresponding to half a modern avoirdupois pound; this is an explicit adaptation choice, not a claim that every historical funt had that weight. Oil stays in mass units rather than being mistranslated as a pint. Three yolks, about two tablespoons vinegar and a teaspoon sugar are retained. Half a teaspoon salt, twelve condiment servings and timing are supplied. The original twenty-minute stirring is a hand-mixing instruction, not egg cooking.');eggsource(r)
merge(70,r,'Both records reproduce the same single original Polish Provensal paragraph: three yolks, half funt oil, two tablespoons vinegar, teaspoon sugar and identical mixing sequence.')

assert len(newids)==5 and len(merges)==2
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'recipe-aliases.json').write_text(json.dumps(list(aliases.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids+updatedids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full source formula, complete variations, measured ingredients and method supplied','repair-batch-031.py'))
for s in merges:db.execute('insert or replace into decisions values(?,?,?,?,?)',(s['id'],s['bodySha256'],'prepared-merge',aliases[s['id']]['reason'],'repair-batch-031.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),updatedCanonical=len(updatedids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))
