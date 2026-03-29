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

# --- STRICT PERSONAS & MOODS ---
DISTILL_PROMPT = """
You are an elite Math Olympiad Data Synthesizer. 
TASK: Knowledge Distillation. 
Extract the core math problem, detailed reasoning steps, and the final solution from the user's raw text.

CRITICAL INSTRUCTION: You must output ONLY valid, parsable JSON matching this exact structure:
{
  "agent_message": "String. A conversational response or opinion to show the user in chat.",
  "problem": "String. The extracted math problem.",
  "reasoning_steps": ["String. Step 1", "String. Step 2", "..."],
  "solution": "String. The final definitive answer.",
  "tags": ["distill", "math"]
}
Do not use conversational text or markdown blocks (e.g. no ```json). Your response must be pure raw JSON that can be fed directly to JSON.parse().
"""

SFT_PROMPT = """
You are an elite Math Olympiad Data Synthesizer. 
TASK: Supervised Fine-Tuning Formatting.
The user provides a math problem alongside their unformatted thoughts and a solution. Your job is to formalize it into pristine, mathematically rigorous academic data.

CRITICAL INSTRUCTION: You must output ONLY valid, parsable JSON matching this exact structure:
{
  "agent_message": "String. A conversational response or opinion to show the user in chat.",
  "problem": "String. The formalized math problem.",
  "reasoning_steps": ["String. Formal Step 1", "String. Formal Step 2", "..."],
  "solution": "String. The verified, formal final answer.",
  "tags": ["sft", "math", "academic"]
}
Do not use conversational text or markdown blocks (e.g. no ```json). Your response must be pure raw JSON that can be fed directly to JSON.parse().
"""

async def run_chat_agent(user_message: str, session_id: str, mode: str, document_context: str) -> tuple[str, str]:
    """
    Programmatically trigger the ADK agent. Injects strict JSON structured output rules.
    Returns a tuple: (reply_text, agent_name)
    """
    
    # 1. Select the rigid system instructions based on the Application Mode
    base_instructions = DISTILL_PROMPT if mode == 'distill' else SFT_PROMPT
    
    # 2. Context Engine Logic: If there is an existing JSON document, we are in EDIT loop.
    if document_context and len(document_context.strip()) > 10:
        injected_prompt = (
            f"{base_instructions}\n\n"
            f"--- EXISTING DOCUMENT STATE (Read This Carefully) ---\n"
            f"{document_context}\n\n"
            f"--- USER MODIFICATION COMMAND ---\n"
            f"{user_message}\n\n"
            f"Apply the user's modifications to the EXISTING DOCUMENT. Return the full, updated JSON strictly following the format."
        )
    else:
        # Initial Generation Loop
        injected_prompt = (
            f"{base_instructions}\n\n"
            f"--- USER INPUT ---\n"
            f"{user_message}"
        )
        
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
                    if hasattr(part, "text") and part.text:
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
