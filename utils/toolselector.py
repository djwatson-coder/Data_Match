
from readers import speacialpdfreader, specialexcelreader
from datamanip import datamatch
import pandas as pd
import os
import shutil


def select_reader(reader_type: str):
    if "PDFReader" in reader_type:
        return getattr(speacialpdfreader, reader_type)
    elif "ExcelReader" in reader_type:
        return getattr(specialexcelreader, reader_type)

    return None

def select_matcher(client: str):
    return datamatch.DataMatcher(client)

def get_attributes(client: str, information: dict):
    for client_info in information:
        if client_info["clientId"] == client:
            return client_info["attributes"]

    return None


def read_in_data(client: str, readers: list, file_paths: str):
    dfs = []
    sums = []
    for reader in readers:
        rdr = select_reader(reader)(file_paths, client)
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


def find_all_files(dir, targ):
    file_list = []
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f):
            print(filename)
            shutil.copy(f, targ)

            if filename.endswith("xlsx"):
                xl = pd.ExcelFile(f"{dir}/{filename}")
                file_list.append(f"{filename}: {xl.sheet_names}")

        else:
            file_list = file_list + find_all_files(f, targ)
    return file_list
