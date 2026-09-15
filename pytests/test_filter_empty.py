import unittest

from streamlit_foods import FOODS
from streamlit_logic import filter_foods


class EmptyFilterTests(unittest.TestCase):
    def test_impossible_combination_can_return_empty(self):
        results = filter_foods(
            FOODS,
            time_filter="تا ۳۰ دقیقه",
            selected_costs=["گران"],
            selected_weights=["سنگین"],
            selected_categories=["خورش"],
        )
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
