"""Complete cold fish preparations and two distinct cooked sauce formulas."""
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

DAY='Keep covered at 4°C (40°F) or colder and serve within 1 day. Refrigerate within 2 hours of preparation and keep cold until serving.'
FISHREF=' Modern cooking endpoints: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures .'
def fishdone(r):r['category']='Main dishes';r['source']+=FISHREF;return eggsource(r)
def aspicitems():return [I('stock',250,'ml','clear unsalted fish stock, chilled','Use the same volume of clear unsalted chicken or vegetable stock.'),I('gelatin',5,'g','unflavored powdered gelatin, approximately 200 Bloom','Use the manufacturer’s equivalent setting amount of leaf gelatin, soaking and draining it first; agar is not a gram-for-gram substitute.')]
ASPIC=['Sprinkle {{gelatin}} over {{stock|0.2}} and leave for 5 minutes. Warm the remaining {{stock|0.8}} in a saucepan, remove from heat and stir in the bloomed gelatin with its stock until fully dissolved. Do not boil.',
 'Pour the liquid aspic into a shallow dish to a depth of about 1 cm. Cool the dish over ice water for 10–15 minutes, keeping water out, then cover and refrigerate for about 2 hours until firmly set. Prepare the remaining components while it chills.']
CHILL='Lift the cooked fish onto a clean shallow tray and let stand for about 5 minutes, just until safe to handle. Remove the skin and bones carefully, checking for fine pin bones, and separate into pieces. Spread in one layer in a shallow container, set over ice water briefly to remove the heat, then cover and refrigerate promptly at 4°C (40°F) or colder until thoroughly cold, about 1 hour. Do not leave a deep pan of fish and hot poaching liquid to cool on the counter.'

# No907 calls No894 for a water/salt/bay poach; it does not call the separate vinegar poach.
mi=copy.deepcopy(records[rows[124]['id']]['recipe']['ingredients'])
for i in mi:i['amount']/=2
ms=copy.deepcopy(records[rows[124]['id']]['recipe']['steps'][:-1])
PITEMS=[I('fish',1000,'g','whole pike, cleaned, scaled and gutted, with head and bones','Use the same cleaned weight of zander or another similar lean white fish; adjust cooking to its thickness.'),water(2500,'poachwater'),I('poachsalt',2,'tsp','fine salt for poaching','Reduce or omit; most poaching liquid is discarded.'),I('bay',1,'','dried bay leaf','Omit if unavailable.'),eggs(2),water(1000)]+aspicitems()+mi
PPOACH=['Use a fish kettle or covered pan large enough for {{fish}} to lie flat. Bring {{poachwater}}, {{poachsalt}} and {{bay}} to a boil. Lower in the cleaned fish, adding hot drinking water only if necessary to cover. Reduce the heat immediately and keep the liquid just below a simmer, without vigorous boiling.',
 'Poach until the thickest flesh reaches 63°C (145°F) and is opaque and separates easily, checking after about 20 minutes and allowing roughly 25–40 minutes for a fish of the base size. Thickness governs the time; continue gently if the center has not reached the endpoint. Remove and discard the bay leaf.',CHILL]
PSTEPS=ASPIC+PPOACH+boil()+['Slice the cold hard-boiled eggs into rounds and keep refrigerated.']+ms+['Arrange the cold deboned fish pieces on a chilled platter and coat with the freshly made mayonnaise. Cut the set aspic into small cubes or chop it and arrange around the fish with the hard-boiled egg slices. Serve cold.',DAY]
r=add(120,'Cold Pike with Mayonnaise and Aspic',4,180,'Gently poached pike is cooled, deboned and coated with lemon mayonnaise, then garnished with clear stock jelly and hard-boiled egg.',PITEMS,PSTEPS,
 'No907 calls the book’s boiled pike No894, whose liquid is water, salt and one bay leaf; the adjacent sour poach is not used. The source gives no fish weight or garnish amounts. This adaptation chooses a 1 kg cleaned whole fish, 2.5 litres water, two teaspoons salt, two eggs and 250 ml aspic made with 5 g gelatin. Half of the same book’s completed No268 mayonnaise supplies the coating. The historical instruction to cool in the poaching liquid is replaced by prompt shallow cooling and refrigeration. Cooking duration is a guide with a thermometer endpoint, not the old fixed three-quarter hour for an unspecified fish. Four main-course servings and three-hour total including chilling are estimates.');fishdone(r)

