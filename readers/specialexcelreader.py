import pandas

from readers.excelreader import ExcelReader
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


class LauExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(LauExcelReader, self).__init__()
        self.cols = ["Corporate Partner/Broker Policy Number", "Company Name", "Net Premium"]
        self.keep_cols = {"Policy": "Corporate_Partner_Broker_Policy_Number",
                          "Company": "Company_Name",
                          "File": "File",
                          "Amount": "Net_Premium"}
        self.folder_path = folder_path
        self.client_name = client_name

    def format_excel(self, df, file_path: str):

        # select the important columns
        df = df[self.cols]
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


class AgExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AgExcelReader, self).__init__()
        self.cols = ["Corporate Partner/Broker Policy Number", "Company Name", "Net Premium"]
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
            df = self.read_type_file(file_path, sheet="Data Table") # Need to create own function for this
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
        df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet)

        # Formatting -- move to a function
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        if "Corporate Partner/Broker Policy Number" in df.columns:
            df = df.rename(columns={"Corporate Partner/Broker Policy Number": "Broker Policy Number"})
        if "Aon Policy Number" in df.columns:
            df = df.rename(columns={"Aon Policy Number": "Broker Policy Number"})
        if "Net_Premium" in df.columns:
            df = df.rename(columns={"Net_Premium": "Net_Amount"})

        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')

        return df

class AgPExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AgPExcelReader, self).__init__()
        self.cols = ['Insured', 'Producer_#', 'Carrier_Doc_#', 'Carrier_Doc_Page_#',
                     'Carrier_Doc_Date', 'Policy_#', 'Line_Type___Coverage',
                     'Effective_Date', 'Due_Date', 'Gross_Due', 'Commission_Amount',
                     'Current_Past_Due', 'Net_Due']
        self.keep_cols = {"Policy": "Policy_#",
                          "Company": "Insured",
                          "File": "File",
                          "Amount": "Net_Due"}
        self.folder_path = folder_path
        self.client_name = client_name

    def read_file(self, file_path: str):
        names = ["Insured", "Insured Producer #"]
        position = self.find_position(file_path, names)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position)
        df = self.format_excel(df, file_path)

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

class AonPExcelReader(ExcelReader):
    def __init__(self, folder_path: str, client_name: str):
        super(AonPExcelReader, self).__init__()
        self.cols = ["CHECK_NUMBER", "REPORT_NAME", "PAY_TO_ID", "PAY_SITE_ID", "CONSOLIDATE_PAYSITE_ID",
                     "TAX_INDICATOR", "POLICY_NUMBER", "Named_Insured_Name", "INVOICE_NUMBER", "INVOICE_LINE_NO",
                     "TRANSACTION_EFFECTIVE_DATE","INVOICE_BILLING_DATE", "PAYSITE_NAME", "PAYEE_NAME",
                     "LOB_DESCRIPTION", "PAYMENT_REFERENCE_NUMBER", "BROKER_NAME", "COMM_RATE", "COMMISSION",
                     "PREMIUM", "OFFICE_CODE", "CORPORATE_OFFICE", "OFFICE_ADDRESS_LINE1", "OFFICE_ADDRESS_LINE2",
                     "OFFICE_ADDRESS_LINE3", "OFFICE_ADDRESS_LINE4", "OFFICE_ADDRESS_CITY", "OFFICE_ADDRESS_COUNTRY",
                     "OFFICE_ADDRESS_STATE", "OFFICE_ADDRESS_ZIP", "OFFICE_PHONE", "Commission_Type",
                     "CONSOLIDATE_ADDRESS_LINE1", "CONSOLIDATE_ADDRESS_LINE2", "CONSOLIDATE_ADDRESS_LINE3",
                     "CONSOLIDATE_ADDRESS_LINE4", "CONSOLIDATION_CITY", "CONSOLIDATION_COUNTRY_CODE",
                     "CONSOLIDATION_STATE_CODE", "CONSOLIDATION_ZIP", "Currency_Code", "OFFICE_BUSINESS_NAME",
                     "APPLIED_AMOUNT", "PAYMENT_DATE", "REASON_MCD", "TRANSACTION_ID", "CLIENT_ACCOUNT_ID",
                     "CLIENT_LEGAL_NAME", "allocation_mcd", "CLAIM_REF_NUMBER", "LANGUAGE_CODE",
                     "TRANSACTION_EFFECTIVE_DATE", "INVOICE_BILLING_DATE", "PAYMENT_DATE", "PAYMENT_TYPE"]
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
