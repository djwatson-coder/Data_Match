
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
        for file in os.listdir(f"{self.folder_path}"):
            if file.endswith(tuple(self.path_extensions)):
                files.append(file)
        return files

    def create_table(self):

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
        summary_table = self.summarise_table(final_table, key="File", group="Amount")

        return final_table, summary_table


    def clean_table(self, df):
        df = self.correct_columns(df, self.keep_cols)
        df = self.format_columns(df)
        df = self.general_clean(df)

        return df

    def correct_columns(self, df, cols: dict):

        df = df.rename(columns={cols['Policy']: 'Policy',
                                cols['Company']: 'Company',
                                cols['File']: 'File',
                                cols['Amount']: 'Amount'})

        df = df[["Policy", "Company", "File", "Amount"]]

        return df

    def format_columns(self, df):
        return df

    def general_clean(self, df):

        # Policy Column
        df = df.dropna(subset=['Policy'])
        df["Policy"] = df["Policy"].astype('str')

        # Amount Column
        df["Amount"] = df["Amount"].astype('str')
        df["Amount"] = df["Amount"].str.replace('$', '')
        df["Amount"] = df["Amount"].str.replace(',', '')
        df["Amount"] = df["Amount"].str.replace('(', '-')
        df["Amount"] = df["Amount"].str.replace(')', '')
        df["Amount"] = df["Amount"].astype('float')

        return df

    def summarise_table(self, df, key, group):
        return df.groupby([key]).agg(Amount=(group, 'sum')).reset_index()
