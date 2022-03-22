import sys
import settings
from readers import speacialpdfreader, excelreader
from utils import toolselector as ts


def main(client: str):

    attributes = ts.get_attributes(client, settings.CLIENT_INFORMATION)

    pay_reader = ts.select_reader(attributes["paymentsReader"])(attributes["folderPath"] + settings.PAYMENTS_EXTENSION,
                                                                client)
    bord_reader = ts.select_reader(attributes["bordReader"])(attributes["folderPath"] + settings.BORDEREAU_EXTENSION,
                                                             client)

    df_pay = pay_reader.create_table()
    df_bord = bord_reader.create_table()

    # data_match = select_payments_reader(attributes["redReader"])
    # data_cleaner.__init__(folder_path=attributes["folderPath"], client_name=client)

    # data_cleaner.create_report()


if __name__ == '__main__':

    try:
        main(sys.argv[1])
    except IndexError:
        main(settings.EXAMPLE_NAME)

# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo add OCR to the PDFReader init variables
# ToDo make a readers class that excel and pdf inherent from
