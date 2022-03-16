
import pdfplumber
import re
import pandas as pd
import os


class PDFReader:
    def __init__(self, folder_path, client_name):
        self.start_page = 0
        self.cols = []
        self.folder_path = folder_path
        self.read_ocr = False
        self.client_name = client_name

    def create_table(self, write_table: bool):

        pdfs = self.get_files()
        data_tables = []
        for pdf in pdfs:
            data_tables.append(self.read_pdf(pdf))

        df = pd.concat(data_tables, ignore_index=True)
        self.write_table(df)

        return df

    def write_table(self, df):
        df.to_excel(f"{self.folder_path}/{self.client_name}_Payments.xlsx")

    def get_files(self):

        pdfs = []
        for file in os.listdir(self.folder_path):
            if not self.read_ocr and (file.endswith('.pdf') or file.endswith('.PDF')):
                pdfs.append(file)
            elif self.read_ocr and (file.endswith('_OCR.pdf') or file.endswith('_OCR.PDF')):
                pdfs.append(file)
        return pdfs

    def read_pdf(self, pdf_path):
        company_name = []
        info_lines = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages[self.start_page:]):
                page_data = page.extract_text().split("\n")
                start = False
                for line in page_data:
                    line = self.specific_line_replacements(line)
                    line_data = line.split(" ")
                    line_data = self.post_line_split_edits(line_data)

                    if self.end_table_conditions(line_data):
                        start = False

                    if start:
                        if self.add_table_conditions(line_data):
                            line_data = self.pre_table_adjustments(line_data)
                            info_lines.append(line_data)

                        elif self.add_to_company_table(line_data):
                            company_name.append(line_data)

                    if self.start_table_conditions(line_data):
                        start = True

        info_lines = self.join_company_data(info_lines, company_name)

        new_df = pd.DataFrame(info_lines, columns=self.cols)

        return new_df

    @staticmethod
    def find_string(alist, pattern):
        string_match = re.compile(pattern)
        for idx, item in enumerate(alist):
            if string_match.search(item):
                return idx
        return

    @staticmethod
    def find_date(alist):
        date_match = re.compile("\d{1,2}\/\d{1,2}\/\d{4}")
        for idx, item in enumerate(alist):
            if date_match.search(item):
                return idx
        return

    def replace_decimal_spaces(self, line):
        regex_replace = ["  .  ","  . ","  ."," .  ",".  "," . "," .",". "]
        for i in regex_replace:
            line = line.replace(i, ".")
        return line

    def post_line_split_edits(self, line_data):
        return line_data

    def specific_line_replacements(self, line):
        return line

    @staticmethod
    def add_table_conditions(line_data):
        return False

    @staticmethod
    def add_to_company_table(line_data):
        return False

    @staticmethod
    def start_table_conditions(line_data):
        return False

    @staticmethod
    def end_table_conditions(line_data):
        return False

    @staticmethod
    def pre_table_adjustments(line_data):
        return False

    @staticmethod
    def join_company_data(info_lines, company_name):
        return info_lines
