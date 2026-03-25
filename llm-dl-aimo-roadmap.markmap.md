---
markmap:
  colorFreezeLevel: 2
  duration: 500
  maxWidth: 300
  initialExpandLevel: 2
  spacingVertical: 20
  spacingHorizontal: 80
  paddingX: 8
  autoFit: true
  pan: true
  zoom: true
---

# AIMO Secret Prep Roadmap (LLM + DL, Zero Waste)

## Part 0 — Competition Orientation (Read First)
- Chapter 0.1: AIMO Problem Format
  - Concepts
    - Text-only olympiad problems in LaTeX
    - Final answer is integer in range [0, 99999]
    - Public vs private evaluation behavior
  - Tasks
    - Read `info/overview.md`
    - Read `info/data_description.md`
    - Write your own one-page summary of rules
- Chapter 0.2: Submission Interface
  - Concepts
    - Inference API flow and one-by-one prediction
    - Importance of deterministic, robust outputs
  - Libraries
    - Python standard libs: `json`, `re`, `time`, `traceback`
  - Tasks
    - Run sample submission end-to-end once
    - Validate output format locally

## Part 1 — Mathematical & Programming Prerequisites
- Chapter 1.1: Python for ML
  - Concepts
    - Data structures, functions, classes, error handling
    - File I/O and clean project structure
  - Libraries
    - `numpy`, `pandas`, `pathlib`
  - Tasks
    - Build a script that loads problems and prints structured records
    - Implement reusable logging utility
- Chapter 1.2: Math for Model Builders
  - Concepts
    - Linear algebra: vectors, matrices, dot product
    - Calculus: gradients, chain rule intuition
    - Probability: distributions, expectation, variance
  - Tasks
    - Solve 20 exercises focused on gradients and optimization
    - Explain backpropagation on a 2-layer network in your own words

## Part 2 — Deep Learning Core
- Chapter 2.1: Neural Networks Fundamentals
  - Concepts
    - Perceptron to MLP
    - Activation functions and representation learning
    - Loss functions and gradient descent
  - Libraries
    - `torch`, `torch.nn`, `torch.optim`
  - Tasks
    - Implement an MLP in PyTorch from scratch (no trainer framework)
    - Train and evaluate on a simple dataset
- Chapter 2.2: Training Mechanics
  - Concepts
    - Batch training, epochs, validation split
    - Overfitting, regularization, early stopping
    - Learning-rate scheduling and optimizer behavior
  - Libraries
    - `torch.utils.data`, `torchmetrics` (optional)
  - Tasks
    - Compare SGD vs AdamW with the same model
    - Plot train/val curves and diagnose failures
- Chapter 2.3: Efficient DL Practice
  - Concepts
    - Mixed precision (bf16/fp16)
    - Gradient clipping and numerical stability
    - Reproducibility and seed control
  - Tasks
    - Add deterministic seeds to all experiments
    - Measure memory peak and runtime for one training run

## Part 3 — Transformer & LLM Foundations
- Chapter 3.1: Transformer Architecture
  - Concepts
    - Self-attention and multi-head attention
    - Positional information, residual connections, normalization
    - Encoder/decoder intuition and decoder-only models
  - Tasks
    - Draw full transformer block from memory
    - Implement scaled dot-product attention in PyTorch
- Chapter 3.2: Tokenization & Context
  - Concepts
    - BPE/SentencePiece intuition
    - Context window and truncation trade-offs
    - Prompt formatting sensitivity
  - Libraries
    - `tokenizers`, `transformers`
  - Tasks
    - Inspect token counts for 50 math problems
    - Build truncation-safe prompt templates
- Chapter 3.3: LLM Inference Control
  - Concepts
    - Temperature, top-p, max_new_tokens, stop criteria
    - Deterministic vs stochastic decoding
  - Tasks
    - Benchmark decoding configs on same problem subset
    - Choose default decoding policy for competition use

## Part 4 — LLM Training & Adaptation (Only Practical)
- Chapter 4.1: Instruction Tuning Basics
  - Concepts
    - SFT objective and dataset format
    - Prompt-response curation quality
  - Libraries
    - `datasets`, `transformers`, `trl` (optional)
  - Tasks
    - Build a small clean SFT dataset for math reasoning
    - Run one baseline SFT experiment
- Chapter 4.2: Parameter-Efficient Fine-Tuning
  - Concepts
    - LoRA/QLoRA and adapter trade-offs
    - When tuning helps vs hurts
  - Libraries
    - `peft`, `bitsandbytes` (if supported)
  - Tasks
    - Train one LoRA adapter
    - Compare base model vs tuned model on same validation split
