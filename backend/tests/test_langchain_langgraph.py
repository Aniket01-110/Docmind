# backend/tests/test_langchain_langgraph.py

from app.services.langchain_rag import langchain_full_pipeline
from app.services.langgraph_rag import langgraph_query

def test_langchain():
    print("\n=== LANGCHAIN RAG TEST ===")
    result = langchain_full_pipeline(
        pdf_path="tests/sample.pdf",
        question="What are the technical skills?"
    )
    print(f"Answer: {result['answer']}")
    print(f"Sources: {len(result['sources'])}")

def test_langgraph():
    print("\n=== LANGGRAPH RAG TEST ===")
    result = langgraph_query(
        question="What are the technical skills?",
        document_id="test_doc_001"
    )
    print(f"Answer: {result['answer']}")
    print(f"Quality: {result['quality']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Rewritten query: {result['rewritten_query']}")

test_langchain()
test_langgraph()