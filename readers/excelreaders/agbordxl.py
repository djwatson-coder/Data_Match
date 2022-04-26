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
        names = ["Corporate Partner/Broker Policy Number", "Broker Policy Number", "Aon Policy Number"]
        position = self.find_position(file_path, names, sheet)

        excel_path = f"{self.folder_path}/{file_path}"
        df = pd.read_excel(excel_path, skiprows=position, sheet_name=sheet, nrows=1000)

        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')

        # Formatting -- move to a function
        # df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        if "Corporate_Partner_Broker_Policy_Number" in df.columns:
            df = df.rename(columns={"Corporate_Partner_Broker_Policy_Number": "Broker_Policy_Number"})
        if "Aon_Policy_Number" in df.columns:
            df = df.rename(columns={"Aon_Policy_Number": "Broker_Policy_Number"})
        if "DAS_Policy_Number" in df.columns and ("Broker_Policy_Number" not in df.columns):
            df = df.rename(columns={"DAS_Policy_Number": "Broker_Policy_Number"})
        if "Net_Premium" in df.columns and ("Net_Amount" not in df.columns):
            df = df.rename(columns={"Net_Premium": "Net_Amount"})
        if "Net_premium" in df.columns and ("Net_Amount" not in df.columns):
            df = df.rename(columns={"Net_premium": "Net_Amount"})
        if "Company_Name" not in df.columns:
            df["Company_Name"] = "No Company Name"




        #print(df.columns)
        df = df[["Broker_Policy_Number", "Company_Name", "Net_Amount"]]

        return df

    def triage_data(self):
        new_folder = f"{self.folder_path}/Excluded"
        ost.create_directory(new_folder)
        keep_files, remove_files = self.categorise_excel(self.folder_path, ["SAMPLE"], "Data Table")
        ost.move_files(self.folder_path, new_folder, remove_files, remove=True)
        return
