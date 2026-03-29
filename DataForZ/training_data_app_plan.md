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
1. **User Action:** Selects a high-quality "Root" problem in the GUI.
2. **Agent Runner:** Instructs a "Variant Agent" to alter numbers and contexts while preserving logic, generating new problems.
3. **Review Process:** The GUI presents the original alongside the generated variants in a side-by-side modal.
4. **Finalization:** User toggles which variants are mathematically sound and pushes them to Firestore, maintaining a parent-child relationship.

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

**Collection: `problems` (The Root Data)**
- `document_id`: Auto-generated string
- `problem_text`: String
- `source`: String (User input, PDF name)
- `tags`: Array of Strings
- `is_root`: Boolean

**Collection: `training_pairs` (The Final Generated Output)**
- `document_id`: Auto-generated string
- `problem_id`: Reference string to `problems`
- `conversation`: Array of Objects (Simulating JSON structure for LLM training: `{"role": "user", "content": "..."}`)
- `generation_method`: String (Human, Agent_Distillation, Agent_Variant)
- `status`: String (Draft, Approved, Exported)
- `parent_id`: Reference string (if it's a variant of another problem)

**Collection: `agent_jobs` (State Management)**
- `document_id`: Auto-generated string
- `job_type`: String (Batch Distillation, PDF Parser)
- `total_tasks`: Integer
- `completed_tasks`: Integer
- `status`: String (Running, Paused, Completed, Failed)

## 6. Model Consistency & Context Engine

To prevent the AI from feeling "lost" or repetitive during long generation sessions, the system implements a persistent "Context Window" feature.

- **How it Works:** A background process tracks your progress in real-time (e.g., "Generated 15 Problem Solving outputs today. Last topic discussed was Calculus. Current active task is Model Distillation").
- **State Injection:** This meta-context is saved as a status document in Firestore. It is automatically retrieved and prepended to the AI's System Prompt at the start of every new chat interaction in the Right Panel.
- **The Result:** The model behaves like a consistent human collaborator. It knows exactly what you have achieved today, what schema you are focusing on, and what the last conversation was, allowing it to adapt its tone and outputs without you having to re-explain the state of the project every single time.