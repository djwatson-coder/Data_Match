from readers.excelreader import ExcelReader
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


class AgPExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AgPExcelReader, self).__init__()
        self.keep_cols = {"File": "File",
                          "Policy": "Policy_#",
                          "Effective_Date": "Effective_Date",
                          "Company": "Insured",
                          "Gross_Amount": "Gross_Due",
                          "Commission_Amount": "Commission_Amount",
                          "Net_Amount": "Net_Due"}
        self.folder_path = folder_path
        self.client_name = client_name

    def read_file(self, file_path: str):
        names = ["Insured", "Insured Producer #"]
        position = self.find_position(file_path, names)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position)
        df = self.format_excel(df, file_path)
        # print(df.columns)

        return df

    def format_excel(self, df: pd.DataFrame, file_path: str):
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')
        df = df.dropna(subset=['Policy_#'])
        if "Insured_Producer_#" in df.columns:
            df = df.rename(columns={"Insured_Producer_#": "Insured"})
        df = df[((df.Insured != 'Insured') & (df.Insured != 'Insured Producer #'))]

        df["Net_Due"] = df["Net_Due"].astype('str')
        df["Net_Due"] = df["Net_Due"].str.replace('$', '')
        df["Net_Due"] = df["Net_Due"].str.replace(',', '')
        df["Net_Due"] = df["Net_Due"].str.replace('(', '-')
        df["Net_Due"] = df["Net_Due"].str.replace(')', '')

        return df


