from readers.excelreader import ExcelReader
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


class AgExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AgExcelReader, self).__init__()
        self.keep_cols = {"Policy": "Broker_Policy_Number",
                          "Company": "Company_Name",
                          "File": "File",
                          "Amount": "Net_Amount"}
        self.folder_path = folder_path
        self.client_name = client_name

    def read_file(self, file_path: str):
        # Need to read different excels from different categorised folders
        excel_path = f"{self.folder_path}/{file_path}"
        xl = pd.ExcelFile(excel_path)
        if "master" in file_path.lower():
            new_folder = "T1"
            df = self.read_type_file(file_path, sheet="Data Table")  # Need to create own function for this
        elif "Data Table" in xl.sheet_names:
            new_folder = "T2"
            df = self.read_type_file(file_path, sheet="Data Table")
        else:
            new_folder = "T3"
            df = self.read_type_file(file_path, sheet=0)

        df = self.format_excel(df, file_path)

        return df

    def format_excel(self, df, file_path: str):

        return df

    def read_type_file(self, file_path: str, sheet):
        names = ["Corporate Partner/Broker Policy Number", "Broker Policy Number", "Aon Policy Number"]
        position = self.find_position(file_path, names, sheet)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet, nrows=100)

        # Formatting -- move to a function
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        if "Corporate Partner/Broker Policy Number" in df.columns:
            df = df.rename(columns={"Corporate Partner/Broker Policy Number": "Broker Policy Number"})
        if "Aon Policy Number" in df.columns:
            df = df.rename(columns={"Aon Policy Number": "Broker Policy Number"})
        if "Net_Premium" in df.columns:
            df = df.rename(columns={"Net_Premium": "Net_Amount"})
        if "Net Premium" in df.columns:
            df = df.rename(columns={"Net_Premium": "Net_Amount"})

        # df = df[["Broker_Policy_Number", "Company_Name", "Net_Amount"]]

        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')

        return df