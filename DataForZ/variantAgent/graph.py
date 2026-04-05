import os
from typing import List, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Pydantic models for structured output
class VariantCandidate(BaseModel):
    problem: str = Field(description="The mutated problem statement.")
    solution: str = Field(description="The solution to this variant.")
    reasoning: str = Field(description="How this links to the original problem statement and solutions, and why it was decided to create it.")

class VariantList(BaseModel):
    variants: List[VariantCandidate] = Field(description="List of 7 generated variant problems.")

class ValidationResult(BaseModel):
    is_valid: bool = Field(description="True if the generated problem is mathematically sound and the solution is correct. False otherwise.")
    correction: str = Field(description="If invalid, provide reason. If valid, leave empty.")

# State definition
class GraphState(TypedDict):
    original_problem: str
    original_solution: str
    original_tags: List[str]
    analysis: str
    candidates: List[dict]
    variants: List[dict]

# Nodes
def analyze_node(state: GraphState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    prompt = f"Analyze the core mathematical concepts and skeleton of the following problem:\nProblem: {state['original_problem']}\nSolution: {state['original_solution']}\n\nProvide a concise analysis of the core structure and what parameters can be mutated."
    response = llm.invoke(prompt)
    return {"analysis": response.content}

def mutate_node(state: GraphState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    prompt = (
        f"You are an elite Math Olympiad Problem Setter.\n"
        f"Based on the original problem and this analysis:\n\n"
        f"Original Problem: {state['original_problem']}\n"
        f"Original Solution: {state['original_solution']}\n"
        f"Analysis: {state['analysis']}\n\n"
        f"Mutate the problem to create 7 entirely new, distinctly different but conceptually related math problems. "
    )
    
    # Force structured output returning a list of Variants
    llm_structured = llm.with_structured_output(VariantList)
    response = llm_structured.invoke(prompt)
    
    # Convert back to regular list of dicts for the graph state
    try:
        candidate_dicts = [v.dict() for v in response.variants]
    except Exception as e:
        candidate_dicts = []
    return {"candidates": candidate_dicts}

def validate_node(state: GraphState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    llm_structured = llm.with_structured_output(ValidationResult)
    
    valid_variants = []
    for candidate in state.get('candidates', []):
        prompt = (
            f"You are an expert Math Validator.\n"
            f"Original Problem: {state['original_problem']}\n"
            f"Original Solution: {state['original_solution']}\n\n"
            f"Generated Variant Problem: {candidate['problem']}\n"
            f"Generated Variant Solution: {candidate['solution']}\n"
            f"Variant Reasoning: {candidate['reasoning']}\n\n"
            f"Check if the Generated Variant Problem is logically sound, mathematically correct, and the Generated Variant Solution correctly solves it."
        )
        try:
            result = llm_structured.invoke(prompt)
            if result.is_valid:
                # Merge original tags directly for UI compatibility
                candidate['tags'] = state.get('original_tags', []) + ['variant']
                valid_variants.append(candidate)
        except Exception as e:
            pass # Skip invalid

    return {"variants": valid_variants}

# Build Graph
builder = StateGraph(GraphState)
builder.add_node("analyze", analyze_node)
builder.add_node("mutate", mutate_node)
builder.add_node("validate", validate_node)

builder.add_edge("analyze", "mutate")
builder.add_edge("mutate", "validate")
builder.add_edge("validate", END)

builder.set_entry_point("analyze")

variant_runner = builder.compile()

def generate_variants_graph(problem: str, solution: str, tags: List[str]) -> List[dict]:
    initial_state = {
        "original_problem": problem,
        "original_solution": solution,
        "original_tags": tags,
        "analysis": "",
        "candidates": [],
        "variants": []
    }
    final_state = variant_runner.invoke(initial_state)
    return final_state["variants"]
