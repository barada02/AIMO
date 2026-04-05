import os
import sys
import json
import urllib.request
from dotenv import load_dotenv
from google import genai

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_google_batch.py <job_name>")
        print("Example: python check_google_batch.py batches/hu7jauh5l8p89xsnfhinnn1yevz6115tmwoe")
        sys.exit(1)

    job_name = sys.argv[1]
    
    print(f"--- Checking Status for: {job_name} ---")
    
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[ERROR] Missing GOOGLE_API_KEY in environment variables.")
        return

    client = genai.Client(api_key=api_key)
    
    try:
        job = client.batches.get(name=job_name)
        print(f"State: {job.state}")
        
        # Check request counts if available in the job object
        completed = getattr(job, 'completed_request_count', 0)
        failed = getattr(job, 'failed_request_count', 0)
        total = getattr(job, 'request_count', 0)
        
        print(f"Progress: {completed} completed, {failed} failed out of {total} total requests.")

        if "SUCCEEDED" in str(job.state):
            print("\nJob Succeeded!")
            
            dest = getattr(job, 'dest', None)
            file_name = None
            if dest and getattr(dest, 'file_name', None):
                file_name = dest.file_name
                
            print(f"Output File Name: {file_name}")
            
            if file_name:
                print("\nDownloading results via Files API...")
                try:
                    # Fetching as a file object
                    response_bytes = client.files.download(file=file_name)
                    
                    out_file = "batch_results.jsonl"
                    with open(out_file, "wb") as f:
                        f.write(response_bytes)
                    print(f"Successfully downloaded results to: {out_file}")
                except Exception as e:
                    print(f"[ERROR] Failed to download using the Files API: {e}")
                    
        elif "FAILED" in str(job.state):
            print("\nJob Failed! Check Google Cloud Console / AI Studio for details.")
        elif "CANCELLED" in str(job.state):
            print("\nJob was Cancelled.")
        else:
            print("\nJob is still running. Try checking again later.")
            
    except Exception as e:
        print(f"[ERROR] Failed to get job status: {e}")

if __name__ == "__main__":
    main()
