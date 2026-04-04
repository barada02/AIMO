# LLM Training Data Generation Platform
## Architecture & Implementation Plan

## 1. Overview
A web application designed to generate, refine, and manage high-quality training datasets for math-focused LLMs. The platform leverages the **`google-adk` (Agent Development Kit)** (acting as an "Agent Runner") and **Google Cloud Firestore** to create a scalable, agentic data generation pipeline that the user can heavily supervise and control.

## 2. System Architecture
- **Backend/Agent Runner:** Python (FastAPI or Flask) acting as the central "Agent Runner." It orchestrates the `google-adk` to manage multiple specialized agents (e.g., Distillation Agent, Review Agent, Math Expert Agent).
- **Frontend (GUI):** Vanilla HTML, CSS, and JavaScript. The UI serves as a command center to monitor agent activities, intervene in generation, and review data.
- **Database:** Google Cloud Firestore. Leveraging document-based NoSQL storage for flexible schema management, fast reads, and seamless scaling.
- **LLM Integration:** `google-adk` (Agent Development Kit) natively powering the agents, with capabilities for multi-turn reasoning, tool use, and structured JSON output.

## 3. Operational Process & Agent Workflows
The application operates on an "Agent Runner" paradigm, where the backend orchestrates autonomous generation that the user can supervise via the GUI.

### Multi-Agent Architecture for Complex Reasoning
To maximize the reasoning capabilities of the models and structure complex workflows like variant generation, the platform utilizes a specialized multi-agent network. Tasks are separated based on cognitive load:

- **Coordinator Agent (`gemini-2.5-flash`)**: The "Manager". Fast and efficient. It acts as the routing layer, analyzing the user's intent. If the user asks for variations of a problem, it proposes 3-4 distinct strategic angles (e.g., "Change the underlying geometry to coordinate mechanics", "Invert the goal constraints") and delegates the heavy lifting to the Reasoning Agent.
- **Math Reasoning Agent (`gemini-2.5-pro`)**: The "Solver". This agent is instantiated exclusively for heavy mathematical generation and solving. Instructed with extreme rigor, it executes the strategy designed by the Coordinator, synthesizing the complex step-by-step Chain-of-Thought (CoT) and ensuring mathematical accuracy.
- **Critic Agent (`gemini-2.5-flash`)**: The "Reviewer". Takes the Math Reasoning Agent's output, verifies the structural integrity (e.g., strict JSON formatting), double-checks for common computational hallucinations, and finalizes the payload for the frontend UI.

### Workflow A: Supervised Fine-Tuning (SFT) Chat & Refinement
1. **User Action:** Submits a raw math problem and an initial solution via the GUI.
2. **Agent Runner:** Spawns a "Review Agent."
3. **Interactive Process:** The Agent and User converse in the GUI. The Agent structures the problem into a highly detailed Chain-of-Thought (CoT) format.
4. **Finalization:** User manually audits the output, makes inline edits, and clicks "Approve & Save." The data is committed to Firestore.

### Workflow B: Autonomous Batch Distillation
1. **User Action:** Uploads a CSV/PDF of raw equations or problems.
2. **Agent Runner:** Spawns a "Distillation Agent" fleet in the background. Each agent autonomously solves issues step-by-step.
3. **Review Process:** The GUI displays a real-time dashboard of completed, pending, and failed tasks.
4. **Finalization:** The user audits a random sample of the generated CoT data and clicks "Commit Batch" to save them to Firestore.

### Workflow C: Problem Variabilization (Data Enrichment)
We employ a **Sequential Multi-Agent Architecture** to generate mathematically robust problem variations:
1. **User Action:** The user inputs a "Root" problem and its verified solution into the GUI and selects the "Variant Generation" mode.
2. **Strategy Agent (Coordinator):** Analyzing the root problem, this agent proposes 3-4 distinct variant strategies (e.g., "Change the constants," "Invert the goal," "Shift context to a real-world scenario").
3. **Generator Agent:** For the chosen strategies, the Generator Agent sequentially synthesizes brand new problems along with full Chain-of-Thought (CoT) solutions.
4. **Review Process:** The generated variants appear in the GUI Editor panel, allowing the user to view the new data side-by-side with the original.
5. **Finalization:** The user reviews and commits the variants. The system automatically inspects the problem's tags, routing it to the appropriate topic collection. It saves a `parent_id` referencing the original Root problem.

## 4. GUI Layout & Control Center (VS Code Style)

The graphical interface is designed similarly to VS Code and the Antigravity platform. It is split into three main horizontal sections and relies on a Left-Side Navigation Tab system.

