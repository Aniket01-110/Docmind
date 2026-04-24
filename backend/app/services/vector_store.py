import chromadb
from chromadb.config import Settings
from typing import List, Optional
import os

# Where ChromaDB stores data on disk
# This folder gets created automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
# Collection name —  just like a table name in SQL
COLLECTION_NAME = "docmind_chunks"

# Initialized ChromaDB client
# PersistentClient means data saved to disk whnerver server restarts no need previohs data is saved
client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(anonymized_telemetry=False)
)

# Get or create collection
# if collection exists → get it
# if collection doesn't exist → create it
# this is safe to call every time server starts
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,

    metadata={"hnsw:space": "cosine"}
)



def add_chunks(chunks: List[dict]) -> bool:
    """
    Store embedded chunks in ChromaDB.
    Takes output from embed_chunks() in Session 6.

    Args:
        chunks: list of chunk dicts with embeddings

    Returns:
        True if successful, False if failed
    """

    try:
        # ChromaDB needs four separate lists
        # one for each piece of data
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for chunk in chunks:

            # ID must be unique across entire collection
            # combine document_id + chunk_index
            # guarantees uniqueness
            chunk_id = f"{chunk['document_id']}_{chunk['chunk_index']}"

            ids.append(chunk_id)
            embeddings.append(chunk["embedding"])
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])

        #adding everything to to chromadbin one Go
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        print(f"✅ Added {len(chunks)} chunks to ChromaDB")
        return True

    except Exception as e:
        print(f"❌ Error adding chunks: {e}")
        return False



def search_chunks(
    query_embedding: List[float],
    document_id: str,
    n_results: int = 5
) -> List[dict]:
    """
    Search ChromaDB for chunks similar to query.
    Filters by document_id so only searches
    within the specified document.

    Args:
        query_embedding: embedded question vector
        document_id: only search this document
        n_results: how many chunks to return

    Returns:
        list of relevant chunks with text and metadata
    """

    try:
        # query() is the main search method
        results = collection.query(

            #the  question converted to vector
            query_embeddings=[query_embedding],

            #returns similar chunks
            n_results=n_results,

            # filter by document_id
            # only return chunks from THIS document
            # this is how we keep documents isolated
            where={"document_id": document_id},

            # what to include in results
            include=["documents", "metadatas", "distances"]
        )

        # Format results into clean list of dicts
        chunks = []

        # results["documents"][0] is a list of texts
        # [0] because we sent one query
        # if we sent 3 queries → results["documents"]
        # would have 3 lists
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(
            documents, metadatas, distances
        ):
            # distance in cosine space
            # lower distance = more similar
            # convert to similarity score:
            # similarity = 1 - distance
            similarity = round(1 - distance, 4)

            chunks.append({
                "text": doc,
                "metadata": meta,
                "similarity": similarity
            })

        return chunks

    except Exception as e:
        print(f"❌ Error searching chunks: {e}")
        return []



def delete_document_chunks(document_id: str) -> bool:
    """
    Delete all chunks belonging to a document.
    Called when user deletes a document.

    Args:
        document_id: ID of document to delete

    Returns:
        True if successful
    """

    try:
        # delete() with where filter
        # removes all chunks matching the filter
        collection.delete(
            where={"document_id": document_id}
        )

        print(f"✅ Deleted chunks for document: {document_id}")
        return True

    except Exception as e:
        print(f"❌ Error deleting chunks: {e}")
        return False



def get_chunk_count() -> int:
    """
    Returns total number of chunks in collection.
    Useful for monitoring and debugging.
    """
    return collection.count()



def document_exists(document_id: str) -> bool:
    

    results = collection.get(
        where={"document_id": document_id},
        limit=1
    )

    # if results has any ids → document exists
    return len(results["ids"]) > 0