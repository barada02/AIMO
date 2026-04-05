import json
import os
import sys
from google import genai
from google.genai import types

# The instruction from DataForZV2/src/Agents/prompts.py
VERIANT_AGENT_INSTRUCTION = """You are an expert AIMO Progress Prize dataset creator. Your objective is to generate high-quality, diverse problem variants from any given original math problem and its multiple solutions.

Core rules (never break these):
1. **Analyze First**: Silently analyze the original problem and ALL provided solutions to identify the core mathematical concepts, sub-problems, and the variety of solving techniques.
2. **Inspiration**: All variants must be deeply inspired by the original problem and its solutions. You can explore a sub-problem, alter the scenario, change boundaries, or increase the difficulty.
3. **Strict AIMO Format**: The ultimate final answer for EVERY variant problem MUST be a single integer between 0 and 99999. This is an absolute competition constraint. Do not produce problems with answers outside this range, negative answers, or fractional answers.
4. **Quality & Correctness**: Do not generate sloppy, useless, or "garbage" problems. For each variant, you must rigorously self-check the logic of the generated solution to ensure it is mathematically sound, factually correct, and solvable.
5. **Diversity**: Generate 8 to 12 diverse variants — do not repeat the same type of change.

Allowed ways to create variants (use a mix of these):
- Change the upper limit / bound.
- Add mild extra constraints (e.g., a < b, a and b coprime, both odd, a + b even, etc.)
- Rewrite the problem in a completely different context or change variable names.
- Extract a sub-problem from the original and ask a harder version of it.       
- Ask for a related count or property that relies on the original insight.      
- Slightly modify the expression or setup while preserving the mathematical heart of the problem.

Output format:
Output ONLY a valid JSON object with this exact structure. Nothing else.        
```json
{
  "original_problem_summary": "1-sentence summary of original problem",
  "variants": [
    {
      "variant_id": "var_001",
      "problem": "the new full problem statement (use LaTeX for math)",
      "solution": "the complete, correct, clearly written solution in plain text. Always end with the final answer as \\boxed{number} where number is between 0 and 99999.",
      "variant_reasoning": "2-3 sentence explanation of how this variant was inspired by the original and why it is a valuable math problem."
    }
  ]
}
```

Input will be given as:
Problem
[problem text]
Solutions
[solution 1 text]
...
[solution N text]

Critically analyze the problem and solutions, self-verify your mathematical foundations, and generate valuable AIMO-style variants. Output only the JSON.
"""

def generate_user_prompt(item):
    """Generates the specific user prompt from the problem and its solutions."""
    problem = item.get('problem', '')
    
    # Extract all solutions available for this problem
    solution_keys = [k for k in item.keys() if k.startswith('solution')]
    
    prompt = f"Problem\n{problem}\n\nSolutions\n"
    for i, key in enumerate(solution_keys, 1):
        prompt += f"[{key.capitalize()}]\n{item[key]}\n\n"
        
    return prompt

def main():
    print("--- Generating Google GenAI Batch Job ---")
    
    dataset_path = os.path.join(os.path.dirname(__file__), 'aime_dataset.json')
    output_path = os.path.join(os.path.dirname(__file__), 'google_batch_requests.jsonl')
    
    # Check if user wants a full run or just a test
    is_test = True
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        is_test = False
        
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read dataset: {e}")
        return

    # For testing, we'll just process the first 3 documents
    if is_test:
        print("Running in TEST mode: Processing only the first 3 records for testing.")
        print("To process the full dataset, run: python generate_google_batch.py --full")
        data = data[:3]
    else:
        print(f"Running in FULL mode: Processing all {len(data)} records.")

    requests = []
    for item in data:
        if not item.get('problem'):
            continue
            
        user_prompt = generate_user_prompt(item)
        
        # Using year-set-number or year-number as the tracking key
        year = str(item.get('year', 'unknown'))
        set_name = str(item.get('set', '')).strip()
        prob_num = str(item.get('problem_number', 'unknown'))
        
        if set_name:
            custom_key = f"{year}-{set_name}-{prob_num}".replace(" ", "_")
        else:
            custom_key = f"{year}-{prob_num}".replace(" ", "_")
        
        # Build the exact JSON required for Google GenAI Batch API
        request_obj = {
            "key": custom_key,
            "request": {
                "contents": [
                    {
                        "parts": [{"text": user_prompt}]
                    }
                ],
                "config": {
                    "system_instruction": {
                        "parts": [{"text": VERIANT_AGENT_INSTRUCTION}]
                    },
                    "temperature": 0.7
                }
            }
        }
        requests.append(request_obj)
        
    # Write the single inline JSON object to the JSONL file
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for req in requests:
            out_f.write(json.dumps(req) + '\n')

    print(f"\nSuccessfully generated batch request file at:\n{output_path}")
    print(f"Total requests prepared: {len(requests)}")
    
    # ---------------------------------------------------------
    # UPLOAD AND START BATCH JOB
    # ---------------------------------------------------------
    print("\n--- Connecting to Google GenAI ---")
    try:
        # Note: Set GOOGLE_API_KEY environment variable before running
        client = genai.Client()
        
        print(f"Uploading file: {os.path.basename(output_path)} ...")
        uploaded_file = client.files.upload(
            file=output_path,
            config=types.UploadFileConfig(
                display_name='aime-variants-batch', 
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
                'display_name': "aime-variants-batch-job",
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
        print("2. Set your environment variable: $env:GOOGLE_API_KEY='your-api-key'")

if __name__ == "__main__":
    main()
