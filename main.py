import sys
import settings
from utils import toolselector
import readers


def main(client: str):
    # Select the formatting functions for the given client
    attributes = {}
    for client_info in settings.CLIENT_INFORMATION:
        if client_info["clientId"] == client:
            attributes = client_info["attributes"]
            break

    payments_reader = getattr(readers.speacialpdfreader, attributes["paymentsReader"])
    payments_reader = payments_reader(folder_path=attributes["folderPath"], client_name=client)

    # bordereau_reader = getattr(readers.speacialpdfreader, attributes["paymentsReader"])
    # bordereau_reader.__init__(folder_path=attributes["folderPath"], client_name=client)

    # data_cleaner = select_payments_reader(attributes["redReader"])
    # data_cleaner.__init__(folder_path=attributes["folderPath"], client_name=client)

    payments_reader.create_table()
    # bordereau_reader.create_table()
    # data_cleaner.create_report()


if __name__ == '__main__':

    try:
        main(sys.argv[1])
    except IndexError:
        main(settings.EXAMPLE_NAME)



# ToDo create a command line executable file
# ToDo create a make command to run the script
# ToDo add OCR to the PDFReader init varaibles