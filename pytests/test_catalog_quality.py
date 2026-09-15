import unittest

from streamlit_foods import FAMILIES, FOODS, METHODS

class CatalogQualityTests(unittest.TestCase):
    def test_every_food_has_required_fields(self):
        required={"name","category","family","methods","weight","cost","prep","cook","ingredients"}
        for food in FOODS:self.assertTrue(required.issubset(food),food.get("name","unknown"))

    def test_food_names_are_unique(self):
        names=[food["name"] for food in FOODS];self.assertEqual(len(names),len(set(names)))

    def test_times_are_valid(self):
        for food in FOODS:
            self.assertGreaterEqual(food["prep"],0);self.assertGreaterEqual(food["cook"],0);self.assertGreater(food["prep"]+food["cook"],0)

    def test_all_families_and_methods_are_known(self):
        for food in FOODS:
            self.assertIn(food["family"],FAMILIES,food["name"])
            self.assertTrue(food["methods"],food["name"])
            for method in food["methods"]:self.assertIn(method,METHODS,f"{food['name']} -> {method}")

if __name__=="__main__":unittest.main()
