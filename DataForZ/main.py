import sys
import os
from dotenv import load_dotenv

# Automatically load environment variables from the .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Import our modular agent runner logic
from src.agent_runner.runner import run_chat_agent

app = FastAPI(title="DataForZ Agent API", description="API to run ADK Agents and connect to Firestore.")

# --- 1. Initialize Firebase DB ---
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-credentials.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully in FastAPI.")
except Exception as e:
    print(f"⚠️ Warning: Firebase initialization failed. Start without DB? Error: {e}")
    db = None


# --- API Data Models ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    reply: str
    agent_name: str


# --- API Endpoints ---
@app.get("/")
def serve_ui():
    """Serves the frontend testing GUI from the modular directory."""
    # Build a cross-platform path to src/ui/index.html
    ui_template = os.path.join(os.path.dirname(__file__), "src", "ui", "index.html")
    if os.path.exists(ui_template):
        return FileResponse(ui_template)
    # Backward compatibility fallback
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    Takes a message from the GUI, sends it to the modular ADK Agent Runner,
    and returns the AI's response.
    """
    try:
        # Programmatically trigger the ADK agent using our modular function
        reply_text, agent_name = await run_chat_agent(req.message, req.session_id)

        return ChatResponse(
            reply=reply_text,
            agent_name=agent_name
        )
        
    except Exception as e:
        print(f"Error executing agent runner logic: {e}")
        raise HTTPException(status_code=500, detail=str(e))
