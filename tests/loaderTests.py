import os
import tempfile
import unittest
from pathlib import Path

from src.loader import DataLoader, FileDataError


class TestDataLoader(unittest.TestCase):
    def _create_temp_file(self, content: str) -> Path:
        """Helper to create a temporary file with given content."""
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return Path(path)

    def test_get_next_data_line_valid_arithmetic_file(self):
        """
        File:
        1 + 2
        3 + 4
        100 - 50
        2 * 10000
        50 / 2
        """
        content = (
            "1 + 2\n"
            "3 + 4\n"
            "100 - 50\n"
            "2 * 10000\n"
            "50 / 2\n"
        )
        path = self._create_temp_file(content)
        loader = DataLoader(path)

        self.assertTrue(loader.HasNext())

        self.assertEqual(loader.GetNextDataLine(), ["1", "+", "2"])
        self.assertTrue(loader.HasNext())

        self.assertEqual(loader.GetNextDataLine(), ["3", "+", "4"])
        self.assertTrue(loader.HasNext())

        self.assertEqual(loader.GetNextDataLine(), ["100", "-", "50"])
        self.assertTrue(loader.HasNext())

        self.assertEqual(loader.GetNextDataLine(), ["2", "*", "10000"])
        self.assertTrue(loader.HasNext())

        self.assertEqual(loader.GetNextDataLine(), ["50", "/", "2"])
        self.assertFalse(loader.HasNext())

    def test_get_next_data_line_past_end_raises_value_error(self):
        content = "1 + 2\n"
        path = self._create_temp_file(content)
        loader = DataLoader(path)


        _ = loader.GetNextDataLine()
        self.assertFalse(loader.HasNext())


        with self.assertRaises(ValueError) as ctx:
            loader.GetNextDataLine()

        self.assertIn("You already read this file", str(ctx.exception))

    def test_malformed_line_raises_file_data_error(self):
        # Second line is malformed: only 2 tokens instead of 3
        content = (
            "1 + 2\n"
            "3 +\n"
        )
        path = self._create_temp_file(content)
        loader = DataLoader(path)


        self.assertEqual(loader.GetNextDataLine(), ["1", "+", "2"])


        with self.assertRaises(FileDataError) as ctx:
            loader.GetNextDataLine()

        self.assertIn("The input file was malformed", str(ctx.exception))

    def test_reset_data_index_allows_reread(self):
        content = (
            "1 + 2\n"
            "3 + 4\n"
        )
        path = self._create_temp_file(content)
        loader = DataLoader(path)

        first_line = loader.GetNextDataLine()
        self.assertEqual(first_line, ["1", "+", "2"])
        self.assertTrue(loader.HasNext())

        # Reset index and read again from the top
        loader.ResetDataIndex()
        self.assertTrue(loader.HasNext())

        first_line_again = loader.GetNextDataLine()
        self.assertEqual(first_line_again, ["1", "+", "2"])

    def test_empty_file_has_no_next_and_raises_on_read(self):
        path = self._create_temp_file("")
        loader = DataLoader(path)

        self.assertFalse(loader.HasNext())

        with self.assertRaises(ValueError) as ctx:
            loader.GetNextDataLine()

        self.assertIn("You already read this file", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
