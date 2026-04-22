from pydantic import BaseModel, EmailStr
from typing import Optional

#REQUEST models - Data coming into my API

class UserSignupRequest(BaseModel):
    name : str
    email : EmailStr
    password : str
    
class UserLoginRequest(BaseModel):
    email : EmailStr
    password : str
    
    
#RESPONSE models - data going out from API as an response

class UserResponse(BaseModel): #clearly user response to frontend shouldnt contain the password of the user 
    id : str
    name : str
    email : EmailStr
    
class AuthResponse(BaseModel):
    access_token : str
    token_type : str
    user : UserResponse