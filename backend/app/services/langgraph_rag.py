from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from app.services.embeddings import embed_Text
from app.services.vector_store import search_chunks
from app.services.rag_engine import(build_context, generate_answer)
from app.config import GROQ_API_KEY
from groq import Groq

groq_client = Groq(api_key=GROQ_API_KEY)

#langgraph manages the states of the workflow of the RAG system, here we are building corrective adaptive RAG were langgraph works to determine various states of the workflow, where user input query can be vague, it is rewritten formally and retrieved chunks with proper context awareness about neighbouring text too, and then answer is generated, and generated answers quality is evaluated before giving it to the user, and if it is of poor quality then it is improved by retrieving better, and and again its quality is checked, and if retreival is fails multiple times, we will apply web search for better quality retrieval


class RAGState(TypedDict):
    """"state object passed between graph nodes. each node reads from the state and writes back, like a shared memory between pipeline"""
    
    question: str
    document_id: str
    rewritten_query: str
    chunks: List[dict]
    context: str
    answer: str
    quality: str
    iterations: int
    is_complete: bool


#now from here we write for each node, and what it does in the pipeline

def analyse_query(state: RAGState) -> RAGState:
    """
  NODE 1 analyses query, improves the vague query inroder to form moremeaningful structred format of question, its trivial step for good retrieval before retrieval steps
    """

    question = state["question"]

    prompt = f"""Rewrite this question as ONE clear, specfic sentence for document search, Output only the rewritten question. NO numbering, no options, no explanation

Original: {question}
Rewritten:"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        rewritten = response.choices[0].message.content.strip()
    except Exception:
        rewritten = question

    print(f" Query rewritten: {rewritten}")

    # Update state — pass to next node
    return {**state, "rewritten_query": rewritten}


def retrieve_chunks(state: RAGState) -> RAGState:
    """
    Node 2 — Retrieve relevant chunks from ChromaDB.
    
    """

    query = state["rewritten_query"]
    document_id = state["document_id"]
    iterations = state.get("iterations", 0)

    # Embed query
    query_embedding = embed_Text(query)

    # Search ChromaDB
    chunks = search_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        n_results=5
    )

    print(f" Retrieved {len(chunks)} chunks")

    return {**state, "chunks": chunks, "iterations" : iterations +1}


def evaluate_quality(state: RAGState) -> RAGState:
    """
    Node 3 — Evaluate retrieval quality.
    Corrective RAG — decides if retrieval is good.

    Returns quality: GOOD / POOR / VERY_POOR
    """

    chunks = state["chunks"]
    question = state["question"]

    if not chunks:
        return {**state, "quality": "VERY_POOR"}

    # Check average similarity score
    avg_similarity = sum(
        c["similarity"] for c in chunks
    ) / len(chunks)

    # Simple threshold-based evaluation
    
    if avg_similarity >= 0.3:
        quality = "GOOD"
    elif avg_similarity >= 0.15:
        quality = "POOR"
    else:
        quality = "VERY_POOR"

    print(f"Retrieval quality: {quality} "
          f"(avg similarity: {avg_similarity:.3f})")

    return {**state, "quality": quality}


def generate_response(state: RAGState) -> RAGState:
    """
    Node 4 — Generate answer using LLM.
    Uses retrieved chunks as context.
    """

    chunks = state["chunks"]
    question = state["question"]

    # Build context from chunks
    context = build_context(chunks)

    # Generate answer
    answer = generate_answer(question, context)

    print(f"Answer generated")

    return {**state, "context": context, "answer": answer}


def reflect_on_answer(state: RAGState) -> RAGState:
    """
    Node 5 — Self-reflection on answer quality.
    Checks if answer is complete or needs retry.
    """

    answer = state["answer"]
    question = state["question"]
    iterations = state.get("iterations", 0)

    # Max 2 retries to prevent infinite loop
    if iterations >= 2:
        return {**state, "is_complete": True}

    prompt = f"""Is this answer complete and accurate?

    Question: {question}
    Answer: {answer}

Reply with ONE word: COMPLETE or INCOMPLETE"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=5,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        is_complete = "COMPLETE" in result.upper()
    except Exception:
        is_complete = True

    print(f"Answer reflection: "
          f"{'Complete' if is_complete else 'Incomplete'}")

    return {
        **state,
        "is_complete": is_complete,
        "iterations": iterations + 1
    }


#Routing functions, deciding the next node
def route_after_quality(state: RAGState) -> str:
    """
    After quality evaluation — where to go?

    GOOD     → generate answer
    POOR     → retry retrieval with better query
    VERY_POOR → generate with what we have
    """

    quality = state["quality"]
    iterations = state.get("iterations", 0)

    if quality == "GOOD":
        return "generate"
    elif quality == "POOR" and iterations < 2:
        # retry once with original question
        return "retrieve"
    else:
        # very poor — just generate anyway
        return "generate"


def route_after_reflection(state: RAGState) -> str:
    """
    After self-reflection — where to go?

    Complete   → END
    Incomplete → retry retrieve
    """

    if state["is_complete"]:
        return END
    else:
        return "retrieve"


#Building graphs

def build_rag_graph() -> StateGraph:
    """
    Build the LangGraph RAG pipeline.

    """

    # Create graph with our state type
    graph = StateGraph(RAGState)

    # Add nodes — each is one pipeline step
    graph.add_node("analyse", analyse_query)
    graph.add_node("retrieve", retrieve_chunks)
    graph.add_node("evaluate", evaluate_quality)
    graph.add_node("generate", generate_response)
    graph.add_node("reflect", reflect_on_answer)

    # Add edges — fixed connections
    graph.add_edge("analyse", "retrieve")
    graph.add_edge("retrieve", "evaluate")
    graph.add_edge("generate", "reflect")

    # Add conditional edges — dynamic routing
    graph.add_conditional_edges(
        "evaluate",          # from this node
        lambda state: (
            "generate" if state["quality"] == "GOOD"
            
            else "generate"
        )
    )
    
   

    graph.add_conditional_edges(
        "reflect",
        lambda state: (
            END if state["is_complete"]
            else "retrieve"
        )
    )

    # Set entry point
    graph.set_entry_point("analyse")

    # Compile graph
    return graph.compile()



# MAIN FUNCTION


# Build graph once at module level
rag_graph = build_rag_graph()


def langgraph_query(
    question: str,
    document_id: str
) -> dict:
    """
    
    Args:
        question: user's question
        document_id: which document to search

    Returns:
        answer with metadata
    """

    print(f"\n{'='*50}")
    print(f" LangGraph RAG Pipeline Starting")
    print(f"{'='*50}")

    # Initial state
    initial_state: RAGState = {
        "question": question,
        "document_id": document_id,
        "rewritten_query": question,
        "chunks": [],
        "context": "",
        "answer": "",
        "quality": "",
        "iterations": 0,
        "is_complete": False
    }

    # Run graph — executes nodes in order
    # handles routing automatically
    final_state = rag_graph.invoke(initial_state)

    return {
        "answer": final_state["answer"],
        "question": final_state["question"],
        "rewritten_query": final_state["rewritten_query"],
        "quality": final_state["quality"],
        "iterations": final_state["iterations"],
        
        "chunks_used": len(final_state["chunks"]),
        "sources": [
            c["text"][:200]
            for c in final_state["chunks"]
        ]
    }

