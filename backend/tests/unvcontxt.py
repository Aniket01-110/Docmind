def detect_section_unv(chunk_text: str, document_type: str, groq_client) -> str:
    prompt = f"""You are analyzing a chunk of test from a {document_type} document.
    What section or category does this text belong to ?, reply within 2-4 words max, be specific with document type
    example of different documents
    -Resume : "Work expreince", "technical skills"
    -Legal : "liability caluase", "definitions"
    -Medical : "Patient history", "diagnosis"
    -Financial : "revenue summary","risk factors"
    -Recipe : "ingredients", "preparation steps"
    
    Text to classify:
    {chunk_text[:300]}

Section name (1-3 words only):"""
    
    try :
        response = groq_client.chat.completions.create(model = "llama-3.1-8b-instant", max_tokens=10, messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content.strip()

    except Exception:
        return ""
    
    
    
