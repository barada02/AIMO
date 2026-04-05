from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agent.agent import root_agent

# Initialize the InMemory session tracker
session_service = InMemorySessionService()

# CRITICAL: The 'app_name' parameter is explicitly required when using standard agents
agent_runner = Runner(
    app_name="dataforzApp",
    agent=root_agent, 
    session_service=session_service
)

async def run_chat_agent(user_message: str, session_id: str, mode: str, document_context: str) -> tuple[str, str]:

    injected_prompt = f"Mode: {mode}\nDocument Context: {document_context}\nUser Message: {user_message}"

    events = await agent_runner.run_debug(
        user_messages=injected_prompt, 
        session_id=session_id,
        user_id="ui_user"
    )
    
    reply_text = ""
    for event in events:
        if hasattr(event, "message") and event.message and getattr(event.message, "role", "") == "model":
            content = getattr(event.message, "content", None)
            if content and hasattr(content, "parts"):
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        reply_text += part.text
                        
        elif hasattr(event, "content") and event.content:
            if hasattr(event.content, "parts"):
                for part in event.content.parts:
                    if hasattr(event.content, "text") and event.content.text:
                        reply_text += str(event.content.text)
                    elif hasattr(part, "text") and part.text:
                        reply_text += str(part.text)
                        
        elif hasattr(event, "text") and event.text:
            reply_text += str(event.text)
            
    if not reply_text and events:
         reply_text = "Parsing error: Could not extract text. Raw dump: " + str(events[-1])
         
    # Extreme fallback cleanup: Sometimes Gemini still adds markdown backticks despite instructions.
    clean_text = reply_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    elif clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
         
    return clean_text.strip(), root_agent.name
