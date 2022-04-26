
import pandas as pd
from readers.filereader import FileReader
import os

class ExcelReader(FileReader):
    def __init__(self):
        super(ExcelReader, self).__init__()
        self.path_extensions = ["xls", "xlsx", "xlsm"]
        self.folder_path: str
        self.client_name: str

    def read_file(self, file_path: str):
        excel_path = f"{self.folder_path}/{file_path}"
        return pd.read_excel(excel_path)

    def format_excel(self, df, file_path: str):
        return df

    def find_position(self, file_path: str, names: list, sheet=0) -> int:
        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, sheet_name=sheet, nrows=100)
        position = -1

        for name in names:
            if name in df.columns:
                position = 0
                break

        for col_idx in range(len(df.columns)):
            column = df.iloc[:, col_idx].tolist()
            if pos := self.find_name(column, names) + 1:
                position = pos
                break
        return position

    def find_name(self, col, names):
        for name in names:
            if name in col:
                return col.index(name)
        return -1

    def categorise_excel(self, folder, not_counted_sheets, correct_name="Data Table"):
        keep = []
        remove = []
        for file in self.get_files():
            file_name = f"{folder}/{file}"
            xl = pd.ExcelFile(file_name)
            if len(list(xl.sheet_names)) > 8:
                remove.append(file)
            elif correct_name in xl.sheet_names:
                keep.append(file)
            else:
                file_sheet_count = 0
                for sheet in xl.sheet_names:
                    df = pd.read_excel(file_name, sheet_name=sheet)
                    if not df.empty and sheet not in not_counted_sheets:
                        file_sheet_count += 1
                if file_sheet_count != 1:
                    remove.append(file)
                else:
                    keep.append(file)
        print(len(keep))
        print(len(remove))
        print(remove)
        return keep, remove

