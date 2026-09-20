import importlib.util,pathlib,unittest
spec=importlib.util.spec_from_file_location('repairs',pathlib.Path(__file__).resolve().parents[1]/'recipe-repairs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Repairs(unittest.TestCase):
 def test_explicit_amounts(self):
  for text,value,unit in [('six ounces of flour',6,'oz'),('1 1/2 kg potatoes',1.5,'kg'),('1/4 cup sugar',.25,'cup')]:
   i=m.ingredient(text,0);self.assertEqual((i['amount'],i['unit']),(value,unit));self.assertEqual(i['sourceText'],text)
 def test_ambiguous_amounts(self):
  for text in ['1-2 cups flour','1 pound and a half sugar','1 lb 2 oz flour','1 heaped tablespoon sugar','1/0 cup flour','some flour','one ounce milk','1 cup plus extra flour']:
   self.assertIsNone(m.ingredient(text,0)['amount'],text)
 def test_repeated_or_divided_method_not_linked(self):
  r={'originalIngredients':['1 cup flour'],'originalSteps':['Add 1 cup flour.','Add 1 cup flour.']};self.assertEqual(m.repair(r)[2],[])
  r['originalSteps']=['Add half the flour.'];self.assertEqual(m.repair(r)[2],[])
  r['originalSteps']=['Add 1 cup flour.'];self.assertEqual(m.repair(r)[1],['Add {{source-0}}.'])
unittest.main()
