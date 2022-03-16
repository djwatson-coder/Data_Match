
from readers.laureaureader import LaureauPDFReader
from readers.agreader import AGPDFReader
from readers.victorreder import VictorPDFReader
import settings

def reader_selector(directory: str):
    reader_type = directory.split("/")[-1]
    if reader_type == "Lareau":
        pdf_reader = LaureauPDFReader(directory, reader_type)
    elif reader_type == "Encon Victor":
        pdf_reader = VictorPDFReader(directory, reader_type)
    elif reader_type == "Arthur Gallagher":
        pdf_reader = AGPDFReader(directory, reader_type)
    else:
        return

    pdf_reader.create_table(settings.write_table)


