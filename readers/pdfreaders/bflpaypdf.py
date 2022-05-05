from readers.pdfreader import PDFReader


class BflPayPdfReader(PDFReader):

    def __init__(self, folder_path, client_name):
        self.ocr = False
        super(BflPayPdfReader, self).__init__(self.ocr)
        self.start_page = 0
        self.cols = ["Client Name", "Policy Number", "Pol Type Code", "Item Number", "Effective Date",
                     "Trans Code", "Trans Amt", "Com", "Com Amt", "Rec Bal", "Payment"]
        self.keep_cols = {"Policy": "Policy Number",
                          "Company": "Client Name",
                          "File": "File",
                          "Amount": "Payment"}
        self.folder_path = folder_path
        self.client_name = client_name

    def post_line_split_edits(self, line_data):
        line_data = list(filter(lambda a: a != '', line_data))
        return line_data

    @staticmethod
    def add_table_conditions(line_data):
        return len(line_data) > 5

    def pre_table_adjustments(self, line_data: list):
        pol = self.find_strings(line_data, ["BFL", "BLF", "BLC", "BSP", "BCAL", "CBFL",
                                            "P210", "PBEC", "B18", "B190", "B20", "BCS0", "CGY",
                                            "BUS", "E420", "DAS"])
        company_name = "-".join(line_data[0:pol])
        line_data[0:pol] = [company_name]

        p_type = self.find_strings(line_data, ["STPK", "RECP", "RRSU", "CLLE", "CLMP",
                                               "STOP", "AEPK", "REPM", "CLPR"]) + 1
        pol_type = "-".join(line_data[2:p_type])
        line_data[2:p_type] = [pol_type]

        line_data = list(filter(lambda a: a != '', line_data))

        return line_data

    @staticmethod
    def start_table_conditions(line_data):
        return len(line_data) > 0 and line_data[0].lower() == "client"

    @staticmethod
    def end_table_conditions(line_data):
        return len(line_data) < 10

    @staticmethod
    def skip_condition(line_data):
        return len(line_data) < 10
