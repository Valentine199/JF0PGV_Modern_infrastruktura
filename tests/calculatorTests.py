import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.calculator import DataCalculator


class TestDataCalculator(unittest.TestCase):
    def _create_temp_file(self, content: str) -> Path:
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return Path(path)

    # ---------- Calculation tests ----------

    def test_do_calculation_add_sub_mul_div(self):
        calc = DataCalculator(file=self._create_temp_file("1 + 2\n"))

        # +
        self.assertAlmostEqual(
            calc.DoCalculation(["1", "+", "2"]),
            3.0
        )

        # -
        self.assertAlmostEqual(
            calc.DoCalculation(["5", "-", "3"]),
            2.0
        )

        # *
        self.assertAlmostEqual(
            calc.DoCalculation(["2", "*", "4"]),
            8.0
        )

        # /
        self.assertAlmostEqual(
            calc.DoCalculation(["10", "/", "2"]),
            5.0
        )

    def test_do_calculation_division_by_zero_raises(self):
        calc = DataCalculator(file=self._create_temp_file("1 / 0\n"))

        with self.assertRaises(ZeroDivisionError) as ctx:
            calc.DoCalculation(["1", "/", "0"])

        self.assertIn("D2 was 0 on division", str(ctx.exception))

    def test_do_calculation_unknown_operator_raises(self):
        calc = DataCalculator(file=self._create_temp_file("1 ? 2\n"))

        with self.assertRaises(AttributeError) as ctx:
            calc.DoCalculation(["1", "?", "2"])

        self.assertIn("Unknown opperand in file", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
