# 🧠 DocMind — Chat With Your Documents

> A multimodal AI-powered RAG system that lets users upload
> any document and have intelligent conversations with it.

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/License-MIT-purple)

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
