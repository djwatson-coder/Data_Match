
import os
import pandas as pd
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

    def triage_data(self):
        return

    def create_table(self):

        # get the excels
        files = self.get_files()

        # read them in
        data_tables = []
        for idx, file in enumerate(files):
            print(f"{idx + 1}. Reading File {file}...")
            table = self.read_file(file)
            table = table.assign(File=file)
            # print(table.head(10))
            # print(table.columns)
            data_tables.append(table)
            # print(f"{idx + 1}. {file}: added, length:{len(table)}")

        # create the table
        final_table = pd.concat(data_tables, ignore_index=True)
        final_table = self.clean_table(final_table)
        summary_table = self.summarise_table(final_table, key="File", group="Net_Amount")

        return final_table, summary_table


    def clean_table(self, df):
        df = self.correct_columns(df, self.keep_cols)
        df = self.format_columns(df)
        df = self.general_clean(df)

        return df

    def correct_columns(self, df, cols: dict):

        df = df.rename(columns={cols['File']: 'File',
                                cols['Policy']: 'Policy',
                                cols['Effective_Date']: 'Effective_Date',
                                cols['Company']: 'Company',
                                cols['Gross_Amount']: 'Gross_Amount',
                                cols['Net_Amount']: 'Net_Amount'})

        if "Commission_Amount" in cols.keys():
            df = df.rename(columns={cols['Commission_Amount']: 'Commission_Amount'})

        df = df[list(cols.keys())]

        return df

    def format_columns(self, df):
        return df

    def general_clean(self, df):

        # Policy Column
        df = df.dropna(subset=['Policy'])
        df["Policy"] = df["Policy"].astype('str')
        df["Policy"] = df["Policy"].str.replace('-', '')
        df["Policy"] = df["Policy"].str.strip()
        df["Policy"] = df["Policy"].str.replace(' ', '')
        df["Policy"] = df["Policy"].str.replace('/', '')
        df["Policy"] = df["Policy"].str.upper()

        # Amount Columns
        df = self.numify(df, "Net_Amount")
        df = self.numify(df, "Gross_Amount")
        if "Commission_Amount" in df.columns:
            df = self.numify(df, "Commission_Amount")
        else:
            df['Commission_Amount'] = df['Gross_Amount'] - df['Net_Amount']

        # Date Columns
        df = self.dateify(df, "Effective_Date")

        return df

    def summarise_table(self, df, key, group):

        df[group] = df[group].fillna(0)
        df = df.groupby([key]).agg(Net_Amount=(group, 'sum')).reset_index()

        # Used if there is an amount in the name of the file which shows the total
        df['Name_Amount'] = df[key].str.extract(r'([\d|,]*\.[\d]{2})', expand=True)
        df['Name_Amount'] = df['Name_Amount'].str.replace(r'\$', '')
        df['Name_Amount'] = df['Name_Amount'].str.replace(r',', '')
        df['Name_Amount'] = df['Name_Amount'].astype(float)
        df['Name_Amount_Check'] = df[group] - df['Name_Amount']

        return df

    @staticmethod
    def dateify(df, col_name):
        # Remove the time (00:00:00)
        df[col_name] = df[col_name].astype('str')
        df[col_name] = df[col_name].str.replace(r'[\d]{2}:[\d]{2}:[\d]{2}', '')
        # Find the type of date format
        # Reformat to YYYY-MM
        for i, row in df.iterrows():
            val = row[col_name]
            if len(val.split("/")) == 3:  # Checking if a 01/01/2021 type
                date_list = val.split("/")
                date = f"{str(int(date_list[2]))}-{str(int(date_list[0]))}"
            elif len(val.split("-")) == 3:  # Checking if a 2021-01-01 type
                date_list = val.split("-")
                date = f"{str(int(date_list[0]))}-{str(int(date_list[1]))}"
            else:
                val = val.removesuffix('.0')
                if len(val) > 6 and val.isdigit():  # Checking if a 01012020 type
                    year = val[-4:]
                    month = val[-6:-4]
                    date = f"{year}-{str(int(month))}"
                else:
                    date = val
            df.at[i, col_name] = date

        return df

    @staticmethod
    def numify(df, col_name):

        df[col_name] = df[col_name].astype('str')
        df[col_name] = df[col_name].str.replace('$', '')
        df[col_name] = df[col_name].str.replace(',', '')
        df[col_name] = df[col_name].str.replace('(', '-')
        df[col_name] = df[col_name].str.replace(')', '')
        df[col_name] = df[col_name].str.replace('s', '5')
        df[col_name] = df[col_name].str.replace('o', '0')
        df[col_name] = df[col_name].str.replace('O', '0')
        df[col_name] = df[col_name].astype('float')
        df[col_name] = df[col_name].fillna(0)

        return df

