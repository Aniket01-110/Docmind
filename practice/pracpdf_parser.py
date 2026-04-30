#writing code for converting extracted texts into embeddings
from sentence_transformers import SentenceTransformer
from typing import list
import numpy as np

model_name = "all-miniLLM-L2-v6"

model = SentenceTransformer(model_name)

#single text embedding

def embed_text(text: str) -> list[float]:
#converting text into vector form , thats embedding
    embed = model.encode(text, convert_to_numpy=True)
    return embed.tolist()



