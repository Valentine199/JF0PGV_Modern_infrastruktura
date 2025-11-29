from typing import List

import src.loader as loader
from pathlib import Path

class DataCalculator:
    def __init__(self, file: Path):
        self.data_handler = loader.DataLoader(file=file)
        self.data_handler.ResetDataIndex()

    def ProcessFile(self):
        while self.data_handler.HasNext():
            try:
                data = self.data_handler.GetNextDataLine()

                result = self.DoCalculation(data)
                print(f"Input: {data[0]} {data[1]} {data[2]}")
                print(f"Result: {result}")
            except loader.FileDataError as e:
                print(e)
                break
            except ValueError as e:
                print(e)
                break



        self.data_handler.ResetDataIndex()


    def DoCalculation(self, data: List[str]) -> float:
        d1 = data[0]
        opp = data[1]
        d2 = data[2]

        match opp:
            case '+':
                return float(d1) + float(d2)
            case '-':
                return float(d1) - float(d2)
            case '*':
                return float(d1) * float(d2)
            case '/':
                if float(d2) == 0.0:
                    raise ZeroDivisionError("D2 was 0 on division")
                return float(d1) / float(d2)
            case _:
                raise AttributeError("Unknown opperand in file")



