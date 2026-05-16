from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.config import GROQ_API_KEY

#LOADING model at once on model level

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)

#Custom prompt

PROMPT_TEMPLATE = """You are DocMind, an intelligent
document assistant. Answer based ONLY on the context.
If answer not in context say so clearly.

Context:
{context}

Question: {question}

Answer:"""
prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

#Langchain RAG PIPELINE

def langchain_ingest_pdf(file_path: str) -> Chroma:
    
    #loading pdf
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    
    #spliting extracted text  into chunks 
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ".", " ",""])
    chunks = splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore

def langchain_query(vectorstore: Chroma, question: str) -> dict:
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt":prompt})
    
    result = chain.invoke({"query": question})
    return {
        "answer": result["result"],
        "sources": [
            doc.page_content[:200]
            for doc in result["source_documents"]
        ]
    }
    


def langchain_full_pipeline(
    pdf_path: str,
    question: str
) -> dict:

    print(" Loading PDF with LangChain...")
    vectorstore = langchain_ingest_pdf(pdf_path)

    print("Querying with LangChain chain...")
    result = langchain_query(vectorstore, question)

    return result