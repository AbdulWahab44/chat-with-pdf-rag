# 📄 Chat with Your PDFs (RAG App)

## 🚀 Overview

This project is an AI-powered application that allows users to chat with their PDF documents. It uses a Retrieval-Augmented Generation (RAG) pipeline to extract relevant information and generate accurate answers based on the document content.

---

## 🧠 Features

* Upload and read PDF documents
* Ask questions in natural language
* Context-aware answers using AI
* Fast retrieval using vector database (FAISS)
* Simple and interactive UI with Streamlit

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* FAISS
* OpenAI / HuggingFace (for embeddings & LLM)
* PyPDF

---

## ⚙️ How It Works

1. Load PDF and extract text
2. Split text into smaller chunks
3. Convert text into embeddings
4. Store embeddings in FAISS vector database
5. Retrieve relevant chunks based on user query
6. Generate answer using LLM

---

## 📦 Installation

```bash
git clone https://github.com/AbdulWahab44/chat-with-pdf-rag.git
cd chat-with-pdf-rag
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
chat-with-pdf-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
└── utils/
```

---

## 🌍 Future Improvements

* Chat history (memory)
* Multiple PDF support
* Better UI (chat-style interface)
* Deployment on cloud
* Use of local LLMs (no API cost)

---

## 🤝 Contributing

Feel free to fork this repo and improve it.

---

## ⭐ Acknowledgment

This project is built for learning and exploring RAG-based AI applications.
