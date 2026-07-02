# SHL Conversational Assessment Recommender

## Overview

This project implements a conversational AI agent that recommends appropriate SHL Individual Test Solutions based on hiring requirements. The application accepts conversational input, retrieves relevant assessments using semantic search, and returns structured recommendations through a FastAPI service.

The solution follows the requirements specified in the SHL AI Intern Take-Home Assignment.

---

## Features

- Conversational recommendation system
- Clarification for vague hiring requests
- Semantic retrieval using Sentence Transformers and FAISS
- Comparison of SHL assessments
- Recommendation refinement during multi-turn conversations
- Off-topic request handling
- Stateless API design
- FastAPI REST API

---

## Technology Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- BeautifulSoup
- Requests
- Uvicorn

---

## Project Structure

```
SHL_AI_Intern/
│── app.py
│── agent.py
│── retriever.py
│── comparator.py
│── filters.py
│── prompts.py
│── scraper.py
│── requirements.txt
│── vector_db/
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python -m uvicorn app:app --reload
```

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
    "status": "ok"
}
```

---

### Chat Endpoint

```
POST /chat
```

Example Request

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Hiring a Java developer with 4 years of experience."
        }
    ]
}
```

Example Response

```json
{
    "reply": "Here are the recommended SHL assessments.",
    "recommendations": [
        {
            "name": "Java Assessment",
            "url": "https://www.shl.com/...",
            "test_type": "Knowledge"
        }
    ],
    "end_of_conversation": true
}
```

---

## Retrieval Pipeline

1. SHL catalogue is scraped.
2. Text is converted into embeddings.
3. Embeddings are indexed using FAISS.
4. User queries are converted into embeddings.
5. Similar assessments are retrieved using semantic similarity.

---

## Conversation Behaviors

The agent supports:

- Clarification
- Recommendations
- Refinement
- Assessment Comparison
- Off-topic refusal

---

## Future Improvements

- Better ranking model
- Improved intent classification
- Hybrid retrieval
- LLM-assisted explanations
- Larger evaluation dataset

---

## Author

Yogita Aggarwal

MCA (Artificial Intelligence and Machine Learning)

SHL AI Intern Take-Home Assignment