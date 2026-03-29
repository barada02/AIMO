Integrate with FastAPI : 
You can then use the db client within your FastAPI routes to interact with Firestore. Remember that FastAPI is often used with asynchronous operations, and while the Firestore client for Python doesn't have native async/await methods, you can run synchronous Firestore calls in a separate thread using FastAPI's run_in_threadpool or by using asynchronous programming best practices.


```
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor


app = FastAPI()
# Initialize Firebase Admin SDK as shown above

executor = ThreadPoolExecutor(max_workers=5) # Adjust as needed

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    # Run synchronous Firestore operation in a thread pool
    user_ref = db.collection("users").document(user_id)
    doc = await app.loop.run_in_executor(executor, user_ref.get)
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return {"message": "User not found"}

@app.post("/users")
async def create_user(user_data: dict):
    # Example of adding data
    doc_ref = db.collection("users").add(user_data)
    return {"id": doc_ref[1].id, "message": "User created"}
```