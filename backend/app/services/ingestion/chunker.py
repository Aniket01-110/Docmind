# backend/app/services/ingestion/chunker.py

from typing import List
from groq import Groq
from app.config import GROQ_API_KEY
import re

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Initialize Groq for universal detection
# loaded once at module level — singleton pattern
groq_client = Groq(api_key=GROQ_API_KEY)


# ─────────────────────────────────────────
# MAIN CHUNKING FUNCTION
# ─────────────────────────────────────────

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> List[dict]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: raw text extracted from document
        chunk_size: maximum characters per chunk
        overlap: characters shared between chunks

    Returns:
        list of chunk dictionaries with text and metadata
    """

    text = clean_text(text)

    if len(text) <= chunk_size:
        return [{
            "chunk_index": 0,
            "text": text,
            "char_start": 0,
            "char_end": len(text),
            "chunk_size": len(text)
        }]

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):

        end = start + chunk_size

        if end >= len(text):
            chunk_text_content = text[start:]
            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk_text_content,
                "char_start": start,
                "char_end": len(text),
                "chunk_size": len(chunk_text_content)
            })
            break

        break_point = find_break_point(text, start, end)
        chunk_text_content = text[start:break_point].strip()

        if chunk_text_content:
            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk_text_content,
                "char_start": start,
                "char_end": break_point,
                "chunk_size": len(chunk_text_content)
            })

        start = break_point - overlap
        chunk_index += 1

    return chunks


# ─────────────────────────────────────────
# CHUNK DOCUMENT — main entry point
# ─────────────────────────────────────────

def chunk_document(
    extracted_content: dict,
    document_id: str,
    filename: str = "document"
) -> List[dict]:
    """
    Chunk a full document including tables.
    Adds universal contextual enrichment to every chunk.

    Args:
        extracted_content: output from any parser
        document_id: unique ID for this document
        filename: original filename for context

    Returns:
        list of chunks ready for ChromaDB
        each chunk has contextual_text for embedding
        and original text for display
    """

    all_chunks = []

    # Chunk main text
    text_chunks = chunk_text(extracted_content["text"])

    for chunk in text_chunks:
        all_chunks.append({
            "document_id": document_id,
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
            "chunk_type": "text",
            "chunk_size": chunk["chunk_size"],
            "metadata": {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "chunk_type": "text",
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "source": filename
            }
        })
    print(extracted_content)
    
    # Chunk tables 
    for table in extracted_content.get("table", []):
        table_chunks = chunk_text(table["content"])

        for chunk in table_chunks:
            all_chunks.append({
                "document_id": document_id,
                "chunk_index": len(all_chunks),
                "text": chunk["text"],
                "chunk_type": "table",
                "chunk_size": chunk["chunk_size"],
                "metadata": {
                    "document_id": document_id,
                    "chunk_index": len(all_chunks),
                    "chunk_type": "table",
                    "page": table["page"],
                    "source": filename
                }
            })

    # Add universal contextual enrichment
    # this is what makes retrieval intelligent
    all_chunks = build_contextual_chunks_universal(
        chunks=all_chunks,
        extracted_content=extracted_content,
        document_id=document_id,
        filename=filename
    )

    return all_chunks


# ─────────────────────────────────────────
# UNIVERSAL CONTEXTUAL ENRICHMENT
# ─────────────────────────────────────────

def build_contextual_chunks_universal(
    chunks: List[dict],
    extracted_content: dict,
    document_id: str,
    filename: str = "document"
) -> List[dict]:
    """
    Universal contextual enrichment using LLM.
    Works for ANY document type, ANY domain,
    ANY language. Not hardcoded — self-adapting.

    Called once per document upload.
    Zero extra cost during queries.

    Args:
        chunks: list of chunks from chunk_document()
        extracted_content: full parsed document
        document_id: unique document ID
        filename: original filename

    Returns:
        same chunks with contextual_text added
    """

    total_chunks = len(chunks)
    full_text = extracted_content.get("text", "")

    # Step 1 — detect document type (1 LLM call)
    print("🔍 Detecting document type...")
    doc_type = detect_document_type(
        full_text=full_text,
        filename=filename
    )
    print(f"   Document type: {doc_type}")

    # Step 2 — generate document summary (1 LLM call)
    print("📝 Generating document summary...")
    doc_summary = generate_document_summary(
        full_text=full_text,
        doc_type=doc_type
    )
    print(f"   Summary: {doc_summary[:100]}...")

    # Step 3 — enrich each chunk (1 LLM call per chunk)
    print(f"🧠 Adding context to {total_chunks} chunks...")

    for i, chunk in enumerate(chunks):

        # Detect section for this specific chunk
        section = detect_section_universal(
            chunk_text=chunk["text"],
            doc_type=doc_type
        )

        # Get window context from neighbours
        prev_text = get_neighbour_text(chunks, i - 1)
        next_text = get_neighbour_text(chunks, i + 1)

        # Build enriched text for embedding
        contextual_text = f"""[Document Summary: {doc_summary}]
