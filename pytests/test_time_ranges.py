import unittest

from streamlit_logic import matches_time


class TimeRangeTests(unittest.TestCase):
    def test_90_minute_food_fits_90_minute_filter(self):
        self.assertTrue(matches_time({"prep": 30, "cook": 60}, "تا ۱ ساعت و نیم"))

    def test_91_minute_food_does_not_fit_90_minute_filter(self):
        self.assertFalse(matches_time({"prep": 31, "cook": 60}, "تا ۱ ساعت و نیم"))


if __name__ == "__main__":
    unittest.main()
