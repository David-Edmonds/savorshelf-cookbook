"""Complete twelve Denison and Manila dressings from verified source formulas."""
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

AI=[butter(14),flour(.5,'tbsp'),salt(.5),lemon(10),mustard(1),sugar(1.5),yolks(2),vinegar(360),cayenne(),I('cream',120,'ml','cold heavy whipping cream, measured before whipping','Use the same volume of lactose-free dairy whipping cream.')]
AS=['Whisk {{yolks}}, {{salt}}, {{mustard}}, {{sugar}} and {{cayenne}} in a heatproof bowl until smooth.',
 'Melt {{butter}} in a small saucepan, stir in {{flour}} to make a smooth paste and cook for about 1 minute until it bubbles without browning. Gradually whisk in {{vinegar}}, keeping the mixture smooth, and heat until steaming.',
 'Whisk the hot vinegar mixture into the yolks very slowly. Return to the saucepan and cook over low heat, stirring constantly, until lightly thickened and at least 71°C (160°F). Remove promptly and stir over cold water until the base is fully cool.',
 'Whip {{cream}} in a chilled clean bowl until it holds soft peaks. Beat a spoonful into the cooled base, then fold in the rest gently. Stir in {{lemon}} last, in small additions. Cover and refrigerate for about 30 minutes before serving.',coldserve(),DAY]
r=add(157,'Denison Tangy Dressing with Whipped Cream and Lemon',36,55,'A sharp vinegar-and-yolk dressing is cooked with a little butter and flour, cooled and softened with whipped cream before lemon is added last.',AI,AS,
 'The scan specifies HALF a tablespoon flour and HALF a teaspoon salt, not the extracted quarter measures. One-and-a-half cups vinegar is genuinely printed and is retained as a modern 360 ml. The original calls for enough whipped cream to reach the desired consistency without giving an amount; this adaptation chooses 120 ml liquid whipping cream before whipping. Butter is a working 14 g, the two teaspoons lemon juice are 10 ml, and the original lemon-last order is retained. The base is cooled before adding whipped cream so it does not simply melt. Thirty-six small dressing portions and timing are estimates.');tagged(r)

r=add(159,'Denison Four-Egg Steamed Mustard Dressing',44,55,'A diluted vinegar dressing is thickened gently with four eggs, prepared mustard and melted butter.',[whole(4),sugar(1),prepared(1.5,'tbsp'),salt(.5),pepper(.5),water(360),vinegar(120),butter(50)],
 ['Melt {{butter}} in a small saucepan and let it cool until just warm. In a heatproof bowl, beat {{eggs}}, {{sugar}}, {{mustard}}, {{salt}} and {{pepper}}. Gradually whisk in {{water}}, {{vinegar}} and the melted butter.',bath(),COOL,coldserve(),DAY],
 'The scanned page369 has one-and-a-half cups cold water, HALF a cup vinegar and HALF a teaspoon salt. This corrects the extracted one-cup water, one-cup vinegar and one-teaspoon salt. Modern measures are 360 ml water and 120 ml vinegar. Four eggs, one tablespoon sugar, one-and-a-half tablespoons prepared mustard and half a teaspoon pepper are retained. Egg-size butter becomes a chosen 50 g. Forty-four small dressing portions and timing are working estimates.');tagged(r)

r=add(160,'Denison Brown-Sugar Milk Dressing',24,45,'Milk, brown sugar and mustard make a lightly sweet cooked egg dressing, with vinegar and a little melted butter.',[whole(1),sugar(1,brown=True),vinegar(120),milk(180),mustard(1),butter(5),salt(.25),pepper(.125)],
 ['Melt {{butter}} and let it cool until just warm. Beat {{eggs}} with {{sugar}}, {{mustard}}, {{salt}} and {{pepper}}, then whisk in the melted butter.',
 'Gradually whisk in {{vinegar}} and {{milk}}. Transfer to a heatproof bowl set over gently simmering water, with the bowl above the water. Stir continuously until it lightly coats a spoon and reaches at least 71°C (160°F), about 8–12 minutes. Remove without boiling hard.',COOL,coldserve(),DAY],
 'Both the scanned ingredient list and method specify THREE-QUARTERS of a cup milk, modern 180 ml, not the extracted half cup. Half a cup vinegar is 120 ml. The egg, tablespoon brown sugar and teaspoon mustard are retained; teaspoon butter becomes a working 5 g and the unspecified salt and pepper are supplied. Gentle water-bath cooking expands the source’s brief boil-until-thick direction while avoiding a hard boil. Twenty-four small portions and total time including cooling are estimates.');tagged(r)

