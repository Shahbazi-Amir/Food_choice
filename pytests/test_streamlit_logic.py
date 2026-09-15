import random
import unittest

from streamlit_foods import FAMILIES, FOODS, METHODS
from streamlit_logic import filter_foods, format_minutes, rank_nearest, recommend_food, suggested_new_foods, total_minutes
from streamlit_recipe import recipe_for


class StreamlitLogicTests(unittest.TestCase):
    def test_catalog_has_at_least_60_foods(self):
        self.assertGreaterEqual(len(FOODS), 60)

    def test_catalog_has_reasonable_families(self):
        expected={"چلو، پلو و کته","خورش و قلیه","آش، سوپ و حلیم","کباب، بریان و تنوری","کوکو و املت"}
        self.assertTrue(expected.issubset(set(FAMILIES)))
        self.assertIn("گریل/منقل",METHODS)

    def test_time_format_below_one_hour(self): self.assertEqual(format_minutes(45),"45 دقیقه")
    def test_time_format_exact_hour(self): self.assertEqual(format_minutes(60),"1 ساعت")
    def test_time_format_over_one_hour(self): self.assertEqual(format_minutes(110),"1 ساعت و 50 دقیقه")
    def test_total_minutes_adds_prep_and_cook(self): self.assertEqual(total_minutes({"prep":20,"cook":40}),60)

    def test_filters_can_be_combined(self):
        results=filter_foods(FOODS,time_filter="تا ۱ ساعت",selected_costs=["اقتصادی"],selected_weights=["سبک"])
        self.assertTrue(results)
        for food in results:
            self.assertLessEqual(total_minutes(food),60);self.assertEqual(food["cost"],"اقتصادی");self.assertEqual(food["weight"],"سبک")

    def test_family_filter_works_with_other_filters(self):
        results=filter_foods(FOODS,time_filter="تا ۲ ساعت",selected_categories=["آش، سوپ و حلیم"],selected_weights=["سبک"])
        self.assertTrue(results)
        self.assertTrue(all(food["family"]=="آش، سوپ و حلیم" for food in results))

    def test_grill_constraint_never_returns_kuku(self):
        usual={"کوکو سبزی"}
        ranked=rank_nearest(FOODS,usual,set(),allow_new=False,time_filter="تا ۱ ساعت",selected_methods=["گریل/منقل"],priority="time")
        self.assertTrue(ranked)
        self.assertNotEqual(ranked[0]["name"],"کوکو سبزی")
        self.assertIn("گریل/منقل",ranked[0]["methods"])
        self.assertEqual(ranked[0]["_source"],"catalog-fallback")

    def test_method_is_hard_even_when_time_is_priority(self):
        ranked=rank_nearest(FOODS,{"کوکو سبزی"},{"همبرگر خانگی"},allow_new=True,time_filter="تا ۳۰ دقیقه",selected_methods=["گریل/منقل"],priority="time")
        self.assertTrue(ranked)
        self.assertTrue(all("گریل/منقل" in item["methods"] for item in ranked))

    def test_familiar_foods_are_preferred(self):
        foods=[{"name":"معمول","family":"x","methods":["تابه‌ای"],"weight":"سبک","cost":"اقتصادی","prep":10,"cook":10},{"name":"جدید","family":"x","methods":["تابه‌ای"],"weight":"سبک","cost":"اقتصادی","prep":10,"cook":10}]
        choice=recommend_food(foods,{"معمول"},{"جدید"},allow_new=True,rng=random.Random(1))
        self.assertEqual(choice["name"],"معمول")

    def test_new_suggestions_exclude_usual_foods(self):
        usual={FOODS[0]["name"],FOODS[1]["name"]};suggestions=suggested_new_foods(FOODS,usual,limit=10);self.assertTrue(set(suggestions).isdisjoint(usual))

    def test_every_food_can_render_recipe(self):
        for food in FOODS:
            recipe=recipe_for(food)
            self.assertGreaterEqual(len(recipe["steps"]),3,food["name"])
            self.assertGreaterEqual(len(recipe["variants"]),1,food["name"])


if __name__=="__main__":unittest.main()
