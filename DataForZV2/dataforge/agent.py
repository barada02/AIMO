from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',

    code_executor=BuiltInCodeExecutor(),

    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return the final numerical result and code in json.
    """,
    description="Executes Python code to perform calculations.",
)
