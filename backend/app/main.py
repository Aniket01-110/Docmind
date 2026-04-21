from fastapi import FastAPI
from app.config import APP_NAME #go into app folder then find config file and grab APP_NAME

app = FastAPI(
    title=APP_NAME,
    description="Multimodal RAG system - chat with your document",
    version="0.1.0"
) #app object , it creates entire web application in one object called app

@app.get("/") #this is the decorator it wraps the fucntion below it, when someone makes a GET request to "/" , run the function directly below me that what this wrapper is
def root():
    return{
        "app":APP_NAME,
        "status":"running",
        "message": "Welcome to Docmind API"
    }

@app.get("/health")
def health_check():
    return{"status":"ok"}

