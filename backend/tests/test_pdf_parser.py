from app.services.vector_store import (
    add_chunks,
    search_chunks,
    get_chunk_count,
    document_exists
)
from app.services.embeddings import embed_chunks, embed_Text
from app.services.ingestion.pdf_parser import extract_pdf_content
from app.services.ingestion.chunker import chunk_document
from app.services.rag_engine import query_document

def test_vector_store():

    # Step 1 — get embedded chunks
    file_path = "tests/sample.pdf"
    extracted = extract_pdf_content(file_path)
    chunks = chunk_document(extracted, "test_doc_001")
    embedded = embed_chunks(chunks)

    # Step 2 — store in ChromaDB
    print("\n=== STORING CHUNKS ===")
    success = add_chunks(embedded)
    print(f"Storage successful: {success}")
    print(f"Total chunks in DB: {get_chunk_count()}")

    # Step 3 — check document exists
    print("\n=== DOCUMENT EXISTS CHECK ===")
    exists = document_exists("test_doc_001")
    print(f"Document exists: {exists}")

    # Step 4 — search with a question
    print("\n=== SEARCHING ===")
    question = "What are the skills?"
    question_embedding = embed_Text(question)

    results = search_chunks(
        query_embedding=question_embedding,
        document_id="test_doc_001",
        n_results=3
    )

    print(f"Question: {question}")
    print(f"Results found: {len(results)}")

    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Similarity: {result['similarity']}")
        print(f"Text: {result['text'][:200]}")

test_vector_store()


def test_rag():

    document_id = "test_doc_001"

    questions = [
        "What are the technical skills?",
        "What projects has the developer built?",
        "What is the educational background?",
        "What is the GitHub profile link?",
        "What is the professional summary?"  # ← your new question
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")

        result = query_document(
            question=question,
            document_id=document_id
        )

        print(f"Answer:\n{result['answer']}")
        print(f"\nChunks used: {result['chunks_used']}")
test_rag()