### Global Layout Structure
- **Left Section (Navigation):** Used to switch between the three main views tabs (Dashboard, Console, Database).
- **Middle Section (The Editor):** The main workspace where the generated JSON data appears. This is a fully editable area where you can view the data structure and manually fix any math errors.
- **Right Section (Agent Chat):** A chat interface to converse directly with the AI agent. You can ask the AI to modify the JSON data in the middle section, and once satisfied, click a prominent "Push to Database" GUI button.

### The Three Main Navigation Tabs

#### Tab 1: Main Dashboard (Data Iteration Hub)
- **Purpose:** This is where the core data generation and refinement happens.
- **Task Selector Buttons:** A set of GUI buttons (e.g., "Model Distillation", "Problem Solving", "SFT") that instantly switch the active System Prompts and strict JSON schemas to match the specific data generation task you are currently performing. This makes scaling easy when you want to add new task types later.
- **Active Panes:** Displays the Middle Section (JSON data Editor) and Right Section (Agent Chat).
- **Workflow:** You select a task type, then instruct the AI in the chat to generate a math problem. The AI outputs the strictly formatted JSON in the middle editor. You make manual tweaks if needed, then click "Push to Database".

#### Tab 2: Console & Model Control
- **Purpose:** Configuration center for the Agent Runner.
- **Features:** 
  - Dropdowns to select different LLM models.
  - Text areas to edit the core System Prompts.
  - Tools to tweak the agent's behavior and environment variables without touching the codebase.

#### Tab 3: Database Visualization & Insights
- **Purpose:** A high-level overview of everything you've created in Firestore.
- **Features:**
  - View total metrics: How many problems generated, how many documents total in the database.
  - Apply filters to the database (e.g., sort by tags or SFT vs Distillation).
  - Visualization of the overall dataset health before exporting it to a `.jsonl` file.

## 5. Database Schema (Firestore Collections)

To ensure clean organization and facilitate dataset analysis (e.g., knowing exactly how many problems exist for a specific topic), data is divided into different collections based on the AI's tagging.

**Topic Collections (`algebra`, `combinatorics`, `geometry`, `number_theory`, `miscellaneous`)**
Each collection stores the final generated problem-solution documents.
- `document_id`: Auto-generated string
- `problem_text`: String (The math problem)
- `reasoning_steps`: Array of Strings (The step-by-step logic)
- `solution`: String (The final answer)
- `tags`: Array of Strings (e.g., ['algebra', 'sft'])
- `source`: String (User input, PDF name)
- `generation_method`: String (Human, Agent_Distillation, Agent_Variant)
- `parent_id`: Reference string (If this is a variant, the ID of the root problem it derived from; otherwise null)
- `timestamp`: Firestore Timestamp

***Routing Logic:*** *When pushing to the database, the backend inspects the `tags` array. If exactly one main topic tag (e.g., "algebra") is found, it routes to that collection. If multiple topics are found (e.g., algebra AND geometry), or if no topic is found, it saves to the `miscellaneous` collection.*

**Collection: `agent_jobs` (Batch State Management)**
- `document_id`: Auto-generated string
- `job_type`: String (Batch Distillation, PDF Parser)
- `total_tasks`: Integer
- `completed_tasks`: Integer
- `status`: String (Running, Paused, Completed, Failed)

**Collection: `topic_tracking` (Dataset Overview & Insights)**
- `document_id`: "global_stats"
- `algebra_count`: Integer
- `combinatorics_count`: Integer
- `geometry_count`: Integer
- `number_theory_count`: Integer
- `miscellaneous_count`: Integer
- `total_completed`: Integer

## 6. Model Consistency & Context Engine

To maintain high-quality outputs and prevent long-context degradation (hallucinations or repetitive problems), the model incorporates a strict session limit and real-time state injection.

- **Session Limiting (4-5 Problems):** Each interaction session is deliberately capped at 4 to 5 problem generations. Once this limit is reached, a "session refresh" happens to clear cognitive load and ensure the AI's output stays mathematically concise and creative.
- **Meta-Data Injection:** For each interaction within a session, the system injects a background summary of the already completed problems and the core context from the previous discussion.
- **Tracking Injection:** The model is fed the live data from the `topic_tracking` collection. Because the model knows exactly how many problems have been generated for Algebra, Combinatorics, Geometry, and Number Theory so far, it is dynamically aware of the dataset's current state and distribution, keeping it focused on what field needs more work without repetitive prompting.