# In parse/utils.py
from PyPDF2 import PdfReader

def convert_pdf_to_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
        print(text)
    return text
