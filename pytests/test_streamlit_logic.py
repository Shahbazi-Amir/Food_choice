import random
import unittest

from streamlit_foods import CATEGORIES, FOODS
from streamlit_logic import filter_foods, format_minutes, recommend_food, suggested_new_foods, total_minutes


class StreamlitLogicTests(unittest.TestCase):
    def test_catalog_has_at_least_40_foods(self):
        self.assertGreaterEqual(len(FOODS), 40)

    def test_catalog_has_reasonable_categories(self):
        expected = {"پلو و چلو", "خورش", "آش و سوپ", "غذای نانی و خوراک", "ساندویچ و فست‌فود خانگی"}
        self.assertTrue(expected.issubset(set(CATEGORIES)))

    def test_time_format_below_one_hour(self):
        self.assertEqual(format_minutes(45), "45 دقیقه")

    def test_time_format_exact_hour(self):
        self.assertEqual(format_minutes(60), "1 ساعت")

    def test_time_format_over_one_hour(self):
        self.assertEqual(format_minutes(110), "1 ساعت و 50 دقیقه")

    def test_total_minutes_adds_prep_and_cook(self):
        self.assertEqual(total_minutes({"prep": 20, "cook": 40}), 60)

    def test_filters_can_be_combined(self):
        results = filter_foods(
            FOODS,
            time_filter="تا ۱ ساعت",
            selected_costs=["اقتصادی"],
            selected_weights=["سبک"],
        )
        self.assertTrue(results)
        for food in results:
            self.assertLessEqual(total_minutes(food), 60)
            self.assertEqual(food["cost"], "اقتصادی")
            self.assertEqual(food["weight"], "سبک")

    def test_category_filter_works_with_other_filters(self):
        results = filter_foods(
            FOODS,
            time_filter="تا ۱ ساعت و نیم",
            selected_categories=["آش و سوپ"],
            selected_weights=["سبک"],
        )
        self.assertTrue(results)
        self.assertTrue(all(food["category"] == "آش و سوپ" for food in results))
        self.assertTrue(all(food["weight"] == "سبک" for food in results))

    def test_familiar_foods_are_preferred(self):
        foods = [
            {"name": "معمول", "category": "x", "weight": "سبک", "cost": "اقتصادی", "prep": 10, "cook": 10},
            {"name": "جدید", "category": "x", "weight": "سبک", "cost": "اقتصادی", "prep": 10, "cook": 10},
        ]
        choice = recommend_food(foods, {"معمول"}, {"جدید"}, allow_new=True, rng=random.Random(1))
        self.assertEqual(choice["name"], "معمول")

    def test_new_suggestions_exclude_usual_foods(self):
        usual = {FOODS[0]["name"], FOODS[1]["name"]}
        suggestions = suggested_new_foods(FOODS, usual, limit=10)
        self.assertTrue(set(suggestions).isdisjoint(usual))


if __name__ == "__main__":
    unittest.main()
