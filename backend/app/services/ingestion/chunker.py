# backend/app/services/ingestion/chunker.py

from typing import List

# ─────────────────────────────────────────
# CONSTANTS — chunking settings
# ─────────────────────────────────────────

# How many characters per chunk
# 1000 chars ≈ 200-250 words ≈ enough context for one idea
CHUNK_SIZE = 1000

# How many characters chunks share with neighbours
# 200 chars ≈ 1-2 sentences of overlap
CHUNK_OVERLAP = 200


# ─────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> List[dict]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: raw text extracted from document
        chunk_size: maximum characters per chunk
        overlap: characters shared between chunks

    Returns:
        list of chunk dictionaries with text and metadata
    """

    # Clean the text first
    # replace multiple newlines/spaces with single ones
    text = clean_text(text)

    # If text is shorter than chunk size
    # no need to split — return as single chunk
    if len(text) <= chunk_size:
        return [{
            "chunk_index": 0,
            "text": text,
            "char_start": 0,
            "char_end": len(text),
            "chunk_size": len(text)
        }]

    # Split into chunks
    chunks = []
    start = 0
    chunk_index = 0

    # Keep chunking until we reach the end of text
    while start < len(text):

        # Calculate where this chunk ends
        end = start + chunk_size

        # If end goes beyond text length
        # just take everything until the end
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

        # Try to find a good break point
        # We don't want to cut in the middle of a word
        # Look for nearest space before the end
        break_point = find_break_point(text, start, end)

        # Extract this chunk
        chunk_text_content = text[start:break_point].strip()

        # Only add if chunk has actual content
        if chunk_text_content:
            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk_text_content,
                "char_start": start,
                "char_end": break_point,
                "chunk_size": len(chunk_text_content)
            })

        # Move start forward
        # subtract overlap so next chunk shares some text
        start = break_point - overlap
        chunk_index += 1

    return chunks


# ─────────────────────────────────────────
# HELPER — find good break point
# ─────────────────────────────────────────

def find_break_point(text: str, start: int, end: int) -> int:
    """
    Find the nearest sentence or word boundary
    before the end position.
    Avoids cutting text in the middle of a word.
    """

    # Best break — end of sentence
    # Look for . ? ! before end position
    for i in range(end, start, -1):
        if text[i] in ".?!":
            return i + 1

    # Second best — end of word (space)
    for i in range(end, start, -1):
        if text[i] == " ":
            return i

    # Last resort — just cut at end position
    return end


# ─────────────────────────────────────────
# HELPER — clean raw text
# ─────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Clean raw extracted text.
    Remove excessive whitespace and normalize newlines.
    """

    import re

    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)

    # Replace multiple newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


# ─────────────────────────────────────────
# HELPER — chunk with metadata
# ─────────────────────────────────────────

def chunk_document(extracted_content: dict,document_id: str) -> List[dict]:
    """
    Chunk a full document including tables.
    Takes output from pdf_parser and returns
    chunks ready for embedding.

    Args:
        extracted_content: output from extract_pdf_content()
        document_id: unique ID for this document

    Returns:
        list of chunks ready for ChromaDB
    """

    all_chunks = []

    # Chunk the main text
    text_chunks = chunk_text(extracted_content["text"])

    for chunk in text_chunks:
        all_chunks.append({
            "document_id": document_id,
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
            "chunk_type": "text",
            "metadata": {
                "document_id": document_id,
                "chunk_index": chunk["chunk_index"],
                "chunk_type": "text",
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"],
                "source": extracted_content["file_path"]
            }
        })

    # Chunk the tables too
    for table in extracted_content["tables"]:
        table_chunks = chunk_text(table["content"])

        for chunk in table_chunks:
            all_chunks.append({
                "document_id": document_id,
                "chunk_index": len(all_chunks),
                "text": chunk["text"],
                "chunk_type": "table",
                "metadata": {
                    "document_id": document_id,
                    "chunk_index": len(all_chunks),
                    "chunk_type": "table",
                    "page": table["page"],
                    "source": extracted_content["file_path"]
                }
            })

    return all_chunks