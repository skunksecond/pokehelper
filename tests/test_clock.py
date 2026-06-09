import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from ui.clock import get_clock_display_strings, normalize_color


class ClockTests(unittest.TestCase):
    def test_normalize_color_accepts_hex_and_rgb(self):
        self.assertEqual(normalize_color("#ffffff"), (255, 255, 255))
        self.assertEqual(normalize_color([255, 0, 0]), (255, 0, 0))
        self.assertEqual(normalize_color((10, 20, 30)), (10, 20, 30))

    def test_get_clock_display_strings_returns_time_and_date(self):
        time_text, date_text = get_clock_display_strings()
        self.assertTrue(time_text)
        self.assertTrue(date_text)
        self.assertIn(":", time_text)
        self.assertTrue("/" in date_text or "-" in date_text)


if __name__ == "__main__":
    unittest.main()
