import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.loader import DataLoader, FileDataError
from src.calculator import DataCalculator


class TestLoaderCalculatorIntegration(unittest.TestCase):
    def _create_temp_file(self, content: str) -> Path:
        """Helper to create a temporary file with given content."""
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return Path(path)

    def test_full_file_calculations_happy_path(self):
        content = (
            "1 + 2\n"
            "3 + 4\n"
            "100 - 50\n"
            "2 * 10000\n"
            "50 / 2\n"
        )
        path = self._create_temp_file(content)
        calc = DataCalculator(file=path)

        results = []
        while calc.data_handler.HasNext():
            line = calc.data_handler.GetNextDataLine()
            result = calc.DoCalculation(line)
            results.append(result)

        self.assertEqual(
            results,
            [3.0, 7.0, 50.0, 20000.0, 25.0]
        )

        # We hit EOF
        self.assertFalse(calc.data_handler.HasNext())

        # Reset and ensure we can re-read
        calc.data_handler.ResetDataIndex()
        self.assertTrue(calc.data_handler.HasNext())
        self.assertEqual(calc.data_handler.GetNextDataLine(), ["1", "+", "2"])

    def test_process_file_stops_on_malformed_line_and_resets_index(self):
        """
        Integration: ProcessFile + DataLoader error.
        Second line is malformed (only two tokens).
        """
        content = (
            "1 + 2\n"
            "3 +\n"
            "5 * 6\n"
        )
        path = self._create_temp_file(content)
        calc = DataCalculator(file=path)

        with patch("builtins.print") as mock_print:
            calc.ProcessFile()

        # Should have printed the FileDataError message
        self.assertTrue(mock_print.called)
        printed = " ".join(str(a) for a in mock_print.call_args[0])
        self.assertIn("The input file was malformed", printed)

        # Index should be reset to -1 after ProcessFile
        self.assertEqual(calc.data_handler.load_index, -1)
        self.assertTrue(calc.data_handler.HasNext())

        # First line should be readable again
        line = calc.data_handler.GetNextDataLine()
        self.assertEqual(line, ["1", "+", "2"])

    def test_integration_unknown_operator_from_file(self):
        """
        Integration: Loader passes through an unknown operator,
        Calculator blows up with AttributeError.
        """
        content = "1 ? 2\n"
        path = self._create_temp_file(content)
        calc = DataCalculator(file=path)

        line = calc.data_handler.GetNextDataLine()
        self.assertEqual(line, ["1", "?", "2"])

        with self.assertRaises(AttributeError) as ctx:
            calc.DoCalculation(line)

        self.assertIn("Unknown opperand in file", str(ctx.exception))

    def test_integration_division_by_zero_from_file(self):
        """
        Integration: Loader passes division by zero, Calculator
        raises ZeroDivisionError.
        """
        content = "1 / 0\n"
        path = self._create_temp_file(content)
        calc = DataCalculator(file=path)

        line = calc.data_handler.GetNextDataLine()
        self.assertEqual(line, ["1", "/", "0"])

        with self.assertRaises(ZeroDivisionError) as ctx:
            calc.DoCalculation(line)

        self.assertIn("D2 was 0 on division", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
