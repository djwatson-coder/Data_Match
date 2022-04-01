
from readers import speacialpdfreader, specialexcelreader


def select_reader(reader_type: str):
    if "PDFReader" in reader_type:
        return getattr(speacialpdfreader, reader_type)
    elif "ExcelReader" in reader_type:
        return getattr(specialexcelreader, reader_type)

    return None


def get_attributes(client: str, information: dict):
    for client_info in information:
        if client_info["clientId"] == client:
            return client_info["attributes"]

    return None

