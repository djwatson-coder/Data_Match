from readers.pdfreader import PDFReader


class BflPayPdfReader(PDFReader):

    def __init__(self, folder_path, client_name):
        self.ocr = False
        super(BflPayPdfReader, self).__init__(self.ocr)
        self.start_page = 0
        self.cols = ["Client Name", "Policy Number",
                     "Line Type / Coverage", "Effective Date", "Due Date", " Gross Due", "Commission Amount",
                     "Net Due"]
        self.keep_cols = {"Policy": "Policy #",
                          "Company": "Client Name",
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
