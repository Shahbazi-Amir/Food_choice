import unittest

from streamlit_logic import build_candidate_pool, rank_nearest


class SoftRankingTests(unittest.TestCase):
    def setUp(self):
        self.foods = [
            {"name":"آشنا کند","category":"خورش","weight":"سنگین","cost":"گران","prep":20,"cook":80},
            {"name":"آشنا سریع","category":"خوراک","weight":"سبک","cost":"اقتصادی","prep":10,"cook":25},
            {"name":"غریبه عالی","category":"خوراک","weight":"سبک","cost":"اقتصادی","prep":5,"cook":15},
            {"name":"جدید منتخب","category":"خوراک","weight":"سبک","cost":"اقتصادی","prep":10,"cook":30},
        ]

    def test_unknown_catalog_food_is_not_in_user_pool(self):
        pool = build_candidate_pool(self.foods, {"آشنا کند","آشنا سریع"}, {"جدید منتخب"}, allow_new=True)
        self.assertNotIn("غریبه عالی", {item["name"] for item in pool})

    def test_impossible_combination_returns_nearest(self):
        ranked = rank_nearest(
            self.foods,
            {"آشنا کند","آشنا سریع"},
            set(),
            allow_new=False,
            time_filter="تا ۳۰ دقیقه",
            selected_costs=["اقتصادی"],
            selected_weights=["سبک"],
            selected_categories=["خورش"],
            priority="time",
        )
        self.assertTrue(ranked)
        self.assertEqual(ranked[0]["name"], "آشنا سریع")
        self.assertFalse(ranked[0]["_exact"])

    def test_priority_can_change_best_choice(self):
        usual={"آشنا کند","آشنا سریع"}
        by_time=rank_nearest(self.foods,usual,set(),allow_new=False,time_filter="تا ۱ ساعت",selected_costs=["اقتصادی"],selected_categories=["خورش"],priority="time")
        by_category=rank_nearest(self.foods,usual,set(),allow_new=False,time_filter="تا ۱ ساعت",selected_costs=["اقتصادی"],selected_categories=["خورش"],priority="category")
        self.assertEqual(by_time[0]["name"],"آشنا سریع")
        self.assertEqual(by_category[0]["name"],"آشنا کند")


if __name__ == "__main__":
    unittest.main()
