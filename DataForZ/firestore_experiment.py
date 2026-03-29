import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

def main():
    print("--- Simple Firestore Read/Write Experiment ---")
    
    # 1. Initialize the Firebase Admin SDK using your service account key
    try:
        # NOTE: You MUST download your Firebase Service Account JSON file
        # and name it 'firebase-credentials.json' in this folder for this script to work.
        cred = credentials.Certificate("firebase-credentials.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized successfully!")
    except FileNotFoundError:
        print("\n[ERROR] Could not find 'firebase-credentials.json'.")
        print("Please download it from the Firebase Console (Project Settings -> Service Accounts -> Generate New Private Key).")
        print("Save it in this folder as 'firebase-credentials.json'.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize Firebase: {e}")
        sys.exit(1)

    # 2. WRITE DATA (Create a document)
    print("\n1. Writing data to Firestore...")
    doc_ref = db.collection("experimental_collection").document("test_doc_1")
    
    data_to_save = {
        "problem": "What is the square root of 144?",
        "solution": "12",
        "tags": ["math", "experiment"],
        "is_test": True
    }
    
    doc_ref.set(data_to_save)
    print(f"Data written successfully to collection 'experimental_collection', document 'test_doc_1'")

    # 3. READ DATA (Fetch the document back)
    print("\n2. Reading data back from Firestore...")
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"Document data retrieved:")
        print(doc.to_dict())
    else:
        print("No such document found!")

if __name__ == "__main__":
    main()
