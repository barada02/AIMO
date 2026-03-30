import sys
import os
import uvicorn
import json
from dotenv import load_dotenv

# Automatically load environment variables from the .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Dict, Any
from google.cloud import firestore

# Import our modular agent runner logic
from src.agent_runner.runner import run_chat_agent

app = FastAPI(
    title="DataForZ Agent API", 
    description="API to run ADK Agents and connect to Firestore."
    )

# Mount the UI folder to serve CSS and JS
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "src", "ui")), name="static")
PROJECT_ID = "geminilive-488617"
# --- 1. Initialize Firebase DB ---
try:
    # If testing locally with a credentials file, set the env var automatically
    if os.path.exists("firebase-credentials.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("firebase-credentials.json")
        print("🔧 Configured local development credentials.")

    # Automatically uses Application Default Credentials (ADC) on Cloud Run
    # Locally, it relies on the GOOGLE_APPLICATION_CREDENTIALS env var we just set
    db = firestore.Client(project=PROJECT_ID, database="dataforz-1")
    print("✅ Firestore initialized securely using google-cloud-firestore.")
except Exception as e:
    print(f"⚠️ Warning: Firestore initialization failed. Start without DB? Error: {e}")
    db = None


# --- API Data Models ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    mode: str = "distill"
    document_context: str = ""

class ChatResponse(BaseModel):
    reply: str
    agent_name: str

class CommitRequest(BaseModel):
    collection_name: str = "training_data"
    document_data: Dict[str, Any]

# --- API Endpoints ---
@app.get("/")
def serve_ui():
    """Serves the frontend testing GUI from the modular directory."""
    ui_template = os.path.join(os.path.dirname(__file__), "src", "ui", "index.html")
    if os.path.exists(ui_template):
        return FileResponse(ui_template)
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    Takes a message from the GUI, sends it to the modular ADK Agent Runner,
    and returns the structured data response.
    """
    try:
        reply_text, agent_name = await run_chat_agent(
            user_message=req.message, 
            session_id=req.session_id,
            mode=req.mode,
            document_context=req.document_context
        )
        return ChatResponse(
            reply=reply_text,
            agent_name=agent_name
        )
    except Exception as e:
        print(f"Error executing agent runner logic: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/commit")
async def commit_endpoint(req: CommitRequest):
    """
    Takes a validated JSON payload from the UI editor and securely commits it to Firestore.
    Runs in a threadpool to prevent blocking the async FastAPI event loop.
    """
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized. Check firebase-credentials.json")
    
    try:
        def push_to_db():
            # Inject a secure backend timestamp to track when the data was generated
            req.document_data['timestamp'] = firestore.SERVER_TIMESTAMP
            
            # Add new document to the targeted collection
            doc_ref = db.collection(req.collection_name).add(req.document_data)
            return doc_ref[1].id
            
        # Execute the blocking Firestore SDK operation inside a thread pool
        doc_id = await run_in_threadpool(push_to_db)
        
        return {"status": "success", "doc_id": doc_id}
        
    except Exception as e:
        print(f"Database error during commit: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Changed from 0.0.0.0 to localhost
        port=8080,
        reload=True,
        log_level="info"
    )