r=add(161,'Denison Cream-and-Olive-Oil Egg Dressing',12,45,'Egg, cream and a small amount of olive oil give body to a tangy mustard dressing that is cooked and served cold.',[whole(1),vinegar(45),oil(15),mustard(1),salt(.5),sugar(1,'tsp'),cream(45)],
 ['Whisk {{eggs}}, {{mustard}}, {{salt}} and {{sugar}} in a heatproof bowl. Gradually whisk in {{oil}}, {{vinegar}} and {{cream}} until evenly combined.',bath(),COOL,coldserve(),DAY],
 'The scan confirms HALF a teaspoon salt, not the extracted full teaspoon. The other quantities are one egg, three tablespoons each vinegar and cream, one tablespoon oil and one teaspoon each mustard and sugar. Modern liquid measures are 45 ml, 45 ml and 15 ml. The source beats everything together and cooks it; the full water-bath method supplies a measured endpoint and gentler heat. Twelve small portions and timing are estimates.');tagged(r)

HI=[eggs(4),water(1200),butter(28),sugar(1),salt(1),mustard(1),pepper(.125),cream(480),vinegar(45)]
HS=boil()+['Separate the firm cooked yolks and press through a fine sieve. Slice or chop the cooked whites and refrigerate them for the salad garnish.',
 'Melt {{butter}} and let it cool until just warm. Mash it into the sieved yolks with {{sugar}}, {{salt}}, {{mustard}} and {{pepper}} until smooth.',
 'Gradually whisk in {{cream}}, then {{vinegar}} in small additions. Transfer to a saucepan and heat gently, whisking constantly, until it just simmers and slightly thickens, about 5–8 minutes. Remove from heat. If the acid causes a grainy texture, briefly blend with an immersion blender with its head fully submerged; do not continue boiling in an attempt to force it smooth.',COOL,
 'Spoon the cold dressing over the prepared salad and use the reserved hard-boiled whites as garnish.',DAY]
r=add(162,'Denison Cooked-Yolk Cream Dressing',40,65,'Sieved hard-boiled yolks and melted butter enrich a cream dressing finished with vinegar, with the cooked whites reserved for garnish.',HI,HS,
 'The full source uses four hard-boiled yolks, two tablespoons butter, one tablespoon sugar, one teaspoon each salt and mustard, two cups milk or cream, pepper and vinegar to thicken. The base chooses modern 480 ml cream, a working 28 g butter, 45 ml vinegar and one-eighth teaspoon pepper. The vinegar amount is supplied, not recovered from the book. The milk version includes the source’s tablespoon cornstarch dissolved in milk. Whisking and an optional brief blending step replace the source’s unconditional promise that a curdled mixture will become smooth through continued boiling. Forty small portions and timing are estimates.');tagged(r)
vi=[milk(480) if i['key']=='cream' else copy.deepcopy(i) for i in HI]+[I('starch',1,'tbsp','cornstarch','Use the same volume of arrowroot powder; thickening may vary.')]
vs=HS[:3]+['Whisk {{starch}} into {{milk}} while cold until no lumps remain. Add the milk mixture gradually to the cooked-yolk paste, then whisk in {{vinegar}}. Heat in a saucepan, whisking constantly, until it gently simmers and thickens, about 5–8 minutes. Simmer for about 1 minute to cook the starch, then remove. If grainy, blend briefly with an immersion blender, keeping its head submerged.']+HS[4:]
variant(r,'milk-and-starch','With milk and the source’s cornstarch thickener',vi,vs)

r=add(163,'Denison Six-Egg Dressing with Cold Cream Finish',36,55,'A mustard-and-vinegar egg base is cooked gently, chilled, then finished with cream and salt.',[whole(6),vinegar(120),sugar(3),cayenne(),mustard(1),salt(.5),cream(120)],
 ['Whisk {{vinegar}}, {{sugar}}, {{mustard}} and {{cayenne}} in a heatproof bowl. Beat {{eggs}} separately, then whisk them into the seasoned vinegar until evenly combined.',bath(),COOL,
  'When the cooked dressing is fully cold, gradually stir in {{cream}} and {{salt}}. Keep refrigerated until serving.',coldserve(),DAY],
 'The scan specifies HALF a cup vinegar and HALF a cup rich cream, modern 120 ml each, not the extracted quarter-cup amounts. Six whole eggs, three tablespoons sugar and one teaspoon mustard are retained. Salt and cayenne are working quantities. Cream and salt are added only after the cooked base is cold. The source’s pint yield is not treated as a verified modern volume, and its weeks-long storage claim is replaced by short refrigerated use. Thirty-six small portions and timing are estimates.');tagged(r)

