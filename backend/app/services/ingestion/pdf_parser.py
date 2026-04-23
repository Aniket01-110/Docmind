import fitz
import pdfplumber
import os

def extract_pdf_content(file_path: str) -> dict:
    """ Extract all content from a PDF file .
    Args:
        file_path: path to the PDF file  on disk
    
    Returns:
        dictoinary contalining text, tables and metadata
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    
    text_content = extract_text(file_path)
    tables = extract_tables(file_path)
    metadata = extract_metadata(file_path)
    return{
        "text": text_content,
        "tables": tables,
        "metadata": metadata,
        "total_pages": metadata.get("total_pages", 0),
        "file_path": file_path
         
    }
    
    
def extract_text(file_path: str) -> str:
    """ Extract all text from PDF page by page.
    Returns one big string of all text combined"""
    
    all_text = []
    
     #with statement is the context manager it automatically handles opening AND closing a resource
    with fitz.open(file_path) as pdf: 
        #do stuff, #file closes automatically #even if error occurs 
        
        for page_number, page in enumerate(pdf): #enumerate gives both index and item at the index
            
            page_text = page.get_text("text")
            
            
            if page_text.strip():
                all_text.append(
                    f"[Page {page_number +1}]\n{page_text}"
                )
        return "\n\n".join(all_text)
    
#Table extraction 

def extract_tables(file_path: str) -> list:
    """Extract all tables from PDF.
    Returns list of tables,each table  is  a lost of rows."""
    
    all_tables=[]
    
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            #extract tables () finds all tables on this page
            #returns list of tables 
            # each table is list of rows
            #each row is list of cell values 
            
            #if this page has tables
            tables_on_page =  page.extract_tables()
            if tables_on_page:
                for table  in tables_on_page:
                    
                    #convert table to readanle text format
                    table_text = convert_table_to_text(table, page_number +1)
                    all_tables.append({
                        "page": page_number + 1,
                        "content": table_text,
                        "raw": table
                    })
    return all_tables
    
    #Table converter 
def convert_table_to_text(table: list, page_number: int)-> str:
    """Convert a raw table (list of lists) into readable text format for embedding"""
    
    lines = [f"[Table on page{page_number}]"]
    
    for row in table:
        #for empty data cells replace them with empty string
        cleaned_row = [
            str(cell) if cell is  not None else""
            for cell in row
        ]
        #joining cells with | spearator, makes table readable as plain text
        lines.append("|".join(cleaned_row))
    return "\n".join(lines)

#metadata extraction  -Pdf INFO

def extract_metadata(file_path: str) -> dict:
    """Extract metadata from PDF - title, author,  pagecount, creation date"""
    
    with fitz.open(file_path) as pdf:
        raw_metadata = pdf.metadata
        
        return{
            "title": raw_metadata.get("title", "Unknown"),
            "author": raw_metadata.get("author", "Unknown"),
            "total_pages": pdf.page_count,
            "created": raw_metadata.get("CreationDate", "Unknown"),
            "modified": raw_metadata.get("modifiedDate", "Unknown"),
            "file_size_kb": round(os.path.getsize(file_path)/1024,2) #divided by 1024 to get answer in kilobytes and upto 2 decimal places
        }

            
            
        
    

   
   
  