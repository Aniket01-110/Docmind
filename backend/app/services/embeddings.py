from google import genai
from typing import List
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

EMBED_MODEL = "text-embedding-004"

def embed_Text(text: str) -> List[float]:
    """
    Convert a single text into embedding vector using Gemini embeddings api"""

    response = client.models.embed_content(
       model = EMBED_MODEL,
       contents = text
   )
    return response.embeddings[0].values

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """
ADD EMBEDDINGS TO EVERY CHUNK"""
    for chunk in chunks:
        chunk["embedding"] = embed_Text(chunk["text"])
    return chunks