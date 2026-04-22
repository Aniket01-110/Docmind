from pydantic import BaseModel
from typing import Optional, List
#List tells pydantic that its a List of something

#Request model
class ChatQueryRequest(BaseModel):
    question : str
    document_id : str
    user_id : str
    
    
#REQUEST MODELS
class MessageResponse(BaseModel):
    
    role : str
    content : str
    created_at : str
    
class ChatQueryResponse(BaseModel):
    answer : str
    document_id : str
    sources : List[str]
    
    
class ChatHistoryResponse(BaseModel):
    document_id : str
    messsages : List[MessageResponse]
    
    


    