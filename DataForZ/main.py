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
    parent_id: str = None
    generation_type: str = "original"

class VariantRequest(BaseModel):
    problem: str
    solution: str
    tags: list = []

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
            tags = req.document_data.pop('tags', [])
            
            pure_data = {
                "problem": req.document_data.get('problem', ''),
                "reasoning_steps": req.document_data.get('reasoning_steps', []),
                "solution": req.document_data.get('solution', '')
            }
            
            doc_ref = db.collection("training_data").document()
            doc_id = doc_ref.id
            doc_ref.set(pure_data)
            
            metadata = {
                "tags": tags,
                "type": req.generation_type,
                "parent_id": req.parent_id,
                "timestamp": firestore.SERVER_TIMESTAMP
            }
            db.collection("training_metadata").document(doc_id).set(metadata)
            
            return doc_id
            
        doc_id = await run_in_threadpool(push_to_db)
        return {"status": "success", "doc_id": doc_id}
        
    except Exception as e:
        print(f"Database error during commit: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/database/data")
async def get_database_data():
    """
    Fetches the latest metadata and pure data from Firestore.
    """
    if not db:
        raise HTTPException(status_code=500, detail="Database not connected.")
    try:
        def fetch_db():
            # Get latest 25 documents sorted by generation time
            meta_docs = db.collection("training_metadata").order_by(
                "timestamp", direction=firestore.Query.DESCENDING
            ).limit(25).stream()
            
            results = []
            for doc in meta_docs:
                meta = doc.to_dict()
                doc_id = doc.id
                
                # Fetch pure data 
                pure_data_snap = db.collection("training_data").document(doc_id).get()
                pure_data = pure_data_snap.to_dict() if pure_data_snap.exists else {}
                
                combined = {**meta, **pure_data, "id": doc_id}
                
                if 'timestamp' in combined and combined['timestamp']:
                    combined['timestamp'] = str(combined['timestamp'])
                results.append(combined)
                
            return results
        
        results = await run_in_threadpool(fetch_db)
        return {"status": "success", "count": len(results), "data": results}
    except Exception as e:
        print(f"Database error during fetch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/variants/generate")
async def generate_variants_endpoint(req: VariantRequest):
    """
    Passes the problem and solution to LangGraph to generate variants.
    """
    try:
        def run_graph():
            from variantAgent import generate_variants_graph
            return generate_variants_graph(req.problem, req.solution, req.tags)
            
        variants = await run_in_threadpool(run_graph)
        return {"status": "success", "variants": variants}
    except Exception as e:
        print(f"Error generating variants: {e}")
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