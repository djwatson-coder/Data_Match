from readers.pdfreader import PDFReader
import re


class MarshPDFReader(PDFReader):
    def __init__(self, folder_path, client_name):
        super(MarshPDFReader, self).__init__()
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