# The second fish dish uses vinegar, salad and a shaped presentation, so it is not a duplicate of120.
raw=copy.deepcopy(records[rows[122]['id']]['recipe']);MITEMS=copy.deepcopy(raw['ingredients'])
for i in MITEMS:
 if i['key']=='yolks':i['amount']=4
 if i['key']=='oil':i['amount']=200
 if i['key']=='lemon':i['amount']=20
 if i['key']=='pepper':i['substitution']='Omit for a milder mayonnaise.'
MSTEPS=raw['steps'][:-1]
FITEMS=[I('fish',750,'g','zander (pike-perch) tail piece, scaled and cleaned, bone-in','Use the whole-pike or cooked-fish variation if preferred.'),water(1500,'poachwater'),I('poachvinegar',125,'ml','white wine vinegar for poaching','Use the same volume of cider vinegar.'),I('poachsalt',2,'tsp','fine salt for poaching','Reduce or omit; most poaching liquid is discarded.'),eggs(2),water(1000),I('greens',200,'g','lamb’s lettuce (mâche), trimmed','Use the same trimmed weight of tender head-lettuce leaves.'),I('saladoil',15,'ml','olive oil for the salad','Use the same volume of sunflower oil.'),I('saladvinegar',10,'ml','white wine vinegar for the salad','Use the same volume of cider vinegar.'),I('saladsalt',.125,'tsp','fine salt for the salad','Reduce or omit.'),I('anchovies',8,'g','anchovy fillets, drained, about two fillets','Use the same weight of thin smoked sprat strips for a different flavor.'),I('capers',20,'g','capers, drained','Use the same drained weight of finely diced cornichons.')]
FPOACH=['Bring {{poachwater}}, {{poachvinegar}} and {{poachsalt}} to a boil in a pan that fits {{fish}}. Lower in the fish, adding hot drinking water only if necessary to cover. Reduce the heat and poach just below a simmer. Begin checking after 8–10 minutes; allow about 15–25 minutes for the base tail piece, and continue until the thickest part reaches 63°C (145°F), is opaque and separates easily. Do not rely on standing off the heat for a fixed time.',CHILL]
EGGSTEPS=boil()+['Slice the cold hard-boiled eggs and refrigerate until assembly.']
SALAD=['Wash {{greens}} and dry thoroughly. Immediately before serving, toss with {{saladoil}}, {{saladvinegar}} and {{saladsalt}}.']
ASSEMBLE=['Drain the cold deboned fish well and gently press out excess liquid with clean utensils. Mound it into a low cone in the center of a chilled shallow bowl and coat with the prepared mayonnaise.',
 'Arrange the dressed greens and hard-boiled egg slices around the fish. Roll {{anchovies}} into small curls and decorate the fish with them and {{capers}}. Serve cold.']
FSTEPS=FPOACH+EGGSTEPS+MSTEPS+SALAD+ASSEMBLE+[DAY]
r=add(126,'Viennese Fish Mayonnaise with Dressed Greens',4,120,'Cold poached zander is shaped into a mound and coated with lemon mayonnaise, with dressed greens, egg slices, anchovies and capers around it.',FITEMS+MITEMS,FSTEPS,
 'The scan specifies 500–750 g fish and one-eighth litre vinegar, 125 ml, not the extracted half litre. Schill is zander or pike-perch, not shad. The base chooses a 750 g tail piece and the printed 200 g salad greens. The source calls four-yolk mayonnaise but references Menu14, whose actual formula has three; this full four-yolk adaptation scales its oil and lemon accordingly while assigning salt, mustard and pepper to taste. Poaching water, salt, egg garnish, caper amount, salad dressing, yield and timing are working quantities. A thermometer endpoint and shallow chilling replace the fixed 8–10 minute off-heat poach and unspecified cooling. Whole fish, already cooked fish, mayonnaise-filled shells, cooked-tartar-filled shells and clear or red aspic garnishes are retained as complete alternatives. Prepared cooked-fish weight is a chosen working yield, not an exact conversion from a bone-in fish.');fishdone(r)
vi=copy.deepcopy(r['ingredients'])
for i in vi:
 if i['key']=='fish':i['name']='whole small pike, cleaned, scaled and gutted';i['substitution']='Use the zander-tail base recipe instead.'
variant(r,'whole-pike','With a small whole pike',vi,[s.replace('base tail piece','small whole pike') for s in FSTEPS])
vi=[i for i in copy.deepcopy(r['ingredients']) if i['key'] not in ['poachwater','poachvinegar','poachsalt']]
for i in vi:
 if i['key']=='fish':i.update(amount=450,name='cooked, chilled, skinless and boneless pike or zander pieces',substitution='Use the freshly poached base recipe instead.')
