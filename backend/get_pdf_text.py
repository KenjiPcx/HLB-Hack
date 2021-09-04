"""
references:
https://pdfminersix.readthedocs.io/en/latest/tutorial/composable.html
https://github.com/MatePocs/lovecraft/blob/master/data_func.py
https://towardsdatascience.com/pdf-text-extraction-in-python-5b6ab9e92dd
"""
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def get_raw_text(file_path):
    """Return text in pdf file as a string."""
    output_string = StringIO()
    with open(file_path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


def preprocess_pdf_str(text):
    """Parse string by '\n\n', remove '\n' characters and remove any line which has less than 6 words."""
    lines = [l.strip() for l in text.split("\n\n") if l.strip()]
    lines = [l.replace("\n", "") for l in lines]
    cleaned_text = [l for l in lines if len(l.split()) > 5]
    return "\n\n".join(cleaned_text)


def write_to_txt(text, txt_file_path):
    """Write text to specified txt file, with all non-ascii characters removed."""
    text = text.encode("ascii", "ignore").decode()  # remove unicode characters
    with open(txt_file_path, "wb") as f:
        f.write(text)


def get_pdf_text(pdf_path):
    """Return text in pdf as a string, with non-paragraphs removed."""
    text = get_raw_text(pdf_path)
    cleaned_text = preprocess_pdf_str(text)
    return cleaned_text
