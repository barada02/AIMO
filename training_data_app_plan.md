# LLM Training Data Generation Platform
## Architecture & Implementation Plan

## 1. Overview
A lightweight, single-repository web application designed to generate, refine, and manage high-quality training datasets for math-focused LLMs. The platform facilitates three main categories of data generation: Model Distillation, Domain Adaptation, and Supervised Fine-Tuning (SFT).

## 2. System Architecture
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML, CSS, and JavaScript (served directly from the FastAPI root `/` endpoint using `Jinja2Templates` and static file mounting). No heavy frameworks like React.
- **Database:** SQLite (for easy local setup) or PostgreSQL, accessed via SQLAlchemy or SQLModel.
- **LLM Integration:** Async API calls to an LLM provider (e.g., OpenAI API, Deepseek, or local vLLM instance) for chat, data structuring, and generation.

## 3. Core Features & Three Data Pillars

### Pillar A: Model Distillation Data
- **Purpose:** Extracting reasoning traces and step-by-step solutions from a stronger "teacher" model (e.g., GPT-4o, Claude 3.5 Sonnet) to train a smaller model.
- **Feature:** Bulk upload of problem statements. The app automatically queries the teacher model using high-quality Chain-of-Thought (CoT) prompts and saves the input-output pairs.

### Pillar B: Domain Adaptation Data (Pre-training/Continued Pre-training)
- **Purpose:** Teaching the model raw domain knowledge from textbooks, research papers, or PDFs.
- **Feature:** PDF/Text upload functionality. The backend chunks the text and uses an LLM to generate synthetic Q&A pairs, theorem explanations, and concept summaries to adapt the model to complex Math Olympiad terminology.

### Pillar C: Supervised Fine-Tuning (SFT) & Pattern Data
- **Purpose:** High-quality, human-aligned reasoning paths for specific mathematical patterns.
- **Workflow (Interactive Chat):**
  1. **Input:** User submits a root problem, their manual solution, their thinking process, and the underlying mathematical pattern.
  2. **Chat Phase:** A chat interface opens. The LLM acts as a sounding board, discussing the solution, refining the reasoning steps, and formatting it into a pristine CoT structure.
  3. **Confirmation:** The user reviews the finalized LLM-generated training sample in a split-screen or modal window.
  4. **Persist:** A "Push to DB" GUI button commits the finalized pair to the database.

### Pillar D: Problem Variabilization (Data Enrichment)
- **Purpose:** Multiplying the dataset size and robustness by altering numbers, contexts, or phrasing without changing the underlying mathematical logic.
- **Tracking System:** 
  - Every problem is tracked in a tree structure. 
  - The original user-inputted problem is the `Root Problem`.
  - The LLM can be prompted to generate `Variant 1`, `Variant 2`, etc.
  - Variants maintain a foreign key bridging back to the `Root Problem` to ensure dataset stratification (so root and variants don't accidentally leak across train/test splits).

## 4. Database Schema (High-Level)

**Table: `problems`**
- `id` (PK)
- `problem_text`
- `problem_type` (Distillation, Domain, SFT)
- `is_root` (Boolean)
- `parent_id` (FK to `problems.id`, null if root)
- `source_material` (e.g., PDF name, or user input)

**Table: `sft_sessions`** (To save chat states)
- `session_id` (PK)
- `problem_id` (FK)
- `chat_history` (JSON)
- `current_status` (Draft, Ready, Committed)

**Table: `training_data`** (The final formatted output)
- `id` (PK)
- `problem_id` (FK)
- `prompt` (The exact string going to the model)
- `response` (The exact target string)
- `format` (e.g., Alpaca, ChatML, OpenAI Messages)
- `created_at` (Timestamp)

## 5. Endpoints (FastAPI structure)

### UI Routes
- `GET /` -> Serves the main SPA (Single Page Application) HTML.
- `GET /static/{filepath}` -> Serves CSS, JS, and assets.

### API Routes
- `POST /api/chat/stream` -> Handles the SFT interactive chat (SSE for streaming).
- `POST /api/generate-variant/{problem_id}` -> Triggers LLM to generate a variant.
- `POST /api/distill/batch` -> Triggers batch distillation task in background.
- `POST /api/upload/document` -> Handles PDF uploads for domain adaptation.
- `POST /api/training-data/commit` -> The "Push to DB" button handler.
- `GET /api/training-data/export` -> Exports the DB to a `.jsonl` file ready for HuggingFace/Unsloth.

## 6. User Interface Layout (Vanilla JS Design)
- **Sidebar:** Navigation (SFT Builder, Distillation Jobs, Document Parser, Data Explorer).
- **Main View (SFT Builder):**
  - **Left Pane:** Input forms (Problem, My Solution, My Thoughts, Pattern).
  - **Middle Pane:** Chat window (WebSocket or SSE) to converse with the LLM about the problem.
  - **Right Pane:** Live preview of the "Final Training Data Object" (JSON format). Updates dynamically. Includes the large "Push to Database" button and "Generate Variant" button.