import os
from typing import List, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Pydantic models for structured output
class VariantCandidate(BaseModel):
    problem: str = Field(description="The new problem statement.")
    solution: str = Field(description="The brief foundational solution to this problem.")
    reasoning: str = Field(description="How this links to the original problem statement and solution, and why it was created.")

class VariantList(BaseModel):
    variants: List[VariantCandidate] = Field(description="List of 7 generated variant problems.")

class ValidationResult(BaseModel):
    is_valid: bool = Field(description="True if the generated problem is mathematically sound and the solution is correct. False otherwise.")
    corrected_problem: str = Field(description="If invalid, provide the corrected and mathematically sound problem. If valid, return the original problem.")
    corrected_solution: str = Field(description="If invalid, provide the corrected solution. If valid, return the original solution.")

# State definition
class GraphState(TypedDict):
    original_problem: str
    original_solution: str
    original_tags: List[str]
    variants: List[dict]

# Nodes
def generate_node(state: GraphState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    prompt = (
        f"You are an elite Math Olympiad Problem Setter.\n"
        f"First, internally analyze the core mathematical concepts of the following problem:\n"
        f"Original Problem: {state['original_problem']}\n"
        f"Original Solution: {state['original_solution']}\n\n"
        f"Next, mutate the problem to create exactly 7 entirely new, distinctly different but conceptually related math problems.\n"
        f"Ensure they vary in context or numbers but remain structurally similar."
    )
    
    # Force structured output returning a list of Variants
    llm_structured = llm.with_structured_output(VariantList)
    response = llm_structured.invoke(prompt)
    
    try:
        variants = [v.dict() for v in response.variants]
    except Exception as e:
        variants = []
    
    return {"variants": variants}

def validate_node(state: GraphState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    llm_structured = llm.with_structured_output(ValidationResult)
    
    validated_variants = []
    for variant in state.get('variants', []):
        prompt = (
            f"You are an expert Math Validator.\n"
            f"Original Problem: {state['original_problem']}\n"
            f"Original Solution: {state['original_solution']}\n\n"
            f"Generated Variant Problem: {variant['problem']}\n"
            f"Generated Variant Solution: {variant['solution']}\n"
            f"Variant Reasoning: {variant['reasoning']}\n\n"
            f"Check if the Generated Variant Problem is logically sound, mathematically correct, and the Generated Variant Solution correctly solves it.\n"
            f"If it is wrong, CORRECT IT by outputting a mathematically sound problem and solution. If it's correct, just output it as-is."
        )
        try:
            result = llm_structured.invoke(prompt)
            # Update the variant with the verified/corrected problem and solution
            variant['problem'] = result.corrected_problem
            variant['solution'] = result.corrected_solution
            # Append tags
            variant['tags'] = state.get('original_tags', []) + ['variant']
            validated_variants.append(variant)
        except Exception as e:
            # If the validator fails to parse, we might still want to pass the uncorrected version or drop it.
            # We will drop it to be safe and ensure only high-quality data remains.
            pass

    return {"variants": validated_variants}

# Build Graph
builder = StateGraph(GraphState)
builder.add_node("generate", generate_node)
builder.add_node("validate", validate_node)

builder.add_edge("generate", "validate")
builder.add_edge("validate", END)

builder.set_entry_point("generate")

variant_runner = builder.compile()

def generate_variants_graph(problem: str, solution: str, tags: List[str]) -> List[dict]:
    initial_state = {
        "original_problem": problem,
        "original_solution": solution,
        "original_tags": tags,
        "variants": []
    }
    final_state = variant_runner.invoke(initial_state)
    return final_state["variants"]
