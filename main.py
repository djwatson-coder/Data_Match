import sys
import settings
from utils import toolselector as ts
from matching import datamatch as dm


def main(client: str):

    attributes = ts.get_attributes(client, settings.CLIENT_INFORMATION)

    pay_reader = ts.select_reader(attributes["paymentsReader"])(attributes["folderPath"] + settings.PAYMENTS_EXTENSION,
                                                                client)
    bord_reader = ts.select_reader(attributes["bordReader"])(attributes["folderPath"] + settings.BORDEREAU_EXTENSION,
                                                             client)

    #df_pay = pay_reader.create_table(save_path=attributes["folderPath"], read_type="Payment")
    df_bord = bord_reader.create_table(save_path=attributes["folderPath"], read_type="Bordereau")

    #data_match = dm.DataMatcher()
    #data_match.create_match_report(df_pay, df_bord)

    return


if __name__ == '__main__':

    # try:
    #     main(sys.argv[1])
    # except IndexError:
    #     main(settings.EXAMPLE_NAME)
    main(settings.EXAMPLE_NAME)

# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo add OCR to the PDFReader init variables
# ToDo make a readers class that excel and pdf inherent from
# ToDo Create a debug and testing files for each important function
