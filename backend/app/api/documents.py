import os
import uuid #universally unique identifier (used for giving unique id to each objects)
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion.pdf_parser import extract_pdf_content
from app.services.embeddings import embed_chunks
from app.services.ingestion.chunker import chunk_document
from app.services.vector_store import(
    add_chunks,
    document_exists,
    delete_document_chunks,
    get_chunk_count
)

router = APIRouter(prefix="/documents", tags=["Documents"])

#TEMPORARITLY STORING THE folder aftet uploading, before processing them

Uploaded_dir = "uploads"
os.makedirs(Uploaded_dir, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """"""
    
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400,
        detail="Only PDF files supported currently")
        
    document_id = str(uuid.uuid4())
    
    file_path = f"{Uploaded_dir}/{document_id}.pdf"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        if document_exists(document_id):
            return{
                "message": "Document already processed",
                "document_id": document_id
            }
            
        print(f"extracting content from{file.filename}...")
        extracted = extract_pdf_content(file_path)
        
        print(f"chunking document...")
        chunks = chunk_document(extracted, document_id)
        
        print(f"embedding chunks...")
        embedded_chunks = embed_chunks(chunks)
        
        print(f"Storing in ChromaDB")
        success = add_chunks(embedded_chunks)
        
        if not success:
            raise HTTPException(status_code = 500, detail = "Failed to store document")
        
        return{
            "message":"Document processed successfully",
            "document_id": document_id,
            "filename" : file.filename,
            "total_chunks": len(chunks),
            "total_pages" : extracted["total_pages"],
            "metadata" : extracted["metadata"]
        }
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            
@router.get("/")
async def list_documents():
    return{
        "documents" : [],
        "message" : "document listing requires"
    }
    
    
@router.delete("/documents_id")
async def delete_document(documents_id):
    #delete all documents and its chunks
    
    success = delete_document_chunks(documents_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="document not found")
    
    return{
        "message":"document deleted successfully",
        "document_id": documents_id
    }


# Add audio formats to accepted types
ACCEPTED_FORMATS = [".pdf", ".mp3", ".wav", ".m4a", ".mp4"]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Get file extension
    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    # Validate format
    if file_extension not in ACCEPTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}"
        )

    document_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{document_id}{file_extension}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Route to correct parser based on extension
        if file_extension == ".pdf":
            from app.services.ingestion.pdf_parser import extract_pdf_content
            extracted = extract_pdf_content(file_path)

        elif file_extension in [".mp3", ".wav", ".m4a", ".mp4"]:
            from app.services.ingestion.audio_parser import extract_audio_content
            extracted = extract_audio_content(file_path)

        # Rest of pipeline is identical
        chunks = chunk_document(extracted, document_id)
        embedded_chunks = embed_chunks(chunks)
        success = add_chunks(embedded_chunks)

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to store document"
            )

        return {
            "message": "Document processed successfully",
            "document_id": document_id,
            "filename": file.filename,
            "file_type": file_extension,
            "total_chunks": len(chunks),
            "total_pages": extracted["total_pages"],
            "metadata": extracted["metadata"]
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)