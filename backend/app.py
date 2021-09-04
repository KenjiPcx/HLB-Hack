from flask import Flask, request, jsonify
import requests
import classifier
import classifier_enhanced
from flask_cors import CORS

from io import StringIO
import os
from werkzeug.utils import secure_filename

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import pdfminer
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

uploads_dir = os.path.join(os.path.abspath(os.getcwd()), 'uploads')
print(uploads_dir)

def get_raw_text(file_path):
    """ Return text in pdf file as a string.
    """
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return(output_string.getvalue())

def preprocess_pdf_str(text):
    """ Parse string by '\n\n', remove '\n' characters and remove any line which has less than 6 words.
    """
    lines = [l.strip() for l in text.split('\n\n') if l.strip()]
    lines = [l.replace('\n', '') for l in lines]
    cleaned_text = [l for l in lines if len(l.split()) > 5]
    return '\n'.join(cleaned_text)

def write_to_txt(text, txt_file_path):
    """ Write text to specified txt file, with all non-ascii characters removed.
    """
    text = text.encode('ascii', 'ignore').decode() # remove unicode characters
    with open(txt_file_path, 'wb') as f:
        f.write(text)

def get_pdf_text(pdf_path):
    """ Return text in pdf as a string, with non-paragraphs removed.
    """
    text = get_raw_text(pdf_path)
    cleaned_text = preprocess_pdf_str(text)
    return cleaned_text

def get_site_text(site_url):
    """ Return all paragraph text from a website.
    """
    page = requests.get(site_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text_lst = soup.find_all('p')
    text = '\n'.join([p.get_text().replace('\n', ' ') for p in text_lst])
    return text

@app.route('/pdf', methods=['POST']) 
def pdf():
    name = request.form.get("companyName")
    pdfText = ""
    for i in range(len(request.files)):
        file = request.files.get(f"file{i}")
        file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
        dir = f"./uploads/{secure_filename(file.filename)}"
        dir = dir.replace(" ", "_")
        pdfText += get_pdf_text(dir) + "\n\n"

    print(pdfText)
    res = classifier.main(pdfText, 1)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(pdfText)
    return jsonify(res)

@app.route('/text', methods=['POST']) 
def text():
    name = request.form.get("companyName")
    text = request.form.get("text")
    
    res = classifier.main(text, 3)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(text)
    res["data"] = classifier_enhanced.main(text)
    return jsonify(res)

@app.route('/url', methods=['POST']) 
def url():
    name = request.form.get("companyName")
    url = request.form.get("url")
    pdfText = get_site_text(url)
    
    res = classifier.main(pdfText, 3)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(pdfText)
    return jsonify(res)