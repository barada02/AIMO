import os
import sys

# Ensure Python can import 'dataforzAgent' from the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dataforzAgent.agent import root_agent

# Initialize the InMemory session tracker
session_service = InMemorySessionService()

# CRITICAL: The 'app_name' parameter is explicitly required when using standard agents
agent_runner = Runner(
    app_name="dataforzApp",
    agent=root_agent, 
    session_service=session_service
)
print(f"✅ Executing from src/agent_runner/runner.py | Runner initialized for: {root_agent.name}")

async def run_chat_agent(user_message: str, session_id: str) -> tuple[str, str]:
    """
    Programmatically trigger the ADK agent using run_debug.
    Returns a tuple: (reply_text, agent_name)
    """
    events = await agent_runner.run_debug(
        user_messages=user_message, 
        session_id=session_id,
        user_id="ui_user"
    )
    
    reply_text = ""
    for event in events:
        # 1. Strategy A: Event wraps a "message"
        if hasattr(event, "message") and event.message and getattr(event.message, "role", "") == "model":
            content = getattr(event.message, "content", None)
            if content and hasattr(content, "parts"):
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        reply_text += part.text
                        
        # 2. Strategy B: Event itself is the message data object
        elif hasattr(event, "content") and event.content:
            if hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        reply_text += str(part.text)
                        
        # 3. Strategy C: Event just has flat text
        elif hasattr(event, "text") and event.text:
            reply_text += str(event.text)
            
    if not reply_text and events:
         # Fallback
         reply_text = "Parsing error: Could not extract text. Raw dump: " + str(events[-1])
         
    return reply_text, root_agent.name
