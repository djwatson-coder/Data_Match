
import os
import pandas as pd
import settings


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
            if file.split(".")[-1].lower() in self.path_extensions:
                files.append(file)
        return files

    def create_table(self):

        # get the excels
        files = self.get_files()

        # read them in
        data_tables = []
        for file in files:
            table = self.read_file(file)
            table["File"] = file
            data_tables.append(table)
            print(f"{file}: added")

        # create the table
        final_table = pd.concat(data_tables, ignore_index=True)

        final_table = self.clean_table(final_table)

        if settings.WRITE_TABLE:
            self.write_table(final_table)

        return final_table

    def write_table(self, df):
        df.to_excel(f"{self.folder_path}/Generated/{self.client_name}_Combined.xlsx")

    def clean_table(self, df):
        df = self.correct_columns(df, self.keep_cols)
        df = self.format_columns(df)

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
