import os
import fitz
import pdfplumber

def extract_pdf_content(file_path: str) -> dict:
    
    if not os.path.exists:
        raise FileNotFoundError(f"PDF file is not available:{file_path}")
    
    text_content = extract_text(file_path)
    tables = extract_tables(file_path)
    
    return{
        "text": text_content
    }
def extract_text(file_path: str) -> str:
    all_text = []
    with fitz.open(file_path) as pdf:
        for page_number, page in enumerate(pdf):
            
            page_text = page.get_text("text")
            
            if page_text.strip():
                all_text.append(f"{page_number + 1}\n{page_text}")
            
            return "\n\n".join(all_text)
        
        
def extract_tables(file_path:str) -> list:
    all_tables = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            tables_on_pages = page.extract_tables()
            if tables_on_pages:
                for table in tables_on_pages:
                    table_text = convert_table_to_text(table, page_number+1)
                    all_tables.append({
                        "page": page_number +1,
                       "content" : table_text,
                       "raw" : table 
                        
                    })
            
            return all_tables
    