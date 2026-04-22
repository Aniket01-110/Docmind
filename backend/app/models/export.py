from pydantic import BaseModel
from typing import Optional

#Request model
class ExportPDFRequest(BaseModel):
    document_id: str
    chat_history_id: str
    title: Optional[str] = "My Export"
    
    
#Response Model

class ExportPDFResponse(BaseModel):
    file_url: str
    filename: str
    created_at: str
    
    