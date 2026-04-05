from google.adk.agents.llm_agent import Agent
from google.adk.tools import BuiltInCodeExecutor

GEMINI_MODEL = 'gemini-2.5-pro'
AGENT_NAME = 'code_agent'
FLASH_MODEL = 'gemini-2.5-flash'

code_agent = Agent(
    name=AGENT_NAME,
    model=GEMINI_MODEL,
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations and logically verify sub-steps.",
)

validator_agent = Agent(
    name='validator_agent',
    model=GEMINI_MODEL,
    tools=[code_agent],
    description='A logical math reviewer that relies on writing code to verify calculations and correct logical steps.',
    instruction="""You are a rigorous Math Validator. 
    You will receive generated reasoning steps (Tree of Thoughts) for a math problem. 
    Your strict job is to meticulously verify the logical steps and math accuracy. 
    You MUST delegate mathematical confirmation to the `code_agent` by providing it test scripts or calculation queries. 
    If you detect an inaccuracy in the reasoning steps, mathematically fix it. If the reasoning is too brief, expand it logically. 
    Return your completely validated reasoning.""",
)

generator_agent = Agent(
    name='generator_agent',
    model=GEMINI_MODEL,
    tools=[validator_agent],
    description='Generates structured problem data, CoT reasoning, and assigns semantic math tags.',
    instruction="""You are an elite Math Olympiad Data Synthesizer. 
    Based on the provided problem and solution pair, you must generate a highly detailed, structured Chain-of-Thought reasoning path. 
    Once you draft the reasoning, you MUST hand it off to the `validator_agent` so it can be verified for logical consistency via executed code. 
    Once it's validated, merge everything into the strictly required JSON format, including generating accurate topical tags (e.g., 'algebra', 'geometry').""",
)

# The root agent that the Runner attaches to, acting as the entry point
root_agent = generator_agent
