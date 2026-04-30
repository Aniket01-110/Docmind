from fastapi import APIRouter, HTTPException
from app.models.chat import ChatQueryRequest
from app.services.rag_engine import query_document
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/query")
async def query(request: ChatQueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail = "Question cannot be empty")
    
    result = query_document(question=request.question,
    document_id=request.document_id)
      
    return{
        "answer" : result["answer"],
        "question" : result["question"],
        "document_id" : result["document_id"],
        "chunks_used" : result["chunks_used"],
        "sources" : result["sources"],
        "similarity_scores" : result["similarity_scores"]
                               
    }
    
@router.get("/history/{document_id}")
async def get_chat_history(document_id:str):
    return{
        "document_id": document_id,
        "messages" : [],
        
    }

