from fastapi import APIRouter
from app.models.chat import ChatQueryRequest, ChatQueryResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/query")
def query_document(request: ChatQueryRequest):
    return{
        "answer": "chat endpoint ready",
        "question": request.question,
        "document_id": request.document_id
    }

@router.get("/history.{document_id}")
def get_chat_history(document_id : str):
    return{
        "document_id": document_id,
        "messages": []
    }