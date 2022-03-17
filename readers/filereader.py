
import os
import pandas as pd
import settings


class FileReader:
    def __init__(self, folder_path: str, client_name: str):
        self.client_name = client_name
        self.folder_path = folder_path
        self.path_extensions = []
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
            data_tables.append(self.read_file(file))
            print(f"{file}: added")

        # create the table
        final_table = pd.concat(data_tables, ignore_index=True)


        if settings.WRITE_TABLE:
            self.write_table(final_table)

        return final_table

    def write_table(self, df):
        df.to_excel(f"{self.folder_path}/Generated/{self.client_name}_Combined.xlsx")
