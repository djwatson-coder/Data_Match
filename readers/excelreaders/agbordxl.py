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
                          "Effective_Date": "Effective_Date",
                          "File": "File",
                          "Net_Amount": "Net_Amount",
                          "Gross_Amount": "Gross_Amount"}
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
        names = ["Corporate Partner/Broker Policy Number", "Broker Policy Number", "DAS Policy Number"]
        position = self.find_position(file_path, names, sheet)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet, nrows=1000)

        df.columns = df.columns.str.replace(r' \(.*\)', '')
        df.columns = df.columns.str.replace('/', '_')
        df.columns = df.columns.str.replace('.', '_')
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.lower()

        # Formatting -- move to a function
        # df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        BPN_Names = ["broker_policy_number", "corporate_partner_broker_policy_number", "das_policy_number"]
        EFD_Names = ["cover_from_date"]
        CPN_Names = ["company_name", "first_name"]
        NAM_Names = ["net_premium"]
        GPN_Names = ["gross_premium"]

        df = self.find_rename_columns(df, "Broker_Policy_Number", BPN_Names)
        df = self.find_rename_columns(df, "Company_Name", CPN_Names)
        df = self.find_rename_columns(df, "Effective_Date", EFD_Names)
        df = self.find_rename_columns(df, "Net_Amount", NAM_Names)
        df = self.find_rename_columns(df, "Gross_Amount", GPN_Names)

        if "Gross_Amount" not in df.columns:
            print(df.columns)

        df = df[["Broker_Policy_Number", "Company_Name", "Effective_Date",
                 "Net_Amount", "Gross_Amount"]]

        return df

    def triage_data(self):
        correct_names = ["Data Table", "AON Municipalities", "Bordereaux"]
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



