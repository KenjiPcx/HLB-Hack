from flask import Flask, request, jsonify
import requests
import classifier
import classifier_enhanced
from flask_cors import CORS

from io import StringIO
import os
from werkzeug.utils import secure_filename

from get_pdf_text import get_pdf_text
from bs4 import BeautifulSoup

import json
import numpy as np
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)

uploads_dir = os.path.join(os.path.abspath(os.getcwd()), 'uploads')

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

    pdfText = get_pdf_text("./uploads/t2.pdf")
    res = classifier.main(pdfText, 5)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(pdfText)
    return jsonify(res)

@app.route('/text', methods=['POST']) 
def text():
    name = request.form.get("companyName")
    text = request.form.get("text")
    
    res = classifier.main(text, 5)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(text)
    return jsonify(res)

@app.route('/url', methods=['POST']) 
def url():
    name = request.form.get("companyName")
    url = request.form.get("url")
    pdfText = get_site_text(url)
    
    res = classifier.main(pdfText, 5)
    res["companyName"] = name
    res["data"] = classifier_enhanced.main(pdfText)
    return jsonify(res)

if __name__ == "__main__":
    input_data = get_pdf_text("./uploads/CYHI_2021_-_Kickoff_Briefing.pdf")
    print(input_data)
    classifier_enhanced.main(input_data)