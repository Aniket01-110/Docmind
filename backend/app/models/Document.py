from pydantic import BaseModel
from typing import Optional  #Optional marks that field is not required, Without this every field is by default required
from enum import Enum

class DocumentType(Enum): #Enum means Enumeration is a way to define set of allowed values, User can choose document from below these choices
    PDF = "pdf"
    AUDIO = "audio"
    IMAGE = "image"
    CSV = "csv"
    
    
#REQUEST MODEL

class DocumentUploadRequest(BaseModel):
    filename: str
    document_type: DocumentType
    user_id : str
    
    
class DocumentResponse(BaseModel):
    id : str
    filename : str
    status : str
    user_id : str
    created_at : str
    
    
#BaseModel is the parent class From Pydantic it helps to provide Validation , type checking , JSON conversion 

#EmailStr  -> pydantic type that checks if a string is valid email format 


 
    