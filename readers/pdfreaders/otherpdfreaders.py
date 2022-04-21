from readers.pdfreader import PDFReader
import re

class VicPDFReader(PDFReader):
    def __init__(self, folder_path, client_name):
        super(VicPDFReader, self).__init__()
        self.cols = ["Document Date", "Policy No", "Company", "Effective Date", "Expiration Date",
                     "Program-Pool","Prov","Gross", "Type", "Vendor", "Pay To", "Amount", "Commission",
                     "Office", "Comm PCT", "TXN Code"]

    def specific_line_replacements(self, line):
        line = line.replace(" 00", ".00")
        line = line.replace(" BR", "BR")

        return line

    def post_line_split_edits(self, line_data):
        line_data = list(filter(lambda a: a != '', line_data))
        line_data = list(filter(lambda a: a != '0', line_data))
        line_data = list(filter(lambda a: a != 'O', line_data))

        return line_data

    @staticmethod
    def start_table_conditions(line_data):
        return len(line_data) != 1 and line_data[0].lower() == "date" and line_data[1].lower() == "policy"

    @staticmethod
    def add_table_conditions(line_data):
        return len(line_data) > 10

    def pre_table_adjustments(self, line_data):
        date_2 = self.find_date(line_data[1:]) + 1
        company_name = "-".join(line_data[2:date_2])
        line_data[2:date_2] = [company_name]

        prov = self.find_string(line_data[5:], pattern="(ON|AB|BC|QC|SK)") + 5
        other_info = "-".join(line_data[5:prov])
        line_data[5:prov] = [other_info]

        return line_data


class MarPDFReader(PDFReader):
    def __init__(self, folder_path, client_name):
        super(MarPDFReader, self).__init__()
        self.start_page = 0
        self.cols = ['Invoice Number', 'Invoice Date', 'Description', 'Net Amount']
        self.folder_path = folder_path
        self.read_ocr = True
        self.client_name = client_name

    @staticmethod
    def specific_line_replacements(line):
        line = line.replace(" .", ".")
        line = line.replace(" 00", ".00")
        return line

    @staticmethod
    def end_table_conditions(line_data):
        return len(line_data) == 0 or len(line_data[0]) < 8

    @staticmethod
    def add_table_conditions(line_data):
        return len(line_data) >= 4

    @staticmethod
    def pre_table_adjustments(line_data):
        desc = "-".join(line_data[2:-1])
        line_data[2:-1] = [desc]
        return line_data

    @staticmethod
    def start_table_conditions(line_data):
        return len(line_data) != 0 and line_data[0].lower() in ["numero", "numfero", "num£ro"]