variant(r,'cooked-fish','With previously cooked fish',vi,['Use {{fish}} that was cooked through and promptly refrigerated at 4°C (40°F) or colder. Check again for bones and drain gently; do not re-poach. Keep cold while preparing the remaining components.']+FSTEPS[2:])
SHELL=['Drain the cold deboned fish well and flake into bite-size pieces. Fold in half of the prepared mayonnaise, divide between four clean food-safe serving shells or small dishes at the base yield, then spread the remaining mayonnaise over the tops.',ASSEMBLE[1].replace('around the fish','around the filled shells').replace('decorate the fish','decorate the shells')]
variant(r,'mayonnaise-shells','Fish and mayonnaise in serving shells',copy.deepcopy(r['ingredients']),FPOACH+EGGSTEPS+MSTEPS+SALAD+SHELL+[DAY])
for red in [False,True]:
 vi=copy.deepcopy(r['ingredients'])+aspicitems();gs=copy.deepcopy(ASPIC)
 if red:
  vi.append(I('color',.25,'ml','red food coloring, liquid','Omit and use the clear-aspic variation; do not use non-food dye.'))
  gs.insert(1,'Stir {{color}} into the dissolved aspic before pouring it into the shallow dish. This measured food-color option is a modern way to obtain the source’s red garnish.')
 variant(r,'red-aspic' if red else 'clear-aspic','With red aspic garnish' if red else 'With clear aspic garnish',vi,gs+FSTEPS[:-1]+['Cut or chop the set aspic and arrange around the finished fish platter. Allow about 1 additional hour for the firmer aspic chilling, making this variation about 3 hours in total.']+[DAY])

# Full half-batch of the source's cooked tartar sauce, separate from the uncooked coating mayonnaise.
TI=[I('tartyolks',3,'','large pasteurized egg yolks for the tartar sauce','Use 18 g commercially pasteurized liquid yolk per yolk.'),I('tartvinegar',15,'ml','tarragon vinegar','Use the same volume of white wine vinegar.'),I('tartlemon',7.5,'ml','lemon juice','Use the same volume of lime juice.'),water(7.5,'tartwater'),I('tartoil',30,'ml','olive oil for the tartar sauce','Use the same volume of sunflower oil.'),I('tartsalt',.25,'tsp','fine salt for the tartar sauce','Reduce or omit.'),I('tartmustard',.5,'tsp','prepared Dijon mustard','Use the same amount of another smooth prepared mustard.'),I('tartparsley',2.5,'g','fresh parsley leaves','Use the same weight of chervil.'),I('tartonion',5,'g','peeled onion','Use the same weight of extra shallot.'),I('tartshallot',5,'g','peeled shallot','Use the same weight of extra onion.'),I('tartchervil',2.5,'g','fresh chervil','Use the same weight of parsley.'),I('tartpickle',15,'g','pickled cucumber, drained','Use the same drained weight of cornichons.'),I('tartanchovy',4,'g','anchovy fillet, drained and boneless','Use the same weight of finely chopped smoked sprat.'),I('tartcapers',20,'g','capers, drained','Use the same weight of extra finely diced cornichons.'),I('mayoreserve',150,'ml','coating mayonnaise reserved from the batch below; not an additional purchase','Measure the finished sauce and refrigerate the surplus separately.')]
TS=['Whisk {{tartyolks}}, {{tartvinegar}}, {{tartlemon}} and {{tartwater}} in a heatproof bowl. Set over gently simmering water, keeping the bowl above the water, and whisk continuously until thickened and 71°C (160°F). Remove promptly without boiling or scrambling the yolks.',
 'Set the bowl in a larger bowl of cold water and stir until cool but smooth, about 10 minutes. Whisk in {{tartoil}} gradually, then {{tartsalt}} and {{tartmustard}}.',
 'Wash and dry {{tartparsley}} and {{tartchervil}}. Finely chop them with {{tartonion}}, {{tartshallot}}, {{tartpickle}}, {{tartanchovy}} and {{tartcapers}}. Stir all into the cooled cooked-yolk sauce and keep refrigerated until assembly.']
TASSEMBLE=['Drain and flake the cold deboned fish. Fold in all of the prepared cooked tartar sauce and divide between four clean food-safe serving shells or small dishes at the base yield. Spread the reserved uncooked mayonnaise over the tops.',SHELL[1]]
TSTEPS=FPOACH+EGGSTEPS+MSTEPS+['Measure {{mayoreserve}} from the uncooked mayonnaise and keep chilled for coating. Cover the extra mayonnaise separately, refrigerate promptly and use within 3 days.']+TS+SALAD+TASSEMBLE+[DAY]
variant(r,'tartar-shells','Fish with cooked tartar sauce in serving shells',copy.deepcopy(r['ingredients'])+TI,TSTEPS)
vi=copy.deepcopy(r['ingredients'])+copy.deepcopy(TI)
for i in vi:
 if i['key']=='tartpickle':i['amount']=30
