
import pandas as pd
import os
import shutil
from utils import toolselector as ts
from pathlib import Path

def get_attributes(client: str, information: dict):
    for client_info in information:
        if client_info["clientId"] == client:
            return client_info["attributes"]

    return None


def read_in_data(client: str, readers: list, file_path: str):

    collated_file_path = file_path + "/Collated"
    create_directory(collated_file_path, remove=True)
    collate_files(file_path, collated_file_path)

    dfs = []
    sums = []
    for reader in readers:
        rdr = ts.select_reader(reader)(collated_file_path, client)
        df, summary = rdr.create_table()
        dfs.append(df)
        sums.append(summary)

    return pd.concat(dfs, ignore_index=True), pd.concat(sums, ignore_index=True)


def write_report(data: dict, save_path: str, report_type: str, client_name: str):
    path = f"{save_path}/Generated"
    if not os.path.exists(path):
        os.makedirs(path)
    with pd.ExcelWriter(f"{path}/{client_name}_{report_type}.xlsx") as writer:
        for name, df in data.items():
            df.to_excel(writer, sheet_name=name, index=False)

    print(f"{report_type} Table Written-----")


def collate_files(directory, targ):
    """ Recursively adds all files in a directory tree to a target directory"""
    file_list = []
    for filename in os.listdir(directory):
        # f = os.path.join(directory, filename)
        f_path = f"{directory}/{filename}"
        if os.path.isfile(f_path):
            shutil.copy(f_path, targ)
            file_list.append(filename)
        elif f_path != targ:
            print(f_path)
            file_list = file_list + collate_files(f_path, targ)
    return file_list


def create_directory(directory, remove=False):
    """ Creates a directory if one does not exist"""
    if remove and os.path.exists(directory):
        shutil.rmtree(directory)
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(len(os.listdir(directory)))

