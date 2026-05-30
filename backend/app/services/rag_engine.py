

from groq import Groq
from typing import List
from app.config import GROQ_API_KEY
from app.services.embeddings import embed_Text
from app.services.vector_store import search_chunks
from app.services.vector_store import get_chunk_count
from app.services.vector_store import get_document_chunk_count

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
context provided to you.

Rules:

1.Priortize factual accuracy from the document
2. If the exact answer exists in the context, provide it clearly
3. If the answer is not explicity stated but is strongly implied, you may provide the inferred answer BUT clearly mention that it is inferred from the document context.
4. Never invent unsupported facts.
5. If information is missing entirely, say:
"I couldnt find this information in this document"
6.Keep answers concise, helpful, and context-aware

7. When possible,  mention which part of the document supports the answer"""                                                                                                                                                                                                        


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

#build prompt
def build_prompt(question: str, context: str) -> str:
    """
    Build final prompt sent to Groq.
    Combines retrieved document context with user question.
    """

    return f"""
Document Context:
{context}

Question:
{question}

Instructions:
- Answer ONLY using the document context above.
- Do not use outside knowledge.
- If the answer is explicitly present, provide it clearly.
- If the answer is strongly implied, mention that it is inferred.
- If the answer cannot be found in the context, say:
  "I couldn't find this information in this document."

Answer:
"""


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

    print("step1: entered query_document")

    # ── Step 1: Embed question ──
    question_embedding = embed_Text(question)
    print(f" step 2 Embedding question...")
    
    total_chunks = get_document_chunk_count(document_id) 
    print("step 3: got chunk count")
    n_results = min(n_results, total_chunks)
    

    # ── Step 2: Smart retrieval ──
    # get total chunks for this document
    # retrieve all of them if small document
    
   

    
    chunks = search_chunks(
        query_embedding=question_embedding,
        document_id=document_id,
        n_results=n_results
    )
    print("Step 4: retrieval done")

    if not chunks:
        return {
            "answer": "No relevant content found in document.",
            "sources": [],
            "question": question,
            "document_id": document_id
        }

    #  Step 3: Build context 
    
   

    context = build_context(chunks)
    print('step 5 : context built')
    # Step 4: Generate answer
    
    
    answer = generate_answer(question, context)
    print("step 6: answer generated")

    print("Step 7 answer generated")
    # Step 5: Return everything 
    return {
        "answer": answer,
        "sources": [chunk["text"][:200] for chunk in chunks],
        "similarity_scores": [chunk["similarity"] for chunk in chunks],
        "question": question,
        "document_id": document_id,
        "chunks_used": len(chunks)
    }
def generate_answer(question: str, context: str) -> str:
    """send question + context to groq and get an answer
    """
    try:
        prompt = build_prompt(question, context)
        
        response = client.chat.completions.create(
            model = MODEL,
            max_tokens = MAX_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content" : prompt
                }
            ]
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating answer:{str(e)}"
