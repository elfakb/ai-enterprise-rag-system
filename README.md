# 🦙 **Enterprise Knowledge Base (RAG)**

An AI-powered enterprise system that understands organizational documents and makes them searchable.

---

## **Overview**

This project is a **RAG-based enterprise knowledge application** that processes internal technical documents and enables users to query them through natural language.
Using an LLM + vector database, it provides accurate, fast, and context-aware responses.

---

## **Problem**

Employees in large organizations are required to review hundreds of pages of documentation daily.
Information is scattered, difficult to search, and time-consuming to access.
There is **no single source of truth → productivity decreases.**

---

## **Solution**

This system collects all internal documents, processes them, and stores them in a vector database.
When a user asks a natural-language question, the system:

1. Retrieves the most relevant document chunks,
2. Sends them to the LLM,
3. Produces a grounded, reliable answer.

---

## **Architecture**

* LangChain pipeline
* Embedding Model: `all-MiniLM-L6-v2`
* LLM: Llama
* Vector DB: ChromaDB
* Containerization: Docker
* Frontend: Streamlit

---

## 🛠 **Tech Stack**

* **Python 3.10+**
* **FastAPI**
* **LangChain**
* **ChromaDB / Pinecone**
* **HuggingFace Embeddings**
* **Docker**
* **Streamlit** (optional UI)

---

## ▶️ **Run Locally**

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ run llama

```bash
run ollama : ollama run llama3
```

### 3️⃣ Start app

```bash
streamlit run app.py
```

### 4️⃣ Add new documents


---

### App

<div align="center">
    <img src="images/image.png" width="45%" alt="Upload PDF">
    <img src="images/image copy.png" width="45%" alt="Question">
    <img src="images/image copy 2.png" width="45%" alt="Answer">
    <img src="images/image copy 3.png" width="45%" alt="Source Attribution">
</div>

