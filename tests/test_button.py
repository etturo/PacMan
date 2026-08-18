import unittest

from src.graphics.ui.button import Button


class TestButton(unittest.TestCase):
    def test_calculate_text_size_single_line(self):
        mapping = {
            char: char
            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 /!-.'\""
        }

        width, height = Button._calculate_text_size("PUZZOLO", 16, 5, mapping)

        self.assertGreater(width, 0)
        self.assertGreater(height, 0)
        self.assertEqual(width, (7 * (16 + 5)) + (16 * 2))
        self.assertEqual(height, (1 * (16 + 5)) + (16 * 2))


if __name__ == "__main__":
    unittest.main()
