from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor
from src.Agents.prompts import DATAFORGE_AGENT_INSTRUCTION

root_agent = Agent(
    model='gemini-3.1-flash-lite-preview',
    name='root_agent',

    code_executor=BuiltInCodeExecutor(),

    instruction=DATAFORGE_AGENT_INSTRUCTION,

    description="Executes Python code to perform calculations.",
)
