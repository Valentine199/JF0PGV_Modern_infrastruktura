from pathlib import Path
from typing import List

class FileDataError(Exception):
    pass

class DataLoader:
    def __init__(self, file: Path):
        with open(file, "r") as f:
            self.lines: List[str] = f.readlines()

        self.load_index = -1

    def GetNextDataLine(self) -> List[str]:
        self.load_index += 1

        try:
            line_data = self.lines[self.load_index].split()
        except IndexError as e:
            raise ValueError("You already read this file. Provide new file or reset the index to reload")

        if len(line_data) != 3:
            raise FileDataError("The input file was malformed")

        return line_data

    def ResetDataIndex(self) -> None:
        self.load_index = -1

    def HasNext(self) -> bool:
        return self.load_index < len(self.lines) - 1





