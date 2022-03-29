from readers.pdfreader import PDFReader
import re


class LauPDFReader(PDFReader):
    def __init__(self, folder_path, client_name):
        self.ocr = True
        super(LauPDFReader, self).__init__(self.ocr)
        self.cols = ['Policy_Number', 'Info_1', 'Info_2', 'Info_3', "Date DE", "Date MISE", "Date",
                     "Info_4", "Info_5", "Info_6", "Prime", "Comm%", "COMM$", "Amount Paid", "Date Due", "Company"]
        self.keep_cols = {"Policy": "Policy_Number",
                          "Company": "Company",
                          "File": "File",
                          "Amount": "Amount Paid"}
        self.start_page = 1
        self.folder_path = folder_path
        self.client_name = client_name


    @staticmethod
    def add_table_conditions(line_data):
        policy_pattern = re.compile("LAR-|2014-|SS-|SOV-|LAR0|SOU-|DAS-|CRE-")
        return len(line_data) != 0 and policy_pattern.search(line_data[0])

    @staticmethod
    def add_to_company_table(line_data):
        return len(line_data) != 0 and line_data[0] not in ["***", "******"]

    @staticmethod
    def start_table_conditions(line_data):
        return len(line_data) != 0 and line_data[0].lower() == "sd"

    @staticmethod
    def pre_table_adjustments(line_data):
        if len(line_data[5]) < 8:
            del line_data[5]
        if len(line_data[14]) < 8:
            del line_data[14]
        return line_data

    @staticmethod
    def join_company_data(info_lines, company_name):

        for idx, company in enumerate(company_name):
            company_info = '-'.join(str(company) for company in company)
            info_lines[idx].append(company_info)

        return info_lines

    def specific_line_replacements(self, line):

        line = self.replace_decimal_spaces(line)

        line = re.sub(r'(\d\d\.\d\d)\.(\d\d\.\d\d)', r'\1 \2', line)
        line = re.sub(r'(\d\d\.\d\d)\.(\d\d\d\.\d\d)', r'\1 \2', line)
        line = re.sub(r'(\d\d\d\d)\.([A-z])', r'\1 \2', line)
        line = line.replace("E.V  001", "E.V-001")
        # line = re.sub(r'(DAS-\d\d\d) (\d)', r'\1\2', line)
        line = line.replace("DAS- ", "DAS-")
        line = line.replace("DAS -", "DAS-")
        line = line.replace("SOU- ", "SOU-")
        line = line.replace("LAR- ", "LAR-")
        line = line.replace("LAR_-", "LAR-")
        line = line.replace("LAR-13 ", "LAR-13")
        line = line.replace("DAS-03 ", "DAS-03")
        line = line.replace("DAS-038 ", "DAS-038")
        line = line.replace("DAS-04 ", "DAS-04")
        line = line.replace("LAR-4 ", "LAR-4")
        line = line.replace("DAS-044 7", "DAS-0447")

        return line

    def post_line_split_edits(self, line_data):

        line_data = list(filter(lambda a: a != "", line_data))
        line_data = list(filter(lambda a: a != "0", line_data))
        line_data = list(filter(lambda a: a != ",", line_data))
        line_data = list(filter(lambda a: a != "-", line_data))
        line_data = list(filter(lambda a: a != '"', line_data))

        return line_data

    def format_columns(self, df):
        df['pos_neg'] = df['Amount'].str.extract("(-)").fillna("")
        df['Amount'] = df['Amount'].replace('(-)', '', regex=True, inplace=True)
        df['Amount'] = df['Amount'].replace('(D|O|G|o)', '0', regex=True, inplace=True)
        df['Amount'] = df['Amount'].replace('(S)', '5', regex=True, inplace=True)
        df['Amount'] = df['Amount'].replace(',', '.', regex=True, inplace=True) # make sure this is correct
        df["Amount"] = df['pos_neg'] + df["Amount"]

        df["Amount"] = df['Amount'].astype('float')

        df = df.drop('pos_neg', axis=1)

        return df


class AgPDFReader(PDFReader):

    def __init__(self, folder_path, client_name):
        self.ocr = False
        super(AgPDFReader, self).__init__(self.ocr)
        self.start_page = 0
        self.cols = ["Insured", "Producer #", "Carrier Doc Page #", "Carrier Doc Date", "Policy #",
                     "Line Type / Coverage", "Effective Date", "Due Date", " Gross Due", "Commission Amount",
                     "Current/Past Due", "Net Due"]
        self.cols = ["Insured", "Carrier Doc Date", "Policy #",
                     "Line Type / Coverage", "Effective Date", "Due Date", " Gross Due", "Commission Amount",
                     "Net Due"]
        self.keep_cols = {"Policy": "Policy #",
                          "Company": "Insured",
                          "File": "File",
                          "Amount": "Net Due"}
        self.folder_path = folder_path
        self.client_name = client_name

    def post_line_split_edits(self, line_data):
        line_data = list(filter(lambda a: a != '', line_data))
        return line_data

    @staticmethod
    def add_table_conditions(line_data):
        return len(line_data) > 5

    def pre_table_adjustments(self, line_data: list):
        prod = self.find_date(line_data)
        company_name = "-".join(line_data[0:prod])
        line_data[0:prod] = [company_name]
        line_data = [x for x in line_data if x not in ("P", "C", "B", "1", "2", "3")]  # B and 1-3 are an issue
        # ToDo Join B, 1-3 back to the Policy number before
        if len(line_data) == 8:
            line_data.insert(4, "01/01/2010")  # This is an issue
        # line_data.append(page_num + 1)
        return line_data

    @staticmethod
    def start_table_conditions(line_data):
        return len(line_data) > 0 and line_data[0].lower() == "page"



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
