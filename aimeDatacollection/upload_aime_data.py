import json
import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def main():
    print("--- Migrating AIME Data to Firestore ---")
    
    # Both dataset and credentials are now in the same directory as the script
    dataset_path = os.path.join(os.path.dirname(__file__), 'aime_dataset.json')
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')

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

    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read dataset: {e}")
        return

    raw_collection = db.collection('aimeRawDataCollection')
    meta_collection = db.collection('aimeMetadataCollection')

    total_uploaded = 0
    print(f"Loaded {len(data)} problems from dataset. Processing...")

    local_raw_list = []
    local_meta_list = []

    for item in data:
        problem = item.get('problem')
        url = item.get('url')
        year = item.get('year')
        set_name = item.get('set')
        problem_number = item.get('problem_number')

        if not problem:
            continue

        # Find all keys starting with 'solution'
        solution_keys = [k for k in item.keys() if k.startswith('solution')]
        
        for sol_key in solution_keys:
            solution = item.get(sol_key)
            if not solution:
                continue
                
            # Create a unique document ID
            doc_id = str(uuid.uuid4())
            
            # 1. Add to aimeRawDataCollection
            raw_data = {
                'id': doc_id,
                'problem': problem,
                'solution': solution
            }
            raw_collection.document(doc_id).set(raw_data)
            
            # 2. Add to metadata collection
            meta_data = {
                'url': url,
                'year': year,
                'set': set_name,
                'problem_number': problem_number,
                'problem_id': doc_id
            }
            meta_collection.document(doc_id).set(meta_data)
            
            # Store locally
            local_raw_list.append(raw_data)
            local_meta_list.append(meta_data)
            
            total_uploaded += 1
            if total_uploaded % 100 == 0:
                print(f"Uploaded {total_uploaded} documents...")

    # Save to local files
    raw_local_path = os.path.join(os.path.dirname(__file__), 'aimeRawDataCollection.json')
    meta_local_path = os.path.join(os.path.dirname(__file__), 'aimeMetadataCollection.json')
    
    with open(raw_local_path, 'w', encoding='utf-8') as f:
        json.dump(local_raw_list, f, indent=4)
        
    with open(meta_local_path, 'w', encoding='utf-8') as f:
        json.dump(local_meta_list, f, indent=4)

    print(f"Saved local JSON copies: {raw_local_path} and {meta_local_path}")
    print(f"--- Migration Complete! Total raw documents created: {total_uploaded} ---")

if __name__ == "__main__":
    main()
