from readers.pdfreader import PDFReader


class AGPDFReader(PDFReader):

    def __init__(self, folder_path, client_name):
        super(AGPDFReader, self).__init__()
        self.start_page = 0
        self.cols = []

    def post_line_split_edits(self, line_data):
        line_data = list(filter(lambda a: a != '', line_data))
        return line_data

    @staticmethod
    def add_table_conditions(line_data):
        return len(line_data) > 5

    def pre_table_adjustments(self, line_data):
        prod = self.find_date(line_data)
        company_name = "-".join(line_data[0:prod])
        line_data[0:prod] = [company_name]
        # line_data.append(page_num + 1)
        return line_data

    @staticmethod
    def start_table_conditions(line_data):
        return line_data[0].lower() == "page"
