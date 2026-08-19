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

    def test_calculate_text_render_size_single_line(self):
        mapping = {
            char: char
            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 /!-.'\""
        }

        width, height = Button._calculate_text_render_size("Play", 16, mapping)

        self.assertEqual(width, 4 * 16)
        self.assertEqual(height, 1 * 16)

    def test_calculate_text_render_size_multiline(self):
        mapping = {
            char: char
            for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 /!-.'\""
        }

        width, height = Button._calculate_text_render_size("AB\nCDE", 16, mapping)

        self.assertEqual(width, 3 * 16)
        self.assertEqual(height, 2 * 16)


if __name__ == "__main__":
    unittest.main()
