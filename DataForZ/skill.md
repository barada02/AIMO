# Antigravity Skills & Reference Implementations

## Topic 1: Google ADK Agent Setup & FastAPI Integration
This section details the correct workflow for scaffolding a Google ADK agent and properly exposing it via a FastAPI endpoint. It covers avoiding common async object errors, correctly setting the application environment, and parsing the raw ADK output block into readable text.

### Step 1: Initialization & Agent Scaffold
1. Install the Agent Development Kit:
   ```bash
   pip install google-adk python-dotenv
   ```
2. Scaffold a new agent project:
   ```bash
   adk create my-agent-name
   ```
   This generates a folder with an `agent.py` file containing your agent definitions.

### Step 2: Environment Variables
The ADK models will crash silently or raise generic API client errors if they cannot locate an API key.
1. Create a `.env` file in the **root directory** of your application.
2. Add your API key:
   ```env
   GEMINI_API_KEY="AIzaSy..."
   ```
3. In your `main.py`, load the `.env` file securely **before** initializing your FastAPI app or ADK Runner:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Step 3: Fast & Proper API Execution (The `run_debug` bypass)
When hooking the ADK agent up to a FastAPI POST endpoint, avoid using the standard `Runner.run_async` method if possible, as it strictly expects raw ADK `Content/Part` objects. 

**Best Practice:** Use `Runner.run_debug` to pass raw string inputs seamlessly from the UI to the model.

**Important Reference Snippet (Runner Setup & Parsing):**
```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from my_agent.agent import root_agent

session_service = InMemorySessionService()

# **CRITICAL:** The 'app_name' parameter is explicitly required when using standard agents!
agent_runner = Runner(
    app_name="dataforzApp",
    agent=root_agent, 
    session_service=session_service
)

# Inside your async endpoint:
events = await agent_runner.run_debug(
    user_messages="User's plain string text goes here", 
    session_id="unique_user_id",
    user_id="test_user"
)

# Extracting the actual text from the ADK Event list involves checking permutations
reply_text = ""
for event in events:
    # 1. Strategy A: Event wraps a "message"
    if hasattr(event, "message") and event.message and getattr(event.message, "role", "") == "model":
        if hasattr(event.message, "content") and hasattr(event.message.content, "parts"):
            for part in event.message.content.parts:
                if hasattr(part, "text") and part.text:
                    reply_text += part.text
                    
    # 2. Strategy B: Event ITSELF is the message data object
    elif hasattr(event, "content") and event.content and hasattr(event.content, "parts"):
        for part in event.content.parts:
            if hasattr(part, "text") and part.text:
                reply_text += str(part.text)
```

---

## Topic 2: FastAPI + Firestore Async Execution
You can use the `db` client within your FastAPI routes to interact with Firestore. Remember that FastAPI handles endpoints asynchronously (`async def`), but the standard Python Firestore client is synchronous.

To prevent Firestore calls from blocking your live event loop (delaying other users), you must run them in a separate thread.

```python
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
# (Assume Firebase Admin SDK is already initialized)

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=5)

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    # Retrieve user data via the thread pool executor!
    user_ref = db.collection("users").document(user_id)
    doc = await app.loop.run_in_executor(executor, user_ref.get)
    
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return {"message": "User not found"}

@app.post("/users")
async def create_user(user_data: dict):
    # Example snippet for writing data to Firestore
    doc_ref = db.collection("users").add(user_data)
    return {"id": doc_ref[1].id, "message": "User created"}
```