
import settings
from utils import toolselector as ts
from utils import ostools as ost
import pandas as pd
import sys


def main(client: str, create_data=True):

    # Get the attributes of the client
    client_info = ost.get_attributes(client, settings.CLIENT_INFORMATION)

    if create_data:

        # Read in the Payment Data
        print("CREATING PAYMENT DFs")
        df_pay, df_pay_sum = ost.read_in_data(client, client_info["paymentsReaders"],
                                              client_info["folderPath"] + settings.PAYMENTS_EXTENSION)
        # Read in the Bordereau Data
        print("CREATING BORDEREAU DFs")
        df_bord, df_bord_sum = ost.read_in_data(client, client_info["bordReaders"],
                                                client_info["folderPath"] + settings.BORDEREAU_EXTENSION)
        input_data = {
            "Bordereau Data": df_bord,
            "Bordereau Data Summary": df_bord_sum,
            "Payment Data": df_pay,
            "Payment Data Summary": df_pay_sum,
        }

        print("CREATING COLLATED INPUT DF")
        ost.write_report(input_data, client_info["folderPath"], "Input_Data", client)

    df_pay = pd.read_excel(client_info["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx", "Payment Data")
    df_bord = pd.read_excel(client_info["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx", "Bordereau Data")

    # Match the Payments and Bordereau Data
    data_match = ts.select_matcher(client)
    summary_report = data_match.create_match_report(df_pay, df_bord)

    # Write the final report
    ost.write_report(summary_report, client_info["folderPath"], "Summary_Report", client)

    return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1], True)
    else:
        # main("BFL", True)

        # ost.excel_of_files(path="C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Arthur Gallagher/Payments Raw",
        #                    destination="C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Arthur Gallagher")

        direct = "C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Marsh/Raw Data - Copy/Bordereau"
        targ = "C:/Users/david.watson/Documents/Clients/ARAG/01. Data/Marsh/Bordereau/Keep/New folder"
        annoying_name = "LegalExpenseBordereauReport.xlsx"
        ost.rename_annoying_files(direct, targ, annoying_name)



# ToDo Create a debug and testing files for each important function
