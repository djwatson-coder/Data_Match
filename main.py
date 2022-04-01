
import settings
from utils import toolselector as ts
import pandas as pd
from datamanip import datamatch as dm
import sys


def main(client: str, create=True):

    # Get the attributes of the client
    attributes = ts.get_attributes(client, settings.CLIENT_INFORMATION)

    if create:

        # Read in the Payment Data
        df_pay, df_pay_sum = ts.read_in_data(client,
                                             attributes["paymentsReaders"],
                                             attributes["folderPath"] + settings.PAYMENTS_EXTENSION)

        # Read in the Bordereau Data
        df_bord, df_bord_sum = ts.read_in_data(client,
                                               attributes["bordReaders"],
                                               attributes["folderPath"] + settings.BORDEREAU_EXTENSION)

        input_data = {
            "Bordereau Data": df_bord,
            "Bordereau Data Summary": df_bord_sum,
            "Payment Data": df_pay,
            "Payment Data Summary": df_pay_sum,
        }

        ts.write_report(input_data, attributes["folderPath"], "Input_Data", client)

    else:
        # Read in the Excels - to skip the need for the previous code when already generated
        df_pay = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx",
                               sheet_name="Payment Data")
        df_bord = pd.read_excel(attributes["folderPath"] + "/Generated/" + client + "_Input_Data.xlsx",
                                sheet_name="Bordereau Data")

    # Match the Payments and Bordereau Data
    data_match = dm.DataMatcher()
    summary_report = data_match.create_match_report(df_pay, df_bord)

    # Write the final report
    ts.write_report(summary_report, attributes["folderPath"], "Summary_Report", client)

    return


if __name__ == '__main__':
    main(sys.argv[1])

# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo Create a debug and testing files for each important function
# ToDo Refactor the write table and write report function to one
