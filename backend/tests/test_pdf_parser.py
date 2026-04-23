# backend/tests/test_pdf_parser.py

from app.services.ingestion.pdf_parser import extract_pdf_content

def test_pdf_parser():
    
    file_path = "tests/sample.pdf"
    
    result = extract_pdf_content(file_path)
    
    print("=== METADATA ===")
    print(result["metadata"])
    
    print("\n=== TOTAL PAGES ===")
    print(result["total_pages"])
    
    print("\n=== TEXT PREVIEW ===")
    print(result["text"][:500])
    
    print("\n=== TABLES FOUND ===")
    print(f"{len(result['tables'])} tables found")

test_pdf_parser()