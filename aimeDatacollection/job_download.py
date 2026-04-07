import os
import json
from dotenv import load_dotenv
from google import genai

# 1. Setup Environment
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit()

client = genai.Client(api_key=api_key)

# Your specific Job ID
JOB_NAME = "batches/3hrmrdf7oeq1gu4ebvvtb704l50aw6z5qzwz"

try:
    print(f"Checking status for: {JOB_NAME}...")
    job = client.batches.get(name=JOB_NAME)
    print(f"Status: {job.state}")

    # 2. Extract Result File ID (Checking all possible locations)
    result_file_id = None
    
    # Try 'dest' (where your previous log found it)
    if hasattr(job, 'dest') and job.dest:
        result_file_id = getattr(job.dest, 'file_name', job.dest)
    # Try 'output'
    elif hasattr(job, 'output') and job.output:
        result_file_id = getattr(job.output, 'file_name', job.output)
    # Try 'output_config'
    elif hasattr(job, 'output_config') and hasattr(job.output_config, 'file_name'):
         result_file_id = job.output_config.file_name
    
    # MANUAL FALLBACK: If discovery fails, calculate from Job ID
    if not result_file_id:
        job_id = JOB_NAME.split('/')[-1]
        result_file_id = f"files/batch-{job_id}"
        print(f"⚠️ Discovery failed, trying manual fallback ID: {result_file_id}")

    if result_file_id:
        print(f"Final Target File: {result_file_id}")
        
        # 3. Download the results
        # FIXED: Using 'file=' argument
        print("Downloading results...")
        try:
            content_bytes = client.files.download(file=result_file_id)
            
            output_path = "batch_results_sft.jsonl"
            with open(output_path, "wb") as f:
                f.write(content_bytes)
                
            print(f"✅ Success! Results saved to: {os.path.abspath(output_path)}")
            
            # 4. Quick Peek
            with open(output_path, "r") as f:
                first_line = json.loads(f.readline())
                print("\n--- SAMPLE RESULT (Request ID: {}) ---".format(first_line.get('key')))
                # Check for code execution in the response
                resp = first_line.get('response', {}).get('candidates', [{}])[0].get('content', {}).get('parts', [])
                for p in resp:
                    if 'executable_code' in p: print("💻 Code found in response!")
                    if 'code_execution_result' in p: print(f"✅ Code Result: {p['code_execution_result']['output']}")
        
        except Exception as download_error:
            print(f"❌ Download failed: {download_error}")
            print("This usually happens if the 48-hour retention period has expired.")

except Exception as e:
    print(f"An error occurred: {e}")