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

# LLM Math Olympiad Resources
## 1. Fundamentals
### Andrej Karpathy's "Neural Networks: Zero to Hero"
- This is the gold standard. He takes you from basic matrix multiplication and backpropagation all the way to building a mini-GPT from scratch in PyTorch.
### "The Illustrated Transformer" by Jay Alammar
- Visual guide to Attention & Positional Encoding
### "Dive into Deep Learning" (d2l.ai)
- Focus on MLPs, Optimization, & Attention mechanisms

## 2. LLMs & Prompt Engineering
### PromptingGuide.ai
- Chain-of-Thought (CoT), Self-Consistency, Tree of Thoughts
### Hugging Face NLP Course
- Transformers library, tokenizers, basic fine-tuning
### "State of GPT" (Andrej Karpathy)
- Video lecture on Pre-training $\rightarrow$ SFT $\rightarrow$ RLHF

## 3. Math-Specific AI (Research Papers)
### "Chain-of-Thought Prompting Elicits Reasoning"
- Wei et al. (2022): The foundation of LLM reasoning
### "PAL: Program-aided Language Models"
- Gao et al.: Prompting LLMs to write Python to solve math
### "Let's Verify Step by Step"
- Lightman et al. (2023): Process Reward Models (PRMs) for scoring steps
### "DeepSeekMath"
- Insights into training SOTA open models for math
### "AlphaGeometry"
- Google DeepMind: Olympiad Geometry without human demos

## 4. Practical Frameworks & Tools
### Unsloth (GitHub)
- Fast LoRA/QLoRA fine-tuning even on single GPUs
### Hugging Face TRL
- Training Reward Models & Direct Preference Optimization (DPO)
### Agent Frameworks
- LangChain, LangGraph, AutoGen
- Use for building LLM + Python REPL loops
### MATH Dataset (Hendrycks et al.)
- Standard dataset for competition math problems