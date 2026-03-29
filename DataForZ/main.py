import asyncio
import sys
import os
from dotenv import load_dotenv
# Automatically load environment variables from the .env file
load_dotenv()

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


from fastapi.responses import FileResponse

# --- API Endpoints ---
@app.get("/")
def serve_ui():
    """Serves the frontend testing GUI"""
    return FileResponse("index.html")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """
    This endpoint takes a message from the GUI, sends it to the ADK Agent,
    and returns the AI's response.
    """
    try:
        # Programmatically trigger the ADK agent using run_debug
        # run_debug is perfect here as it accepts plain strings easily
        events = await agent_runner.run_debug(
            user_messages=req.message, 
            session_id=req.session_id,
            user_id="ui_user"
        )
        
        reply_text = ""
        # ADK returns a list of Events. We extract the text from the model's response.
        for event in events:
            # Different ADK versions nest the text differently
            
            # 1. Strategy A: Event wraps a "message"
            if hasattr(event, "message") and event.message and getattr(event.message, "role", "") == "model":
                content = getattr(event.message, "content", None)
                if content and hasattr(content, "parts"):
                    for part in content.parts:
                        if hasattr(part, "text") and part.text:
                            reply_text += part.text
                            
            # 2. Strategy B: Event itself is the message (matching the dump you saw)
            elif hasattr(event, "content") and event.content:
                if hasattr(event.content, "parts"):
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            reply_text += str(part.text)
                            
            # 3. Strategy C: Event just has flat text
            elif hasattr(event, "text") and event.text:
                reply_text += str(event.text)
                
        if not reply_text and events:
             # Fallback if the object schema is totally unexpected
             reply_text = "Parsing error: Could not extract text. Raw dump: " + str(events[-1])

        return ChatResponse(
            reply=reply_text,
            agent_name=root_agent.name
        )
        
    except Exception as e:
        print(f"Error running agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
