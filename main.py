import sys
import settings
from utils import toolselector as ts
import os
import pandas as pd
from datamanip import datamatch as dm


def main(client: str):

    # Get the attributes of the client
    attributes = ts.get_attributes(client, settings.CLIENT_INFORMATION)

    # # Read in the Payment Data
    # df_pay = read_in_data(client,
    #                       attributes["paymentsReaders"],
    #                       attributes["folderPath"] + settings.PAYMENTS_EXTENSION)
    #
    # # Read in the Bordereau Data
    # df_bord = read_in_data(client,
    #                        attributes["bordReaders"],
    #                        attributes["folderPath"] + settings.BORDEREAU_EXTENSION)
    #
    # # Save the datasets
    # write_table(df_pay, attributes["folderPath"], "Payments", client)
    # write_table(df_bord, attributes["folderPath"], "Bordereau", client)

    # Match the Paymnets and Bordereau Data
    df_pay = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Payments.xlsx")
    df_bord = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Bordereau.xlsx")

    data_match = dm.DataMatcher()
    data_match.create_match_report(df_pay, df_bord)

    return


def read_in_data(client: str, readers: list, file_paths: str):
    dfs = []
    for reader in readers:
        rdr = ts.select_reader(reader)(file_paths, client)
        dfs.append(rdr.create_table())
    return pd.concat(dfs, ignore_index=True)


def write_table(df, save_path: str, read_type: str, client_name: str):

    path = f"{save_path}/Generated"
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_excel(f"{path}/{client_name}_{read_type}.xlsx", index=False)

    print(f"{read_type} Table Written-----")



if __name__ == '__main__':

    # try:
    #     main(sys.argv[1])
    # except IndexError:
    #     main(settings.EXAMPLE_NAME)
    main(settings.EXAMPLE_NAME)

# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo Create a debug and testing files for each important function