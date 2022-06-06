
import pandas as pd
import os
import shutil
from utils import toolselector as ts
from pathlib import Path
import win32com.client
from openpyxl import load_workbook


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
        rdr.triage_data()  # put in the exculsion folder
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
            # print(f_path)
        elif f_path != targ:
            print(f"Reading Folder:{f_path}")
            file_list = file_list + collate_files(f_path, targ)
    return file_list


def create_directory(directory, remove=False):
    """ Creates a directory if one does not exist"""
    if remove and os.path.exists(directory):
        shutil.rmtree(directory)
    Path(directory).mkdir(parents=True, exist_ok=True)
    # print(len(os.listdir(directory)))


def move_files(path, destination, files, remove=False):
    """ moves or copies files to a destination path"""
    for file in files:
        if os.path.isfile(f"{destination}/{file}"):
            os.remove(f"{destination}/{file}")
        if remove:
            shutil.move(os.path.join(path, file), destination)
        else:
            shutil.copy(os.path.join(path, file), destination)


def excel_of_files(path, destination):
    all_files = []
    for filename in os.listdir(path):
        if os.path.isfile(f"{path}/{filename}"):
            all_files.append([filename])

    final_table = pd.DataFrame(all_files, columns=["Filename"])
    final_table.to_excel(f"{destination}/all_files.xlsx")

def excel_of_filepaths(path, destination):
    """ Takes a folder and lists all the files in the sub folders with the sub folder as a column """
    all_files = []
    for folder in os.listdir(path):
        sub_folder = f"{path}/{folder}"
        for filename in os.listdir(sub_folder):
            all_files.append([sub_folder.split("/")[-1], filename, ""])

    final_table = pd.DataFrame(all_files, columns=["SubFolder", "FileName", "Include?"])
    final_table.to_excel(f"{destination}/Checking Files.xlsx", index=False, sheet_name="Checking_Files")


def decrypt_excel_files(path):

    excel = win32com.client.Dispatch('Excel.Application')

    for excel_file in os.listdir(path):

        excel_file_path = f"{path}/{excel_file}"
        path = r'%s' % excel_file_path
        # workbook = excel.Workbooks.open(excel_file_path)
        # path_ext = excel_file_path.split(".xlsx")
        # new_excel_file_path = path_ext[0] + " - BT EDITED" + ".xlsx"
        # print(f"Decrypted: {new_excel_file_path}")
        # workbook.SaveAs(new_excel_file_path)
        wb = load_workbook(path)
        wb.security


def rename_annoying_files(directory, targ, ext_name=""):
    """ Moves and renames annoying files so I don't have to do it manually"""
    for thing in os.listdir(directory):
        path = f"{directory}/{thing}"
        if [x for x in os.listdir(path) if os.path.isfile(f"{path}/{x}")]:  # if there is a file in the folder
            name_discrim_files(path, targ, f"{ext_name}-{thing}")
        else:
            rename_annoying_files(path, targ, f"{ext_name}-{thing}")


def name_discrim_files(path, target, extension_name):
    # If there is 1 file - take it
    files = [x for x in os.listdir(path) if os.path.isfile(f"{path}/{x}")]
    taken = ""
    duplicate = ""
    if len(files) == 1:
        taken = files[0]
    elif len(files) == 2 and files[0][:10] == files[1][:10]:
        taken = max(files, key=len)
        duplicate = min(files, key=len)

    if taken:
        rename_and_copy_xl(taken, path, target, extension_name)
        # print(f"Keep File: {taken}")
    else:
        global COUNT
        print(f"{COUNT}."
              f"{path.replace('C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Marsh/Raw Data -2/Bordereau/', '')}")
        COUNT += 1
        global CHECK_LIST
        CHECK_LIST.append(path.replace('C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Marsh/Raw Data -2/Bordereau/', ''))
        # move_folder(path, target + "/check",)
    if duplicate:
        rename_and_copy_xl(duplicate, path, target + "/dp", extension_name)
        # print(f"duplicate File: {taken}")

        return


def rename_and_copy_xl(file, path, target, extension_name):
    f_path = f"{path}/{file}"
    shutil.copy(f_path, target)
    old_file = os.path.join(target, file)
    if ".csv" in file:
        old_split = file.split(".csv")
        new_file_name = f"{old_split[0]}{extension_name}.csv"
    else:
        old_split = file.split(".xl")
        new_file_name = f"{old_split[0]}{extension_name}.xl{old_split[1]}"
    new_file = os.path.join(target, new_file_name)
    os.rename(old_file, new_file)


COUNT = 0
CHECK_LIST = []


def move_folder(original_path, new_path):
    shutil.copy(original_path, new_path)
