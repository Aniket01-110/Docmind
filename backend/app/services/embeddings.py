print("Gemini embeddings loaded")
from google import genai
from typing import List
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

EMBED_MODEL = "gemini-embedding-001"

def embed_Text(text: str) -> List[float]:
    """
    Convert a single text into embedding vector using Gemini embeddings api"""

    response = client.models.embed_content(
       model = EMBED_MODEL,
       contents = text
   )
    return response.embeddings[0].values

def embed_chunks(chunks: List[dict]) -> List[dict]:
    
    texts = [chunk["text"] for chunk in chunks]
    response = client.models.embed_content(model=EMBED_MODEL, contents = texts)
    """
ADD Batch embeddings """

    embeddings = [item.values 
    for item in response.embeddings]
    
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
    return chunks

