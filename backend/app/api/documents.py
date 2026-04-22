from fastapi import     APIRouter, UploadFile, File
from app.models.Document import DocumentResponse

router = APIRouter(prefix = "/documents", tags=["Documents"])


@router.get("/")
def list_documents():
    return{
        "documents": [],
        "message": "document endpoint ready"
    }
    
@router.post("/upload") #UploadFile is Fastapis built in type for file uploads
#File(...) means File is required
def upload_document(file: UploadFile = File(...)):
    return{
        "filename": file.filename,
        "message": "documents endpoint ready"
    }

