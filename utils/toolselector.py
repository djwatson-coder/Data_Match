
from readers.pdfreaders import agpaypdf, laupaypdf, otherpdfreaders
from readers.excelreaders import agpayxl, agbordxl, aonpayxl, laubordxl, otherxlreaders
from datamanip import datamatch


def select_reader(reader_type: str):
    print(reader_type)
    if "PDFReader" in reader_type:
        return select_pdf_reader(reader_type)
    elif "ExcelReader" in reader_type:
        return select_excel_reader(reader_type)

    return None


def select_pdf_reader(reader_type: str):
    pdf_readers = {
        "AgPDFReader": agpaypdf,
        "LaPDfReader": laupaypdf,
        "other": otherpdfreaders
    }

    if reader_type in pdf_readers.keys():
        return getattr(pdf_readers[reader_type], reader_type)

    return None


def select_excel_reader(reader_type: str):
    excel_readers = {
        "AgPExcelReader": agpayxl,
        "AonPExcelReader": aonpayxl,
        "AgExcelReader": agbordxl,
    }

    if reader_type in excel_readers.keys():
        return getattr(excel_readers[reader_type], reader_type)

    return None


def select_matcher(client: str):
    return datamatch.DataMatcher(client)

