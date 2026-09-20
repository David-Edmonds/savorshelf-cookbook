"""Authored modern adaptations; keep stable source IDs and record changed assumptions."""
import json,pathlib
root=pathlib.Path(__file__).parent
source=root.parent.parent/'outputs/SavorShelf-Image-Tools/approved-export/Recipes.jsonl'
ids=['historical-f8ae338a990b1599597520f3','historical-7b50009f683c2e6110a9c62e','historical-dd8c7e4f64772fa37bb54bed']
originals={r['id']:r for line in source.open(encoding='utf-8') if (r:=json.loads(line))['id'] in ids}
def item(key,amount,unit,name,substitution):return dict(key=key,amount=amount,unit=unit,name=name,substitution=substitution)
records=[]
def add(id,category,servings,minutes,description,ingredients,steps,changes,references=''):
 s=originals[id];r=dict(s['recipe']);r.update(id=id,category=category,servings=servings,yieldUnit='servings',minutes=minutes,totalMinutes=minutes,description=description,ingredients=ingredients,steps=steps,notes=changes+' Yield and timing are planning estimates. This adaptation has not been kitchen-tested.',source=s['recipe']['source']+' Modern adaptation by SavorShelf. '+references,sourceStatus='adapted',versionNote='Modern measured adaptation',updatedAt='2026-09-20T00:00:00Z')
 records.append(dict(sourceId=id,bodySha256=s['bodySha256'],recipe=r))
add(ids[0],'Breakfast',2,15,'Thick bread is toasted crisp and buttered on both faces while hot, leaving a crunchy surface and a tender middle.',[
 item('bread',4,'slice','bread, each about 19 mm (¾ inch) thick','Use the same number of similarly sized wheat, white or sourdough slices. Gluten-free bread may toast faster.'),
 item('butter',28,'g','softened salted butter','Use the same weight of a spreadable dairy-free butter alternative; flavor and browning differ.')],
 ['Arrange {{bread}} on a rack over a baking tray. Heat the oven to 400°F (200°C).',
  'Toast for about 6–10 minutes, turning halfway, until both faces are crisp and golden. Watch the final minutes closely.',
  'Spread {{butter|0.5}} over one face of the warm slices. Turn them over and spread the remaining {{butter|0.5}} over the other face.',
  'Serve two slices per person immediately. For a larger batch, toast in uncrowded batches; do not multiply the oven temperature or per-batch time.'],
 'The source specified bread thickness and buttering both sides but no quantities. This adaptation sets four slices, 28 g butter and an oven method. Bread size changes the portion size.')
add(ids[1],'Sides',6,85,'Steamed potatoes are mashed with warm milk and a little butter for a soft, light side dish, with optional oven browning.',[
 item('potatoes',1000,'g','peeled floury potatoes, cut into 3 cm chunks','Use the same weight of russet potatoes; Yukon Gold gives a denser, creamier mash.'),
 item('butter',14,'g','unsalted butter','Use the same weight of a dairy-free butter alternative.'),
 item('milk',240,'ml','whole milk','Use the same volume of lactose-free whole milk. Unsweetened plant milk changes the flavor.'),
 item('salt',3,'g','fine salt','Omit for an unsalted version; do not exchange different salts by volume.')],
 ['Cover {{potatoes}} with cold water and leave for 30 minutes, as in the source; then drain.',
  'Put the potato pieces in a steamer over simmering water, keeping them above the water. Cover and steam for 20–25 minutes until a fork meets no resistance. Keep water in the lower pan as needed for steaming.',
  'Warm {{milk}} in a small saucepan until steaming, without boiling. Transfer the tender potatoes to a warm bowl and mash by hand.',
  'Mix {{butter}} and {{salt}} into the hot mash. Stir in half the warm milk, {{milk|0.5}}, followed by the remaining {{milk|0.5}}, until evenly combined. Avoid a blender or food processor.',
  'Serve as six side portions. For the optional browned finish, place in a shallow oven-safe dish and bake at 400°F (200°C) for 10–15 minutes.'],
 'The missing potato weight and salt amount are supplied as a modern formulation. Milk and butter are interpreted as 240 ml and 14 g. The original soak and steaming method are retained. Allow about 70 minutes without browning, or 85 with it.',
 'Mashing technique cross-check: https://www.idahopotato.com/recipes/traditional-mashed-idaho-potatoes ; quantities and steaming method above are this source adaptation, not that recipe.')
add(ids[2],'Breakfast',3,10,'Eggs scrambled in butter with a small splash of milk form tender curds. The source’s generous pepper amount gives a pronounced peppery finish.',[
 item('eggs',6,'','large eggs','Use pasteurized shell eggs in the same number if preferred. An egg-free replacement needs a separate formulation.'),
 item('milk',30,'ml','whole milk','Use 30 ml water for a less creamy result, or the same volume of lactose-free milk.'),
 item('salt',3,'g','fine salt','Reduce or omit to taste; salt does not provide the structure here.'),
 item('pepper',1.5,'g','ground black pepper','Use less if desired; the original recipe is strongly peppered. White pepper has a different flavor.'),
 item('butter',28,'g','unsalted butter','Use the same weight of a dairy-free butter alternative; flavor will differ.')],
 ['Whisk {{eggs}}, {{milk}}, {{salt}} and {{pepper}} in a bowl until evenly combined.',
  'Melt {{butter}} in a large nonstick frying pan over medium-low heat; do not let it brown.',
  'Pour in the egg mixture. Move a spatula slowly across the base and fold the setting curds over, cooking about 3–5 minutes until the eggs are set and no liquid egg remains.',
  'Remove from the heat and divide into three portions. Serve immediately; the pan’s retained heat continues to firm the eggs.'],
 'This adaptation keeps the six-egg formula, interprets the old milk and butter measures in metric, supplies weighed seasoning and a three-portion yield, and clarifies heat and doneness. Pan size and stove heat affect timing.',
 'Technique cross-check: https://www.incredibleegg.org/recipe/basic-scrambled-eggs/ ; this retains the historical formula rather than the reference recipe’s proportions.')
(root/'content-overrides.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
