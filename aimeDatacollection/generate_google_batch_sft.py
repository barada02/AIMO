import json
import os
import sys

DATAFORGE_AGENT_INSTRUCTION = """You are an expert AIMO Progress Prize dataset creator specialized in generating high-quality Supervised Fine-Tuning (SFT) data for math models.Your task is to convert a given math problem and its solution into a single JSON object that follows the schema below.STRICT RULES:Create only one JSON document per problem. 
    The reasoning must be turned into a clean Chain-of-Thought in the reasoning_steps array.
    Every step that requires calculation must include a code_snippet (Python code using sympy or basic Python) and its actual code_execution_result.
    Make the steps detailed enough so the model learns when and why to call code dynamically during inference.
    Output only the valid JSON. No extra text, no explanations, no markdown.

    JSON SCHEMA (you must follow this exactly):json
    {
    "id": "string (unique, e.g. aimo_sft_math_001)",
    "problem": "string (exact problem statement with LaTeX)",
    "topics": ["array of strings: only algebra, geometry, number_theory, combinatorics"],
    "difficulty": "string (easy | medium | hard)",
    "domain_focus": "string (short description, e.g. algebraic_rewriting + counting_composites_with_distinct_factors)",
    "reasoning_steps": [
    {
      "step": integer (1, 2, 3...),
      "thought": "string (what the model should think/say at this step)",
      "code_snippet": "string (full executable Python code or null)",
      "code_execution_result": "string (exact output of the code or null)",
      "key_insight": "string (the important takeaway after this step)"
    }
  ],
  "target_value": number (the final numerical answer),
  "final_answer": "string (the boxed answer exactly as in the solution, e.g. \\boxed{070})",
  "metadata": {
    "training_type": "tool_integrated_reasoning",
    "purpose": "string (short description of what this example teaches)",
    "verified_with_code": boolean (true or false)
    }
    }
    How to build reasoning_steps:Break the given solution into logical steps.
    For every calculation, create a step with actual Python code and its result.
    Keep thoughts clear, natural, and in first-person style as if the model is thinking.
    End with a final step that states the conclusion.
    Example input will be given as:
    Problem: [problem text]
    Solution: [solution text]Your output must be ONLY the JSON..
    """

def generate_user_prompt(item):
    """Generates the specific user prompt from the problem and its solution."""
    problem = item.get('problem', '')
    solution = item.get('solution', '')
    
    prompt = f"Problem: {problem}\nSolution: {solution}\n"
    return prompt

def main():
    print("--- Generating Google GenAI Batch Job for SFT ---")
    
    dataset_path = os.path.join(os.path.dirname(__file__), 'aimeRawDataCollection.json')
    output_path = os.path.join(os.path.dirname(__file__), 'google_batch_requests_sft.jsonl')
    
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read dataset: {e}")
        return

    # Processing only the first 3 records for testing
    print("Running in TEST mode: Processing only the first 3 records for testing.")
    data = data[:3]

    requests = []
    for i, item in enumerate(data):
        if not item.get('problem'):
            continue
            
        user_prompt = generate_user_prompt(item)
        
        request_id = f"sft-{i+1}"
        
        request_obj = {
            "key": request_id,
            "request": {
                "contents": [
                    {
                        "parts": [{"text": user_prompt}]
                    }
                ],
                "system_instruction": {
                    "parts": [{"text": DATAFORGE_AGENT_INSTRUCTION}]
                },
                "tools": [{"code_execution": {}}],
                "generation_config": {
                    "temperature": 0.7,
                    "response_mime_type": "application/json"
                }
            }
        }
        requests.append(request_obj)

    print(f"Generated {len(requests)} requests.")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for r in requests:
            f.write(json.dumps(r) + '\n')
            
    print(f"Saved to {output_path}")

    # ---------------------------------------------------------
    # UPLOAD AND START BATCH JOB
    # ---------------------------------------------------------
    print("\n--- Connecting to Google GenAI ---")
    try:
        from dotenv import load_dotenv
        from google import genai
        from google.genai import types

        load_dotenv()
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        client = genai.Client(
            api_key=api_key
        )
        
        print(f"Uploading file: {os.path.basename(output_path)} ...")
        uploaded_file = client.files.upload(
            file=output_path,
            config=types.UploadFileConfig(
                display_name='aime-sft-batch', 
                mime_type='application/jsonl'
            )
        )
        print(f"Successfully uploaded file!")
        print(f"File Name/URI: {uploaded_file.name}")
        
        print("\nCreating batch job...")
        file_batch_job = client.batches.create(
            model="gemini-3-flash-preview",
            src=uploaded_file.name,
            config={
                'display_name': "aime-sft-batch-job",
            },
        )
        
        print(f"Created batch job successfully!")
        print(f"Job Name: {file_batch_job.name}")
        print(f"Job State: {file_batch_job.state}")
        print("\nYou can poll the status programmatically by getting the job state.")
        
    except Exception as e:
        print(f"[ERROR] Failed to start Google GenAI batch job: {e}")
        print("\nMake sure you have:")
        print("1. Installed the google-genai library: pip install google-genai")
        print("2. Set your environment variable: GOOGLE_API_KEY='your-api-key'")

if __name__ == "__main__":
    main()