r=add(164,'Denison Spiced Sweet-Yolk Dressing',36,55,'Sweetened yolks and cream are tempered with hot vinegar and butter, then cooked into a tangy dressing with black pepper and cayenne.',[yolks(4),sugar(120,'ml'),salt(.5),pepper(.5),mustard(.5),butter(14),cream(120),I('cayenne',1/3,'tsp','ground cayenne pepper','Reduce or omit for a milder dressing.'),vinegar(240)],
 ['Whisk {{yolks}}, {{sugar}}, {{salt}}, {{pepper}}, {{mustard}}, {{cream}} and {{cayenne}} in a heatproof bowl until smooth.',
  'Heat {{vinegar}} in a small saucepan until steaming, then add {{butter}} and stir until melted. Slowly pour the hot vinegar-butter mixture into the yolks while whisking continuously.',bath(),COOL,coldserve(),DAY],
 'The scanned page372 specifies HALF a cup each sugar and cream, HALF a teaspoon each salt, black pepper and mustard, and ONE-THIRD teaspoon cayenne. The extracted quarter measures are incorrect. The half pint vinegar is represented here by a working modern 240 ml; this does not establish the historical pint’s capacity. Sugar is a dry volume of 120 ml, cream is 120 ml, and a tablespoon butter becomes a working 14 g. The vinegar is heated with butter before tempering, as printed. Thirty-six small portions and timing are estimates; this fresh dressing is refrigerated briefly rather than bottled for many weeks.');tagged(r)

TI=[sugar(2,'tsp'),salt(.5),mustard(3),vinegar(120),whole(2),butter(50),milk(60)]
TS=['Whisk {{eggs}}, {{sugar}}, {{salt}}, {{mustard}} and {{milk}} in a heatproof bowl. Add {{butter}} in small pieces. Keep the vinegar aside at this stage.',bath(),
 'Gradually whisk {{vinegar}} into the hot thickened base, then return the bowl to the water bath and stir for another 2–3 minutes until smooth and thickened again. Do not boil hard.',COOL,coldserve(),DAY]
r=add(165,'Denison Two-Stage Mustard Dressing',24,55,'Eggs, milk and butter are cooked first, then vinegar is added for a second gentle cooking to finish a strong mustard dressing.',TI,TS,
 'The scan gives HALF a teaspoon salt and HALF a cup vinegar, correcting the extracted quarter amounts. Quarter cup milk remains modern 60 ml, and the full tablespoon mustard is three modern teaspoons. Egg-size butter becomes a chosen 50 g. The first cooking excludes vinegar; it is added before the second cooking. The optional cold-cream thinning is preserved as a full variation with a working 30 ml cream. Twenty-four small portions and timing are estimates; the source’s long-storage claim is not carried forward.');tagged(r)
variant(r,'cream-thinned','With cream added after cooling',copy.deepcopy(TI)+[cream(30)],TS[:-2]+['When fully cold, gradually stir in {{cream}} to loosen the dressing.']+TS[-2:])

EI=[butter(15),sugar(2,'tsp'),salt(.25),pepper(.125),prepared(1),cream(120),vinegar(120),I('starch',2,'tsp','cornstarch','Use the same volume of arrowroot powder; thickening may vary.')]
ES=['Whisk {{starch}} into {{cream}} while cold until smooth. Add {{sugar}}, {{salt}}, {{pepper}} and {{mustard}}, then gradually whisk in {{vinegar}}.',
 'Transfer to a small saucepan and add {{butter}}. Heat gently, whisking constantly, until the butter melts and the sauce comes to a gentle simmer. Stir for 1 minute until lightly thickened, then remove. If the acidic mixture looks grainy, blend briefly with an immersion blender, keeping the head submerged.',COOL,coldserve(),DAY]
r=add(174,'Denison Egg-Free Cream-and-Mustard Dressing',18,45,'Cornstarch thickens a cream, vinegar and butter dressing flavored with prepared mustard, sugar and pepper.',EI,ES,
 'The scanned page381 confirms half a cup cream or milk and half a cup vinegar, modern 120 ml each, with no egg. Walnut-size butter and an unspecified amount of cornstarch become working 15 g and two teaspoons. The saltspoonful of salt and pepper is not treated as a verified modern standard; the chosen amounts are quarter teaspoon salt and one-eighth teaspoon pepper. Two teaspoons sugar and one teaspoon prepared mustard are retained. Both dairy options have full methods. Eighteen small portions and timing are estimates.');tagged(r)
variant(r,'milk','Made with milk instead of cream',[milk(120) if i['key']=='cream' else copy.deepcopy(i) for i in EI],[s.replace('{{cream}}','{{milk}}') for s in ES])

