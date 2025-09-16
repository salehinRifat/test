import PyPDF2
from fastapi import UploadFile

def extract_text(file: UploadFile) -> str:
    reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text
