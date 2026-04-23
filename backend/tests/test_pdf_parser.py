# backend/tests/test_pdf_parser.py

from app.services.ingestion.pdf_parser import extract_pdf_content
from app.services.ingestion.chunker import chunk_document


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


def test_chunker():

    file_path = "tests/sample.pdf"
    extracted = extract_pdf_content(file_path)
    chunks = chunk_document(extracted, document_id="test_doc_001")

    print(f"\n=== TOTAL CHUNKS: {len(chunks)} ===")

    for chunk in chunks:
        print(f"\n{'='*50}")
        print(f"Chunk Index : {chunk['chunk_index']}")
        print(f"Type        : {chunk['chunk_type']}")
        print(f"Size        : {chunk['chunk_size']} chars")
        print(f"Text Preview:\n{chunk['text'][:300]}")
        print(f"{'='*50}")


# Run both tests
test_pdf_parser()
test_chunker()