r=add(175,'Denison Oil-Free Eleven-Yolk Dressing',44,55,'Eleven yolks thicken a mustard-and-vinegar dressing that is beaten as it cools and loosened with cream for serving.',[yolks(11),salt(3),mustard(3),vinegar(360),sugar(9,'tsp'),cream(120)],
 ['Whisk {{yolks}}, {{salt}}, {{mustard}} and {{sugar}} in a heatproof bowl. Gradually whisk in {{vinegar}}; use ordinary culinary vinegar, not concentrated vinegar essence.',
  'Set the bowl over gently simmering water, with the bowl above the water. Stir continuously, scraping the bottom and sides, until thickened and at least 71°C (160°F), about 10–15 minutes. Remove promptly without letting the yolks scramble.',
  'Set the bowl over cold water and beat with a hand whisk or electric whisk on low speed until cool and smooth, keeping water out. Cover and refrigerate for about 30 minutes until cold.',
  'Just before using, gradually stir in {{cream}} to loosen the dressing, then spoon over the prepared salad.',DAY],
 'The primary scan genuinely prints ELEVEN yolks, one-and-a-half cups vinegar, three teaspoons each salt and mustard and nine teaspoons sugar. The vinegar becomes modern 360 ml. The unmeasured cream for thinning becomes a working 120 ml. The sauce is cooked, then beaten during cooling, as printed; eleven is not an OCR correction or an inferred number. Forty-four small condiment portions and timing are estimates. Weeks-long storage is replaced by short refrigerated use.');tagged(r)

MA=[whole(1),butter(14),flour(1),water(15),cream(45),mustard(.5),salt(.25),sugar(2.5),I('celerysalt',.0625,'tsp','celery salt','Omit, or use the same amount of fine salt for a different flavor.'),vinegar(30)]
MAS=['Let {{butter}} soften, then rub it together with {{flour}}, {{salt}}, {{mustard}}, {{sugar}} and {{celerysalt}} until smooth. Beat in {{eggs}}, then gradually whisk in {{vinegar}} and {{water}}.',
 'Cook the mixture in a small saucepan over low heat, stirring constantly, until thickened and at least 71°C (160°F), about 5–8 minutes. Stir gently for about 2 minutes after thickening to cook the flour, without boiling hard or letting it catch.',
 'Transfer to a clean shallow bowl and stir over cold water until almost cold. Gradually stir in {{cream}}, then cover and refrigerate for about 30 minutes until fully cold.',coldserve(),DAY]
r=add(177,'Manila Sweet Cooked Salad Dressing',14,45,'A sweet egg-and-butter dressing is thickened with a little flour, flavored with mustard and celery salt, and finished with cream after cooling.',MA,MAS,
 'The scan shows QUARTER teaspoon salt, not the extracted three-quarter teaspoon. It also genuinely prints two separate sugar lines, two-and-a-half tablespoons and one tablespoon, while vinegar appears only in the method with no amount. This adaptation chooses two-and-a-half tablespoons sugar and a working 30 ml vinegar; it does not claim to recover an intended correction to that printing error. A full sweeter variation retains the sum of both printed sugar lines. Celery salt is restored explicitly to the method, cream is added when almost cold, and tablespoon butter becomes a working 14 g. Fourteen small portions and timing are estimates.');tagged(r)
vi=copy.deepcopy(MA)
for i in vi:
 if i['key']=='sugar':i['amount']=3.5
variant(r,'printed-sugar-total','With both printed sugar amounts combined',vi,copy.deepcopy(MAS))

r=add(178,'Manila Cooked-Yolk and Cream Dressing',8,30,'Hard-boiled yolks are pounded smooth with a little oil, prepared mustard, cream and sugar to make a thick, mild dressing.',[eggs(3),water(1000),oil(15),salt(.25),prepared(1),I('sugar',2,'tsp','icing sugar','Use the same volume of fine caster sugar, stirring until dissolved.'),cream(15)],
 boil()+['Separate the firm cooked yolks and pound them to a smooth paste in a mortar or press through a fine sieve. Refrigerate the cooked whites separately for another dish and use within 2 days.',
 'Beat {{oil}} into the cooked-yolk paste a few drops at a time. Gradually work in {{salt}}, {{mustard}}, {{sugar}} and {{cream}} until smooth. This is a thick spoonable dressing rather than a loose pouring sauce.',coldserve(),DAY],
 'The complete scanned formula specifies three hard-boiled yolks, three teaspoons oil, QUARTER teaspoon salt, one teaspoon prepared mustard, two teaspoons powdered sugar and three teaspoons cream. Modern oil and cream volumes are 15 ml each. No vinegar or lemon appears in either the ingredient list or the method, so none is added. The complete egg-boiling and cooling instructions are supplied. Eight small condiment portions and timing are estimates.');tagged(r)

assert len(newids)==12 and len(merges)==0
(root/'content-overrides.json').write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for id in newids:db.execute('insert or replace into decisions values(?,?,?,?,?)',(id,records[id]['bodySha256'],'prepared-adaptation','Full Denison and Manila source formulas corrected from scans, with measured cooking and complete alternatives','repair-batch-046.py'))
db.commit();print(json.dumps(dict(newAdaptations=len(newids),newAliases=len(merges),totalOverrides=len(records),totalAliases=len(aliases))))

