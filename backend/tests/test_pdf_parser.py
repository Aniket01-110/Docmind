from app.services.ingestion.pdf_parser import extract_pdf_content
from app.services.ingestion.chunker import chunk_document
from app.services.embeddings import (
    embed_Text,
    embed_texts,
    embed_chunks,
    cosine_similarity
)

def test_embeddings():

    # Test 1 — single embedding
    text = "Gradient descent is an optimization algorithm"
    embedding = embed_Text(text)

    print(f"\n=== EMBEDDING TEST ===")
    print(f"Text: {text}")
    print(f"Vector dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

    # Test 2 — similarity between related texts
    text1 = "machine learning optimization"
    text2 = "gradient descent algorithm"
    text3 = "my cat loves fish"

    emb1 = embed_texts(text1)
    emb2 = embed_texts(text2)
    emb3 = embed_texts(text3)

    sim_related = cosine_similarity(emb1, emb2)
    sim_unrelated = cosine_similarity(emb1, emb3)

    print(f"\n=== SIMILARITY TEST ===")
    print(f"'{text1}' vs '{text2}'")
    print(f"Similarity: {sim_related:.3f}  ← should be HIGH")

    print(f"\n'{text1}' vs '{text3}'")
    print(f"Similarity: {sim_unrelated:.3f} ← should be LOW")

    # Test 3 — embed all chunks from resume
    file_path = "tests/sample.pdf"
    extracted = extract_pdf_content(file_path)
    chunks = chunk_document(extracted, "test_doc_001")
    embedded_chunks = embed_chunks(chunks)

    print(f"\n=== CHUNKS EMBEDDED ===")
    print(f"Total chunks embedded: {len(embedded_chunks)}")
    print(f"Embedding dimensions: {len(embedded_chunks[0]['embedding'])}")

test_embeddings()