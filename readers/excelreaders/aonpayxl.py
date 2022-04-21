from readers.excelreader import ExcelReader
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


class AonPExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AonPExcelReader, self).__init__()
        self.keep_cols = {"Policy": "POLICY_NUMBER",
                          "Company": "Named_Insured_Name",
                          "File": "File",
                          "Amount": "APPLIED_AMOUNT"}
        self.folder_path = folder_path
        self.client_name = client_name
        self.row_skips = 4

    def read_file(self, file_path: str):

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=self.row_skips)
        df = self.format_excel(df, file_path)

        return df

    def format_excel(self, df, file_path: str):
        return df