import unittest

from streamlit_foods import FOODS
from streamlit_logic import suggested_new_foods


class ProfileSuggestionTests(unittest.TestCase):
    def test_suggestions_respect_limit(self):
        suggestions = suggested_new_foods(FOODS, set(), limit=6)
        self.assertLessEqual(len(suggestions), 6)

    def test_suggestions_do_not_repeat_usual_foods(self):
        usual = {food["name"] for food in FOODS[:10]}
        suggestions = suggested_new_foods(FOODS, usual, limit=10)
        self.assertFalse(set(suggestions) & usual)


if __name__ == "__main__":
    unittest.main()