- Chapter 4.3: Model Selection Criteria
  - Concepts
    - Quality vs speed vs memory tradeoff
    - Stability under repeated runs
  - Tasks
    - Build a model card table: params, context, latency, accuracy

## Part 5 — Math Reasoning Systems for AIMO
- Chapter 5.1: Prompting for Mathematical Reasoning
  - Concepts
    - Decomposition prompts
    - Self-consistency and majority voting
    - Structured answer formatting
  - Tasks
    - Create 3 prompt styles and compare error types
- Chapter 5.2: Program-Aided Solving
  - Concepts
    - Generate-check loops using Python execution
    - Symbolic support and arithmetic verification
  - Libraries
    - `sympy`, `math`, `fractions`
  - Tasks
    - Implement safe code-execution helper with timeout
    - Add consistency checks between text answer and computed result
- Chapter 5.3: Verifier and Reranking
  - Concepts
    - Candidate scoring by consistency and constraints
    - Rejecting malformed or impossible outputs
  - Tasks
    - Build verifier rules for integer range and modulo conditions
    - Add reranker that picks best candidate from N generations

## Part 6 — Competition Pipeline Engineering
- Chapter 6.1: End-to-End Inference Pipeline
  - Concepts
    - Preprocess -> generate -> verify -> normalize -> submit
    - Fail-safe defaults for parse/runtime errors
  - Tasks
    - Build single `predict(problem_text)` function with clear stages
    - Add fallback when generation fails
- Chapter 6.2: Robust Answer Extraction
  - Concepts
    - Regex parsing hierarchy
    - Integer normalization and clipping policy
  - Libraries
    - `re`
  - Tasks
    - Implement parser with unit tests for edge cases
    - Test on adversarial outputs
- Chapter 6.3: Runtime & Memory Hardening
  - Concepts
    - Throughput bottlenecks
    - OOM prevention and graceful degradation
  - Tasks
    - Add profiling logs (latency per problem, memory usage)
    - Define reduced-compute fallback mode

## Part 7 — Evaluation & Experimentation Discipline
- Chapter 7.1: Validation Framework
  - Concepts
    - Fixed split evaluation and reproducible comparisons
    - Metric suite: exact match, parse failure, timeout failure
  - Tasks
    - Build a local evaluation script for all candidate systems
- Chapter 7.2: Error Taxonomy
  - Concepts
    - Arithmetic errors
    - Logical reasoning errors
    - Parsing/formatting errors
    - Time/memory failures
  - Tasks
    - Label 100 failed examples and categorize root cause
- Chapter 7.3: Improvement Loop
  - Concepts
    - Hypothesis-driven iteration
    - Keep/remove decisions based on measurable gain
  - Tasks
    - Maintain experiment table with exact config and result

## Part 8 — Library Stack (Reference)
- Core Stack
  - `python`, `numpy`, `pandas`, `pytorch`
- LLM Stack
  - `transformers`, `datasets`, `accelerate`, `tokenizers`
- Tuning Stack
  - `peft`, `bitsandbytes` (optional), `trl` (optional)
- Math & Verification
  - `sympy`, `math`, `fractions`, `re`
- Utilities
  - `pyyaml`, `tqdm`, `matplotlib` (for diagnostics)

## Part 9 — Project Structure Blueprint
- Chapter 9.1: Repository Layout
  - `src/data/` dataset readers and schema
  - `src/prompts/` prompt templates
  - `src/inference/` generation and decoding
  - `src/verifier/` checks and reranking
  - `src/eval/` metrics and reports
  - `notebooks/` experiments only
- Chapter 9.2: Essential Artifacts
  - Config file per experiment
  - Reproducible run logs
  - Failure-case notebook

## Part 10 — Mastery Milestones (Book End)
- Milestone 1: DL Competence
  - You can train/debug neural nets confidently
- Milestone 2: LLM Competence
  - You can control inference and diagnose generation behavior
- Milestone 3: AIMO System Competence
  - You can build robust solve-verify pipeline end-to-end
- Milestone 4: Competition Competence
  - You can produce stable submissions under strict constraints

## Appendix — Explicit Exclusions (No Time Waste)
- Do not study RLHF pipelines now
- Do not build distributed systems unless required
- Do not chase unrelated benchmarks
- Do not over-engineer infrastructure before baseline works
