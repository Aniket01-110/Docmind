from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


model = None
model_name = "all-MiniLM-L6-v2"

def get_model():
    global model
    
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer(model_name)
    
    return model

#single text embedding

def embed_Text(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()



#BATCH EMBEDDING - multiple texts at once
def embed_texts(texts: List[str]) ->List[List[float]]:
    """CONVERT multpile texts into embedding vectors at once, 
    faster than embedding one by one
    Args:
        texts: list of strings to embed
        
    Returns:
        list of embedding vectors, one per text
    """
    model = get_model()
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True, convert_to_numpy=True)
    return embeddings.tolist()


#embedding chunks that are obtained

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """Add emnbedding to chunks from chunker
    Takes output from chunk_document() and adds embedding vector to each chunk
    
    Args:
        chunks:list of chunk dicts from chunk_documents()
    Returns:
        same chunks with 'embedding' field added
    """
    
    #Extract just text from each chunk 
    #WE EMBED text only, not the whole chunk
    texts = [chunk["text"] for chunk in chunks]
    
    print(f"Embedding {len(texts)} chunks...")
    embeddings = embed_texts(texts)
    
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
    
    #zip() pairs each chunk with its embedding, 
    #zip([chunk1,chunk2],[emb1, emb2])
    # -> [(chunk1, emb1), (chunk2, emb2)]
    
    return chunks

    
#after getting embeddings for everything lets see similarity between each encoded vector representation

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate similarity between two embedding vectors.
    Returns value between 0 and 1.
    0.0 = completely different meaning"""
    
    #convert to numpy arrays for math operation
    a = np.array(vec1)
    b = np.array(vec2)
    
    #cosine similarity formula : (a.b)/(|a| * |b|)
    #dot product divided by product of magnitudes
    
    similarity = np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return float(similarity)