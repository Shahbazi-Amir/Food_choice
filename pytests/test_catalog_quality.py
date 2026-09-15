import unittest

from streamlit_foods import FOODS


class CatalogQualityTests(unittest.TestCase):
    def test_every_food_has_required_fields(self):
        required = {"name", "category", "weight", "cost", "prep", "cook", "ingredients"}
        for food in FOODS:
            self.assertTrue(required.issubset(food), food.get("name", "unknown"))

    def test_food_names_are_unique(self):
        names = [food["name"] for food in FOODS]
        self.assertEqual(len(names), len(set(names)))

    def test_times_are_positive(self):
        for food in FOODS:
            self.assertGreater(food["prep"], 0)
            self.assertGreater(food["cook"], 0)


if __name__ == "__main__":
    unittest.main()
