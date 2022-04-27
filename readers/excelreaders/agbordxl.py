from readers.excelreader import ExcelReader
import pandas as pd
import warnings
import utils.ostools as ost
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
        if "Data Table" in xl.sheet_names:
            df = self.read_type_file(file_path, sheet="Data Table")
        else:
            correct_sheet = self.get_correct_sheet(file_path)
            df = self.read_type_file(file_path, sheet=correct_sheet)

        df = self.format_excel(df, file_path)

        return df

    def get_correct_sheet(self, file_path):

        excel_path = f"{self.folder_path}/{file_path}"
        xl = pd.ExcelFile(excel_path)
        for sheet in xl.sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet)
            if not df.empty and sheet != "SAMPLE":
                return sheet

    def format_excel(self, df, file_path: str):

        return df

    def read_type_file(self, file_path: str, sheet):
        names = ["Corporate Partner/Broker Policy Number", "Broker Policy Number", "Aon Policy Number",
                 "Policy No.", "Das Policy Number", "Policy #", "DAS Policy Number", "Certificate No.",
                 "POLICY_NUMBER"]
        position = self.find_position(file_path, names, sheet)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet, nrows=1000)

        df.columns = df.columns.str.replace(' ', '')
        df.columns = df.columns.str.replace('/', '')
        df.columns = df.columns.str.replace('.', '')
        df.columns = df.columns.str.replace('_', '')
        df.columns = df.columns.str.lower()

        # Formatting -- move to a function
        # df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        BPN_Names = ["corporatepartnerbrokerpolicynumber",
                     "aonpolicynumber",
                     "corporatepartnernumber",
                     "daspolicynumber",
                     "policyno",
                     "policy#",
                     "certificateno",
                     "policynumber"]
        NAM_Names = ["netpremium",
                     "daspremium",
                     "netwrittenpremium",
                     "daspolicynumber",
                     "policyno",
                     "totalpremium",
                     "19-20daspremium",
                     "appliedamount",
                     "grosspremium",
                     "premium"]  # be careful with this one - should come last

        df = self.find_rename_columns(df, "brokerpolicynumber", BPN_Names)
        df = self.find_rename_columns(df, "netamount", NAM_Names)

        df = df.rename(columns={"brokerpolicynumber": "Broker_Policy_Number",
                                "netamount": "Net_Amount"})

        if "Company_Name" not in df.columns:
            df["Company_Name"] = "No Company Name"

        if "Broker_Policy_Number" not in df.columns or "Net_Amount" not in df.columns:
            print(df.columns)

        df = df[["Broker_Policy_Number", "Company_Name", "Net_Amount"]]

        return df

    def triage_data(self):
        correct_names = ["Data Table", "AON Municipalities"]
        new_folder = f"{self.folder_path}/Excluded"
        ost.create_directory(new_folder)
        keep_files, remove_files = self.categorise_excel(self.folder_path, ["SAMPLE"], correct_names)
        ost.move_files(self.folder_path, new_folder, remove_files, remove=True)
        return

    def find_rename_columns(self, df, correct_col, alt_cols):
        for col in alt_cols:
            if col in df.columns and correct_col not in df.columns:
                df = df.rename(columns={col: correct_col})
        return df
