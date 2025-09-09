# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vertex_client import generate_response
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="MannMitra Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    text: str

class MoodRequest(BaseModel):
    user_id: str
    mood: str  # e.g., "happy", "anxious"

# Simple in-memory store for prototype (replace with Firestore/Firebase in prod)
db = {"mood_logs": {} , "chats": {}}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # generate_response calls Vertex AI if configured, else returns mock
        ai_text = generate_response(req.text, user_id=req.user_id)
        # store chat
        db["chats"].setdefault(req.user_id, []).append({"user": req.text, "ai": ai_text})
        return {"reply": ai_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mood")
def mood(req: MoodRequest):
    db["mood_logs"].setdefault(req.user_id, []).append({"mood": req.mood})
    return {"status": "saved", "counts": len(db["mood_logs"][req.user_id])}

@app.get("/mood_trend/{user_id}")
def mood_trend(user_id: str):
    logs = db["mood_logs"].get(user_id, [])
    return {"logs": logs}
