

from groq import Groq
from typing import List
from app.config import GROQ_API_KEY
from app.services.embeddings import embed_Text
from app.services.vector_store import search_chunks
from app.services.vector_store import get_chunk_count

# ─────────────────────────────────────────
# GROQ CLIENT SETUP
# ─────────────────────────────────────────

# Initialize Groq client once at module level
# same singleton pattern as before
client = Groq(api_key=GROQ_API_KEY)

# Free, fast model from Groq
# llama3-8b-8192 means:
# llama3    → Meta's Llama 3 model
# 8b        → 8 billion parameters
# 8192      → can read 8192 tokens at once
MODEL = "llama-3.1-8b-instant"

# Maximum tokens in response
MAX_TOKENS = 1024


# 
# SYSTEM PROMPT
#

SYSTEM_PROMPT = """You are DocMind, an intelligent document assistant.

Your job is to answer questions based ONLY on the document
context provided to you. Follow these rules strictly:

1. ONLY use information from the provided context
2. If the answer is not in the context, say clearly:
   "I couldn't find this information in the document."
3. Always be specific and reference the document content
4. Never make up information not present in the context
5. Keep answers clear, concise and helpful
6. If asked about something partially covered, answer
   what you can and note what's missing"""



# BUILD CONTEXT


def build_context(chunks: List[dict]) -> str:
    """
    Format retrieved chunks into context string
    for the LLM to read and reason over.
    """

    if not chunks:
        return "No relevant context found in the document."

    context_parts = []

    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Context {i+1}]\n{chunk['text']}\n"
        )

    return "\n---\n".join(context_parts)


# BUILD PROMPT


def build_prompt(question: str, context: str) -> str:
    """
    Combine context and question into full prompt.
    """

    return f"""Here are the relevant sections from the document:

{context}

Based ONLY on the context above, please answer
this question:

{question}

If the information is not in the context above,
say so clearly rather than guessing."""



# GENERATE ANSWER


def generate_answer(question: str,
                    context: str) -> str:
    """
    Send question + context to Groq and get answer.
    """

    try:
        prompt = build_prompt(question, context)

        # Groq uses OpenAI-compatible API structure
        # messages list contains conversation history
        # system message → instructions
        # user message → question + context
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract answer text from response
        # choices[0] → first completion choice
        # message.content → actual text
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating answer: {str(e)}"



# MAIN RAG FUNCTION


def query_document(question: str,
                   document_id: str,
                   n_results: int = 5) -> dict:
    """
    Main RAG function — retrieves relevant chunks
    and generates answer using Groq LLM.

    Steps:
    1. Embed the question
    2. Search ChromaDB for similar chunks
    3. Format chunks into context
    4. Send to Groq → get answer
    5. Return answer + sources
    """

    

    # ── Step 1: Embed question ──
    print(f" Embedding question...")
    question_embedding = embed_Text(question)

    # ── Step 2: Smart retrieval ──
    # get total chunks for this document
    # retrieve all of them if small document
    total_chunks = get_chunk_count()
    n_results = min(n_results, total_chunks)

    print(f" Searching {total_chunks} chunks...")
    chunks = search_chunks(
        query_embedding=question_embedding,
        document_id=document_id,
        n_results=n_results
    )

    if not chunks:
        return {
            "answer": "No relevant content found in document.",
            "sources": [],
            "question": question,
            "document_id": document_id
        }

    #  Step 3: Build context 
    context = build_context(chunks)

    # Step 4: Generate answer
    print(f" Generating answer with Groq...")
    answer = generate_answer(question, context)

    # Step 5: Return everything 
    return {
        "answer": answer,
        "sources": [chunk["text"][:200] for chunk in chunks],
        "similarity_scores": [chunk["similarity"] for chunk in chunks],
        "question": question,
        "document_id": document_id,
        "chunks_used": len(chunks)
    }