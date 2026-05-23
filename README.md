# 🧠 DocMind — Chat With Your Documents

> A multimodal AI-powered RAG system that lets users upload
> any document and have intelligent conversations with it.

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/License-MIT-purple)
## 🛠️ Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### AI/ML
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-FF6B35?style=for-the-badge&logo=langchain&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

### Database & Auth
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=for-the-badge&logo=databricks&logoColor=white)

### Deployment
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

---

## 🚀 What is DocMind?

DocMind is a full-stack AI application where users can:

- 📄 Upload **PDFs, images, audio files, and CSVs**
- 🤖 Ask questions and get **AI-powered answers** grounded
  in their documents
- 💬 Maintain **persistent chat history** per user
- 📝 **Auto-generate PDFs** from conversations
- 🔐 Secure **login and signup** with per-user data isolation

Built with industry-standard architecture — clean separation
of concerns, proper environment management, and
production-ready folder structure.

---

## 🧱 Tech Stack

| Layer               | Technology             |
| ------------------- | ---------------------- |
| LLM                 | Claude API (Anthropic) |
| Embeddings          | sentence-transformers  |
| Vector DB           | ChromaDB               |
| Audio → Text        | OpenAI Whisper         |
| Image Understanding | Claude Vision API      |
| PDF Parsing         | PyMuPDF + pdfplumber   |
| Backend             | FastAPI (Python)       |
| Frontend            | React.js + TailwindCSS |
| Auth + Database     | Supabase               |
| PDF Generation      | ReportLab              |
| Backend Deploy      | Render                 |
| Frontend Deploy     | Vercel                 |

---

## 📁 Project Structure

docmind/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── config.py # Environment variables
│ │ ├── api/ # Route handlers
│ │ ├── services/ # Business logic
│ │ │ └── ingestion/ # File parsers
│ │ ├── models/ # Pydantic data models
│ │ └── middleware/ # Auth guards
│ ├── tests/
│ └── .env # Secrets (never committed)
├── frontend/
│ └── src/
│ ├── components/
│ ├── context/
│ ├── pages/
│ └── services/
└── README.md

---
