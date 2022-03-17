
import pandas as pd
import numpy as np
import os
import settings
from readers.filereader import FileReader


class ExcelReader(FileReader):
    def __init__(self, folder_path: str, client_name: str):
        super(ExcelReader, self).__init__(folder_path + settings.BORDEREAU_EXTENSION, client_name)
        self.path_extensions = ["xls", "xlsx", "xlsm"]
        self.cols = ["LAREAU Broker Code", "Corporate Partner/Broker Policy Number", "Company Name", "Net Premium"]

        return

    def read_file(self, file_path: str):

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, sheet_name="Data Table")
        df = self.format_excel(df, file_path)

        return df

    def format_excel(self, df, file_path: str):

        # select the important columns
        df = df[self.cols]
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')
        df["Excel_File"] = file_path
        df.dropna(subset=['Corporate_Partner_Broker_Policy_Number'])

        return df

