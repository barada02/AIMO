from google import genai
import json
import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
# Initialize with your API Key
client = genai.Client(api_key=api_key)

JOB_NAME = "batches/3hrmrdf7oeq1gu4ebvvtb704l50aw6z5qzwz"

try:
    # Retrieve the job details
    job = client.batches.get(name=JOB_NAME)
    
    print("--- JOB METADATA ---")
    print(f"Display Name: {job.display_name}")
    print(f"State:        {job.state}")
    print(f"Created At:   {job.create_time}")
    
    # Check for failure details
    if job.state == "FAILED":
        print(f"!!! ERROR: {job.error if hasattr(job, 'error') else 'Unknown Error'}")
    
    # Check execution timeline
    if hasattr(job, 'start_time'):
        print(f"Started At:   {job.start_time}")
    if hasattr(job, 'end_time'):
        print(f"Ended At:     {job.end_time}")

    # Check for output results
    print("\n--- OUTPUT LOCATION ---")
    # For Gemini API, results are usually in 'dest'
    if hasattr(job, 'output_config'):
        print(f"Output Config: {job.output_config}")
    
    # If the job succeeded, let's see if there are results to download
    if job.state == "SUCCEEDED":
        # Check if they are inlined (small batches)
        if hasattr(job, 'dest') and hasattr(job.dest, 'inlined_responses'):
            print("Results are inlined. Sample of first result:")
            print(job.dest.inlined_responses[0])
        # Check if they are in a file (larger batches)
        elif hasattr(job, 'output'):
            print(f"Result File ID: {job.output}")
            print("Use client.files.get() to check if this file still exists.")

except Exception as e:
    print(f"Could not retrieve job: {e}")