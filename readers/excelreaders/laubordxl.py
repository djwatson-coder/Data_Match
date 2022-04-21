from readers.excelreader import ExcelReader
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


class LauExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(LauExcelReader, self).__init__()
        self.keep_cols = {"Policy": "Corporate_Partner_Broker_Policy_Number",
                          "Company": "Company_Name",
                          "File": "File",
                          "Amount": "Net_Premium"}
        self.folder_path = folder_path
        self.client_name = client_name

    def format_excel(self, df, file_path: str):

        # select the important columns
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')
        df['Corporate_Partner_Broker_Policy_Number'].replace('', np.nan, inplace=True)
        df = df.dropna(subset=['Corporate_Partner_Broker_Policy_Number'])

        return df

    def read_file(self, file_path: str):

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, sheet_name="Data Table")
        df = self.format_excel(df, file_path)

        return df

