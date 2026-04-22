from fastapi import APIRouter
from app.models.user import UserSignupRequest, UserLoginRequest, AuthResponse

#APIRouter () creates a mini router for Auth feature 
#prefix means   all routes start with /auth



router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/Signup")
def signup(request: UserSignupRequest):
    
    return {
        "message": "signup endpoint ready",
        "email": request.email,
        "name": request.name
    }
    
    
@router.post("/Login")
def login(request: UserLoginRequest):
    return{
        "message": "login endpoint ready",
        "email": request.email
    }
    