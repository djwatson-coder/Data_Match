from readers.excelreader import ExcelReader
import pandas as pd
import warnings
warnings.simplefilter("ignore")


class BflExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(BflExcelReader, self).__init__()
        self.keep_cols = {"Policy": "Corporate Partner/Broker Policy Number",
                          "Company": "Company Name",
                          "File": "File",
                          "Amount": "Net Premium"}
        self.folder_path = folder_path
        self.client_name = client_name
        self.row_skips = 0

    def read_file(self, file_path: str):
        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=self.row_skips)
        df = self.format_excel(df, file_path)

        return df

    def format_excel(self, df, file_path: str):
        df = df.dropna(subset=['Company Name'])
        return df
