
from readers.pdfreader import PDFReader
from readers.laureaureader import LaureauPDFReader
from readers.agreader import AGPDFReader
from readers.victorreder import VictorPDFRedear



def reader_selector(dir):
    reader_type = dir_list = dir.split("/")[-3]
    if reader_type == "Lareau":
        return LaureauPDFReader(dir, reader_type)
    elif reader_type == "Encon Victor":
        return VictorPDFRedear(dir, reader_type)
    if reader_type == "Arthur Gallagher":
        return AGPDFReader(dir, reader_type)

    return None

def get_reader_context(dir):
    dir_list = dir.split("/")[-3]
