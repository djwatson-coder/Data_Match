
import settings
from utils import toolselector as ts
import os
import pandas as pd
from datamanip import datamatch as dm
import sys


def main(client: str):

    # Get the attributes of the client
    attributes = ts.get_attributes(client, settings.CLIENT_INFORMATION)

    # Read in the Payment Data
    df_pay, df_pay_sum = read_in_data(client,
                          attributes["paymentsReaders"],
                          attributes["folderPath"] + settings.PAYMENTS_EXTENSION)

    # Read in the Bordereau Data
    df_bord, df_bord_sum = read_in_data(client,
                           attributes["bordReaders"],
                           attributes["folderPath"] + settings.BORDEREAU_EXTENSION)

    input_data = {
        "Bordereau Data": df_bord,
        "Bordereau Data Summary": df_bord_sum,
        "Payment Data": df_pay,
        "Payment Data Summary": df_pay_sum,
    }

    write_report(input_data, attributes["folderPath"], "Input_Data", client)

    # Read in the Excels - to skip the need for the previus code when already generated
    df_pay = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx",
                           sheet_name="Payment Data")
    df_bord = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx",
                            sheet_name="Bordereau Data")

    # Match the Payments and Bordereau Data
    data_match = dm.DataMatcher()
    summary_report = data_match.create_match_report(df_pay, df_bord)

    # Write the final report
    write_report(summary_report, attributes["folderPath"], "Summary_Report", client)

    return


def read_in_data(client: str, readers: list, file_paths: str):
    dfs = []
    sums = []
    for reader in readers:
        rdr = ts.select_reader(reader)(file_paths, client)
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


if __name__ == '__main__':
    main(sys.argv[1])

# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo Create a debug and testing files for each important function
# ToDo Refactor the write table and write report function to one