[Document Type: {doc_type}]
[Filename: {filename}]
[Section: {section}]
[Position: chunk {i + 1} of {total_chunks}]
[Previous context: {prev_text}]

{chunk["text"]}

[Next context: {next_text}]"""

        # Store enriched version for embedding
        # original text preserved for display
        chunk["contextual_text"] = contextual_text

        # Store detection results in metadata
        # persisted in ChromaDB permanently
        chunk["metadata"]["section"] = section
        chunk["metadata"]["document_type"] = doc_type
        chunk["metadata"]["position"] = (
            f"{i + 1} of {total_chunks}"
        )

        print(
            f"   Chunk {i + 1}/{total_chunks}"
            f" → section: {section}"
        )

    return chunks


# ─────────────────────────────────────────
# LLM — DOCUMENT TYPE DETECTION
# ─────────────────────────────────────────

def detect_document_type(
    full_text: str,
    filename: str
) -> str:
    """
    Use LLM to detect document type.
    Works for ANY file type and domain.
    Called once per document upload.
    """

    prompt = f"""What type of document is this?

Filename: {filename}
First 500 characters of content:
{full_text[:500]}

Reply with ONE word or short phrase only.
Examples: resume, research_paper, legal_contract,
medical_report, financial_report, textbook,
news_article, recipe, technical_manual,
meeting_notes, lecture_transcript, other

Document type:"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=10,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Document type detection failed: {e}")
        return "document"


# ─────────────────────────────────────────
# LLM — DOCUMENT SUMMARY GENERATION
# ─────────────────────────────────────────

def generate_document_summary(
    full_text: str,
    doc_type: str
) -> str:
    """
    Generate brief document summary using LLM.
    Prepended to every chunk for global context.
    Called once per document upload.
    """

    prompt = f"""Summarize this {doc_type} document 
in exactly 2 sentences.

Focus on: what it is, who it is about or for,
and the main topic or purpose.

Document content (first 1000 characters):
{full_text[:1000]}

2-sentence summary:"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=80,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Summary generation failed: {e}")
        return f"A {doc_type} document."


# ─────────────────────────────────────────
# LLM — SECTION DETECTION (UNIVERSAL)
# ─────────────────────────────────────────

def detect_section_universal(
    chunk_text: str,
    doc_type: str
) -> str:
    """
    Use LLM to detect which section this chunk
    belongs to. Works for ANY document domain.

    Not hardcoded — adapts to document type.
    Called once per chunk during upload.
    """

    prompt = f"""This text is from a {doc_type} document.

What section or category does this text belong to?
Reply with 1-3 words maximum.
Be specific to the document type.

Examples by document type:
- resume: "work experience", "technical skills", "education"
- legal_contract: "liability clause", "payment terms"
- medical_report: "patient history", "diagnosis", "treatment"
- research_paper: "methodology", "results", "conclusion"
- recipe: "ingredients", "preparation steps"
- financial_report: "revenue summary", "risk factors"

Text to classify:
{chunk_text[:300]}

Section (1-3 words only):"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=10,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Section detection failed: {e}")
        return "general"


# ─────────────────────────────────────────
# HELPER — GET NEIGHBOUR TEXT
# ─────────────────────────────────────────

def get_neighbour_text(
    chunks: List[dict],
    index: int
) -> str:
    """
    Get abbreviated text from neighbouring chunk.
    Returns empty string if neighbour doesn't exist.
    Used for window context in embeddings.
    """

    # Check index is valid
    if index < 0 or index >= len(chunks):
        return "none"

    # First 100 chars — enough context, not too noisy
    return chunks[index]["text"][:100] + "..."


# ─────────────────────────────────────────
# HELPER — FIND BREAK POINT
# ─────────────────────────────────────────

def find_break_point(
    text: str,
    start: int,
    end: int
) -> int:
    """
    Find nearest sentence or word boundary.
    Avoids cutting text in middle of word.
    """

    # Best — sentence boundary
    for i in range(end, start, -1):
        if text[i] in ".?!":
            return i + 1

    # Second — word boundary
    for i in range(end, start, -1):
        if text[i] == " ":
            return i

    # Last resort — cut at end
    return end


# ─────────────────────────────────────────
# HELPER — CLEAN TEXT
# ─────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Clean raw extracted text.
    Remove excessive whitespace and normalize newlines.
    """

    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)

    # Replace 3+ newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text