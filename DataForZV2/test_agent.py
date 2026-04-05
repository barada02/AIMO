import asyncio
import sys
import os

# Add the agent module's directory to sys.path so 'from agent.agent import root_agent' works
base_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.join(base_dir, 'src', 'Agents', 'dataforge_agent')
sys.path.insert(0, agent_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(agent_dir, '.env'))

from src.Agents.dataforge_agent.runner import run_chat_agent

async def test_agent():
    user_message = """Problem: Find the value of x if 2x + 3 = 7.
Solution: Subtract 3 from both sides to get 2x = 4. Divide by 2 to get x = 2."""
    session_id = "test-session-123"
    mode = "SFT Generation"
    document_context = "Testing context"
    
    print(f"Sending message to agent...")
    try:
        response, agent_name = await run_chat_agent(user_message, session_id, mode, document_context)
        print(f"\nModel completed.")
        print(f"Agent Name: {agent_name}")
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent())
