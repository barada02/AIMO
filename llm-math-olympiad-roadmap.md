---
markmap:
  colorFreezeLevel: 4
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

# LLM for Math Olympiad: A Focused Roadmap
## 1. Fundamentals (The Bare Minimum)
### 1.1 Neural Network Basics
- What is a perceptron?
- Activation functions (ReLU, GeLU)
- Feedforward Neural Networks (FNN)
### 1.2 Training & Optimization
- Loss functions (Cross Entropy)
- Backpropagation (Intuition, not heavy math)
- Optimizers (Adam, AdamW)
## 2. From Sequences to Attention
### 2.1 The Sequence Problem
- Why traditional NNs fail on sequences
- (Optional/Brief) RNNs/LSTMs - just understand the bottleneck
### 2.2 Word Embeddings
- Word2Vec / GloVe concepts
- Tokenization (BPE, WordPiece, Tiktoken) - **Crucial** for math (how numbers are split)
### 2.3 The Transformer Revolution
- **Attention Mechanism:** The core of LLMs (Self-Attention, Multi-Head Attention)
- Positional Encoding (Absolute, RoPE)
- Transformer Architecture: Encoder (BERT) vs. Decoder (GPT)
- *Practical:* Build a simple self-attention block in PyTorch.
## 3. Large Language Models (LLMs)
### 3.1 Pre-training
- Next-token prediction objective
- Scaling Laws (Compute vs. Data vs. Model Size)
### 3.2 Post-training (Alignment)
- Instruction Tuning (SFT - Supervised Fine-Tuning)
- RLHF (Reinforcement Learning from Human Feedback) & DPO (Direct Preference Optimization)
### 3.3 Prompt Engineering (Immediate Practicality)
- Zero-shot, Few-shot prompting
- **Chain of Thought (CoT):** Essential for math reasoning!
- Tree of Thoughts (ToT)
## 4. Specializing LLMs for Math (Olympiad Level)
### 4.1 Fine-Tuning Techniques
- LoRA / QLoRA (Parameter-Efficient Fine-Tuning)
- Fine-tuning on math datasets (e.g., MATH, GSM8K)
### 4.2 Tool Use & Augmentation
- Toolformer concepts (Teaching LLMs to use calculators/Python)
- Code-augmented reasoning (Program-Aided Language Models - PAL)
- *Practical:* Connect an open-source LLM (like Llama 3) to a Python REPL via an agent framework (LangChain/LlamaIndex).
### 4.3 Advanced Reasoning & Search
- Majority Voting (Self-Consistency)
- Process Reward Models (PRMs) - Rewarding steps, not just the final answer. (Key for AlphaGeometry/AlphaProof level systems).
- Search algorithms guided by LLMs (MCTS - Monte Carlo Tree Search).
## 5. Practical Build Path (Your Project)
### Phase 1: API & Prompting
- Use OpenAI API (or Deepseek Coder/Math)
- Implement Chain-of-Thought prompting
- Implement Self-Consistency (sample 10 times, take majority answer)
### Phase 2: Open Source & RAG/Tools
- Run models locally (vLLM, Ollama)
- Build an agent that generates Python code to solve the math problem, runs it, and reads the output.
### Phase 3: Fine-tuning
- Fine-tune a small model (e.g., Llama-3-8B) on a dataset of step-by-step math solutions using LoRA.
### Phase 4: Advanced (Olympiad System)
- Train a Process Reward Model (PRM) to evaluate intermediate reasoning steps.
- Implement a search tree (like MCTS) where the LLM generates next steps and the PRM scores them.
