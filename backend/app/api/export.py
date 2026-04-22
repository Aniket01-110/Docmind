from fastapi import APIRouter
from app.models.export import ExportPDFRequest, ExportPDFResponse

router = APIRouter(prefix = "/export", tags=["Export"])

@router.post("/pdf")
def export_pdf(request: ExportPDFRequest):
    return{
        "message": "export endpoint ready",
        "title": request.title,
        "document_id":request.document_id
    }