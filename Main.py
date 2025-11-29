from pathlib import Path
from src.calculator import DataCalculator

folder = "data"
data = Path(folder) / "data.txt"

calc = DataCalculator(data)
calc.ProcessFile()