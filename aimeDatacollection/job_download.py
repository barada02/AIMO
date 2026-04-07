import os
import time
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Use your successful job ID
JOB_NAME = "batches/xp3jvoqxuvn5m6u39bwn64tfuhm7fcazdyaa"
FILE_ID = "files/batch-xp3jvoqxuvn5m6u39bwn64tfuhm7fcazdyaa"
OUTPUT_FILE = "aime_variants_results.jsonl"

def robust_download(file_id, save_path, retries=5):
    for i in range(retries):
        try:
            print(f"📥 Download Attempt {i+1}/{retries}...")
            # Using the SDK download method
            content_bytes = client.files.download(file=file_id)
            
            with open(save_path, "wb") as f:
                f.write(content_bytes)
            
            print(f"✅ Success! File saved to {save_path}")
            return True
        except Exception as e:
            print(f"⚠️ Attempt {i+1} failed: {e}")
            if i < retries - 1:
                wait_time = (i + 1) * 5
                print(f"Waiting {wait_time}s before retrying...")
                time.sleep(wait_time)
    return False

# --- Main Execution ---
try:
    job = client.batches.get(name=JOB_NAME)
    print(f"\n--- Job Metadata ---")
    print(f"State: {job.state}")
    
    # Fix for the 0/0/0 count issue:
    if hasattr(job, 'state_counts') and job.state_counts:
        s = job.state_counts
        print(f"Real Progress: {s.succeeded} succeeded, {s.failed} failed out of {s.total} total.")
    else:
        # Fallback to the counts you were using
        print(f"Progress (Root): {getattr(job, 'completed_request_count', 0)} completed.")

    # Execute robust download
    robust_download(FILE_ID, OUTPUT_FILE)

except Exception as e:
    print(f"Fatal Error: {e}")