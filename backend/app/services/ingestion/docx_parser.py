
from docx import Document
def extract_docx_content(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    
    return{
        "text": text,
        "total_pages" : 1,
        "metadata":{
            "type":"docx"
        }
    }