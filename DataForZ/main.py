import asyncio
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Import Google ADK components
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Import your generated agent
from dataforzAgent.agent import root_agent

app = FastAPI(title="DataForZ Agent API", description="API to run Google ADK Agents and connect to Firestore.")

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

# --- 2. Initialize ADK Runner ---
# We use InMemorySessionService to keep track of conversation turns.
# In the future, this can be swapped with a Firestore session service.
session_service = InMemorySessionService()
# Google ADK Runner requires an app_name when providing the agent directly.
agent_runner = Runner(
    app_name="dataforzApp",
    agent=root_agent, 
    session_service=session_service
)
print(f"✅ Google ADK Runner initialized for agent: {root_agent.name}")


# --- API Data Models ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    reply: str
    agent_name: str


# --- API Endpoints ---
@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI is running with Google ADK!"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    This endpoint takes a message from the GUI, sends it to the ADK Agent,
    and returns the AI's response.
    """
    try:
        # Programmatically trigger the ADK agent using the Runner
        response = await agent_runner.run_async(
            input=req.message, 
            session_id=req.session_id
        )
        
        # Depending on ADK version, response might be a string or an object.
        # We handle both just in case:
        reply_text = response
        if not isinstance(response, str):
            if hasattr(response, "text"):
                reply_text = response.text
            elif hasattr(response, "message"):
                reply_text = str(response.message)
            else:
                reply_text = str(response)

        return ChatResponse(
            reply=reply_text,
            agent_name=root_agent.name
        )
        
    except Exception as e:
        print(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
