import json
import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def main():
    print("--- Parsing and Uploading Variants Data to Firestore ---")
    
    batch_file_path = os.path.join(os.path.dirname(__file__), 'batch_results.jsonl')
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')

    if not os.path.exists(batch_file_path):
        print(f"[ERROR] Batch results file not found at {batch_file_path}")
        return

    # Initialize the Firebase Admin SDK
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        # Connect to specific database ID
        db = firestore.client(database_id='dataforz-1')
        print("Firebase initialized successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Firebase: {e}")
        return

    raw_collection = db.collection('aimeVariantRawDataCollection')
    meta_collection = db.collection('aimeVariantMetadataCollection')

    local_raw_list = []
    local_meta_list = []
    
    total_variants_processed = 0
    total_lines = 0

    print("Processing batch_results.jsonl ...")
    
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            total_lines += 1
            
            try:
                # 1. Parse the outer JSONL line wrapper
                obj = json.loads(line)
                batch_key = obj.get('key', 'Unknown_Key')
                
                response_obj = obj.get('response', {})
                model_version = response_obj.get('modelVersion', 'unknown-model')
                candidates = response_obj.get('candidates', [])
                
                if not candidates:
                    print(f"  [WARNING] Skipping key {batch_key}: No candidates found.")
                    continue
                    
                parts = candidates[0].get('content', {}).get('parts', [])
                if not parts:
                    continue
                    
                raw_text = parts[0].get('text', '')
                if not raw_text:
                    continue

                # Clean LLM Markdown wrapping
                clean_text = raw_text.strip()
                if clean_text.startswith('```json'):
                    clean_text = clean_text[7:]
                elif clean_text.startswith('```'):
                    clean_text = clean_text[3:]
                    
                if clean_text.endswith('```'):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
                
                # 2. Fix LaTeX escaping issues to safely convert to JSON
                fixed_text = clean_text.replace('\\', '\\\\')
                fixed_text = fixed_text.replace('\\\\"', '\\"')
                fixed_text = fixed_text.replace('\\\\n', '\\n')
                fixed_text = fixed_text.replace('\\\\t', '\\t')
                fixed_text = fixed_text.replace('\\\\r', '\\r')
                
                # Double check for backspace which comes from \b
                fixed_text = fixed_text.replace('\\\\b', '\\b')
                fixed_text = fixed_text.replace('\\\\f', '\\f')
                
                try:
                    data = json.loads(fixed_text)
                except json.JSONDecodeError as je:
                    print(f"  [ERROR] Could not parse LLM JSON for key {batch_key}: {je}")
                    continue
                    
                original_summary = data.get('original_problem_summary', '')
                variants = data.get('variants', [])
                
                if not variants:
                    print(f"  [WARNING] No variants list found inside parsed JSON for key {batch_key}.")
                    continue
                    
                # 3. For each variant, upload Raw Data and Metadata
                for v in variants:
                    doc_id = str(uuid.uuid4())
                    
                    variant_id_str = v.get('variant_id', 'unknown_var_id')
                    problem_str = v.get('problem', '')
                    solution_str = v.get('solution', '')
                    reasoning_str = v.get('variant_reasoning', '')
                    
                    if not problem_str or not solution_str:
                        continue # Skip empty variants
                        
                    # RAW DATA Schema
                    raw_data = {
                        'id': doc_id,
                        'problem': problem_str,
                        'solution': solution_str
                    }
                    
                    # METADATA Schema
                    meta_data = {
                        'problem_id': doc_id,    # Same as Raw ID
                        'batch_key': batch_key,  # The original year-set-no reference
                        'variant_id': variant_id_str, # Identifying ID from LLM
                        'original_problem_summary': original_summary,
                        'variant_reasoning': reasoning_str,
                        'model_version': model_version
                    }
                    
                    # Write to Firestore
                    raw_collection.document(doc_id).set(raw_data)
                    meta_collection.document(doc_id).set(meta_data)
                    
                    # Append to local lists
                    local_raw_list.append(raw_data)
                    local_meta_list.append(meta_data)
                    
                    total_variants_processed += 1
                    
                    if total_variants_processed % 50 == 0:
                        print(f"  ... Uploaded {total_variants_processed} variant records...")
                        
            except Exception as e:
                print(f"  [ERROR] on line {total_lines}: {e}")

    # 4. Save to local JSON files
    raw_local_path = os.path.join(os.path.dirname(__file__), 'aimeVariantRawDataCollection.json')
    meta_local_path = os.path.join(os.path.dirname(__file__), 'aimeVariantMetadataCollection.json')
    
    with open(raw_local_path, 'w', encoding='utf-8') as f:
        json.dump(local_raw_list, f, indent=4)
        
    with open(meta_local_path, 'w', encoding='utf-8') as f:
        json.dump(local_meta_list, f, indent=4)

    print(f"\nSaved local Raw Data JSON: {raw_local_path}")
    print(f"Saved local Metadata JSON: {meta_local_path}")
    print(f"--- Migration Complete! Processed {total_lines} lines and uploaded {total_variants_processed} discrete variants! ---")

if __name__ == "__main__":
    main()
