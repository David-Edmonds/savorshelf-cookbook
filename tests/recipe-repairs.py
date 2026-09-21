import importlib.util,pathlib,unittest
spec=importlib.util.spec_from_file_location('repairs',pathlib.Path(__file__).resolve().parents[1]/'recipe-repairs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Repairs(unittest.TestCase):
 def test_explicit_amounts(self):
  for text,value,unit in [('six ounces of flour',6,'oz'),('1 1/2 kg potatoes',1.5,'kg'),('1/4 cup sugar',.25,'cup')]:
   i=m.ingredient(text,0);self.assertEqual((i['amount'],i['unit']),(value,unit));self.assertEqual(i['sourceText'],text)
 def test_standard_forms_and_counts(self):
  for text,value,unit,name in [('½ cup sugar',.5,'cup','sugar'),('1½ kg potatoes',1.5,'kg','potatoes'),('half a pound of flour',.5,'lb','flour'),('three-quarters of a pound of butter',.75,'lb','butter'),('a quarter of a pound of sugar',.25,'lb','sugar'),('250g flour',250,'g','flour'),('2 tablespoonfuls sugar',2,'tbsp','sugar'),('a pint of milk',1,'pint','milk'),('two eggs',2,'','eggs'),('3 large onions, chopped',3,'','large onions, chopped')]:
   i=m.ingredient(text,0);self.assertEqual((i['amount'],i['unit'],i['name']),(value,unit,name),text);self.assertEqual(i['sourceText'],text)
 def test_no_inferred_package_or_regional_conversion(self):
  for text in ['half a dozen eggs','2 or 3 eggs','2 400g cans tomatoes','1 small handful parsley','a little sugar','3 spoonfuls yeast','two of allspice','1 pint and a half milk']:
   self.assertIsNone(m.ingredient(text,0)['amount'],text)
  self.assertEqual(m.ingredient('1 quart milk',0)['unit'],'quart')
 def test_fraction_steps_preserve_source(self):
  row={'originalIngredients':['½ cup flour'],'originalSteps':['Stir in ½ cup flour.']}
  items,steps,links=m.repair(row);self.assertEqual(steps,['Stir in {{source-0}}.']);self.assertEqual(items[0]['sourceText'],'½ cup flour')
 def test_ambiguous_amounts(self):
  for text in ['1-2 cups flour','1 pound and a half sugar','1 lb 2 oz flour','1 heaped tablespoon sugar','1/0 cup flour','some flour','one ounce milk','1 cup plus extra flour']:
   self.assertIsNone(m.ingredient(text,0)['amount'],text)
 def test_repeated_or_divided_method_not_linked(self):
  r={'originalIngredients':['1 cup flour'],'originalSteps':['Add 1 cup flour.','Add 1 cup flour.']};self.assertEqual(m.repair(r)[2],[])
  r['originalSteps']=['Add half the flour.'];self.assertEqual(m.repair(r)[2],[])
  r['originalSteps']=['Add 1 cup flour.'];self.assertEqual(m.repair(r)[1],['Add {{source-0}}.'])
unittest.main()
