import unittest
from streamlit_logic import build_candidate_pool, rank_nearest

class SoftRankingTests(unittest.TestCase):
    def setUp(self):
        self.foods=[
            {"name":"خورش کند","family":"خورش و قلیه","methods":["خورشتی/آرام‌پز"],"weight":"سنگین","cost":"گران","prep":20,"cook":80},
            {"name":"کوکو سریع","family":"کوکو و املت","methods":["تابه‌ای"],"weight":"سبک","cost":"اقتصادی","prep":10,"cook":25},
            {"name":"جوجه گریل","family":"کباب، بریان و تنوری","methods":["گریل/منقل"],"weight":"متوسط","cost":"معمولی","prep":15,"cook":25},
            {"name":"برگر منتخب","family":"ساندویچ و غذای سریع","methods":["گریل/منقل","تابه‌ای"],"weight":"سنگین","cost":"معمولی","prep":10,"cook":20},
        ]
    def test_unknown_catalog_food_is_not_in_user_pool(self):
        pool=build_candidate_pool(self.foods,{"خورش کند","کوکو سریع"},{"برگر منتخب"},allow_new=True)
        self.assertNotIn("جوجه گریل",{x["name"] for x in pool})
    def test_family_semantics_are_not_sacrificed_for_time(self):
        ranked=rank_nearest(self.foods,{"خورش کند","کوکو سریع"},set(),allow_new=False,time_filter="تا ۳۰ دقیقه",selected_families=["خورش و قلیه"],priority="time")
        self.assertEqual(ranked[0]["name"],"خورش کند")
        self.assertFalse(ranked[0]["_exact"])
    def test_catalog_fallback_still_respects_method(self):
        ranked=rank_nearest(self.foods,{"کوکو سریع"},set(),allow_new=False,time_filter="تا ۱ ساعت",selected_methods=["گریل/منقل"],priority="time")
        self.assertTrue(ranked)
        self.assertTrue(all("گریل/منقل" in x["methods"] for x in ranked))
        self.assertEqual(ranked[0]["_source"],"catalog-fallback")

if __name__=="__main__":unittest.main()