variant(r,'tartar-shells-extra-pickle','Tartar-filled shells with the ingredient-list pickle amount',vi,copy.deepcopy(TSTEPS))
r['notes']+=' The full tartar variation uses half the six-yolk cooked sauce on scanned page73, including its tarragon vinegar, lemon, water, parsley, onion, shallot, chervil, anchovy and capers. The printed heading says one pickle but the method says half; the base tartar choice follows the method and an extra-pickle variation follows the heading. Pickle weights of 15 g or 30 g are half-batch working choices. The unspecified few spoonfuls of oil become 30 ml in this half-batch. It also makes the complete four-yolk coating mayonnaise, reserves 150 ml and accounts for the surplus. Allow about 20 additional minutes for the cooked tartar variation.'

r=add(132,'Warm Cooked Mayonnaise with Parsley',6,15,'A small egg-and-oil sauce is gently cooked with vinegar and water, then finished with parsley and a trace of cayenne.',[yolks(2),oil(30),vinegar(15),water(60),salt(.25),cayenne(),parsley()],
 ['Whisk {{yolks}} in a small heatproof bowl. Measure {{oil}} and whisk it in a few drops at a time until smoothly incorporated.',
  'Warm {{water}} until hot but not boiling. Gradually whisk {{vinegar}} into the yolk mixture, then the measured hot water in a thin stream while whisking continuously.',
  'Set the bowl over gently simmering water without letting its base touch the water. Whisk continuously until the sauce thickens and reaches 71°C (160°F). Remove immediately; do not allow it to boil or scramble.',
  'Stir in {{salt}}, {{cayenne}} and {{parsley}}. Serve promptly while warm with cooked fish or vegetables. This is a pourable cooked sauce, not a cold thick mayonnaise.',DAY],
 'The complete Farmer recipe specifies two yolks, two tablespoons oil, one tablespoon vinegar, a quarter cup hot water and one teaspoon chopped parsley, with salt and cayenne to taste. Modern measures give 30 ml oil, 15 ml vinegar and 60 ml water. Salt, cayenne, six small sauce portions, timing and the measured cooking endpoint are supplied. The original oil-first, acid/water-next, cooked-over-water method and final parsley addition are preserved.');r['source']+=FISHREF;eggsource(r)

r=add(194,'Warm Brown-Butter Tartar Sauce',6,15,'Browned butter is strained into warm vinegar, lemon and Worcestershire sauce for a tangy fish sauce with a nutty aroma.',[vinegar(15),lemon(5),salt(.25),I('worcestershire',15,'ml','Worcestershire sauce','Use the same volume of vegetarian Worcestershire sauce if required.'),I('butter',76,'g','unsalted butter, cut into pieces','Use the same weight of salted butter and omit the added salt; an oil substitute will not brown in the same way.')],
 ['Combine {{vinegar}}, {{lemon}}, {{salt}} and {{worcestershire}} in a small heatproof bowl. Set over hot water and stir gently until warm; keep the bowl above the water.',
  'Melt {{butter}} in a light-colored small frying pan over medium-low heat. Swirl or stir as it foams, watching the milk solids closely. Cook for about 3–5 minutes until the solids are golden brown and the butter smells nutty. Remove from heat immediately before it darkens or burns.',
  'Pour the browned butter through a fine heatproof sieve into the warm seasoned liquid. Discard the strained solids, whisk the sauce briefly and serve at once with cooked fish. Whisk again if the butter separates; this sauce is not intended to be a stable mayonnaise.',
  'If saving leftovers, cool promptly, cover and refrigerate at 4°C (40°F) or colder for up to 2 days. Rewarm gently over hot water, stirring, without boiling.'],
 'Farmer credits The Boston Cook Book for this Tartar Sauce. It is a warm brown-butter sauce, not the cold egg-and-pickle tartar sauce. The printed third-cup butter is represented by a modern working 76 g of solid butter; the source does not specify pre-melted butter. Vinegar, lemon, salt and Worcestershire proportions and the explicit straining step are preserved. Six small portions and timing are estimates.')

assert len(newids)==4 and len(merges)==0
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full source fish and cooked sauces with corrected measurements, complete components and source variations','repair-batch-042.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

