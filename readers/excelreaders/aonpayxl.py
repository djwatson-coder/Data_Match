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
        self.row_skips = 9

    def read_file(self, file_path: str):


        excel_path = f"{self.folder_path}/{file_path}"
        xl = pd.ExcelFile(excel_path)
        if 'Remittance Advice' in xl.sheet_names:
            df = pd.read_excel(excel_path, skiprows=9)
            df = self.format_type_1(df)
        elif len(xl.sheet_names) > 1:
            sheet_names = list(xl.sheet_names)
            position = self.find_position(file_path, ['Office\nSucc.'], sheet_names[0])
            df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet_names[0])
            for sheet in sheet_names[1:]:
                position = self.find_position(file_path, ['Office\nSucc.'], sheet)
                df1 = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet)
                df = pd.concat([df, df1])
            df = self.format_type_1(df)
        else:
            df = pd.read_excel(excel_path, skiprows=4)

        df = self.format_excel(df, file_path)

        return df

    def format_excel(self, df, file_path: str):
        df = df[["POLICY_NUMBER", "Named_Insured_Name", "APPLIED_AMOUNT"]]

        return df

    def format_type_1(self, df):
        """ Skip 9 rows """
        df = df.rename(columns={"Policy Number\nNo de la Police": "POLICY_NUMBER",
                                "Client Number\nNo du cliente": "Named_Insured_Name",
                                "Net Balance\nSolde": "APPLIED_AMOUNT"})

        return df
