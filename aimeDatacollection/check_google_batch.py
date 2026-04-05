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
            out_uri = getattr(job, 'output_uri', None)
            print(f"Output URI: {out_uri}")
            
            if out_uri:
                # The output URI is usually a link we can fetch using the API key or it's a Cloud Storage bucket depending on the endpoint.
                # Usually Google AI Studio batch jobs output a Cloud Storage URL that is publicly readable for a short time, 
                # or it gives you a URL you can just download with your API key.
                print(f"\nAttempting to download results...")
                
                # Check if it's a direct https URL
                if out_uri.startswith("https://"):
                    req = urllib.request.Request(out_uri)
                    try:
                        with urllib.request.urlopen(req) as response:
                            data = response.read()
                            
                        out_file = "batch_results.jsonl"
                        with open(out_file, "wb") as f:
                            f.write(data)
                        print(f"Successfully downloaded results to: {out_file}")
                    except Exception as e:
                        print(f"Could not auto-download. You might need to manually download it: {e}")
                else:
                    print("Output URI format unknown or requires a specific API call. Check the URL manually.")
                    
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
