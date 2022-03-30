
import os
import pandas as pd
import settings
pd.options.mode.chained_assignment = None

class FileReader:
    def __init__(self):
        self.client_name = ""
        self.folder_path = ""
        self.path_extensions = []
        self.keep_cols = {}
        return

    def read_file(self, file):
        return

    def get_files(self):

        files = []
        for file in os.listdir(self.folder_path):
            if file.endswith(tuple(self.path_extensions)):
                files.append(file)
        return files

    def create_table(self, save_path: str, read_type: str):

        # get the excels
        files = self.get_files()

        # read them in
        data_tables = []
        for idx, file in enumerate(files):
            print(f"{idx+1}. Reading File {file}...")
            table = self.read_file(file)
            table = table.assign(File=file)
            data_tables.append(table)
            #print(f"{file}: added")

        # create the table
        final_table = pd.concat(data_tables, ignore_index=True)

        final_table = self.clean_table(final_table)

        if settings.WRITE_TABLE:
            self.write_table(final_table, save_path, read_type)

        return final_table

    def write_table(self, df, save_path, read_type):
        path = f"{save_path}/Generated"
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_excel(f"{path}/{self.client_name}_{read_type}.xlsx")

        print(f"{read_type} Table Written-----")

    def clean_table(self, df):
        df = self.correct_columns(df, self.keep_cols)
        df = self.format_columns(df)
        df = self.general_clean(df)

        return df

    def correct_columns(self, df, cols: dict):

        df.rename(columns={cols['Policy']: 'Policy',
                           cols['Company']: 'Company',
                           cols['File']: 'File',
                           cols['Amount']: 'Amount'},
                  inplace=True)

        df = df[["Policy", "Company", "File", "Amount"]]

        return df

    def format_columns(self, df):
        return df

    def general_clean(self, df):
        df["Amount"] = df["Amount"].astype('float')
        return df
