# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from agent import process

# app = FastAPI()

# class Message(BaseModel):
#     role: str
#     content: str

# class ChatRequest(BaseModel):
#     messages: List[Message]

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.post("/chat")
# def chat(request: ChatRequest):
#     messages = [
#         {"role": m.role, "content": m.content}
#         for m in request.messages
#     ]
#     return process(messages)
from fastapi import FastAPI
from pydantic import BaseModel
from processor import process

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    return process(req.messages)