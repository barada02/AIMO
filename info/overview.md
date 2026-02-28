# AIMO Progress Prize 3 - Overview

## Competition Goal

The goal of this competition is to create **open-source algorithms and models** that can solve olympiad-level math problems written in **LaTeX format**. Your participation will help to advance AI models' mathematical reasoning skills and drive frontier knowledge.

## Description

> **Note**: This is the **third AIMO Progress Prize competition**. It builds upon the first AIMO Progress Prize competition, which was won in July 2024 by **Project Numina** and the second AIMO Progress Prize competition, which was won in April 2025 by **Nvidia's NemoSkills team**. 

### Key Features of AIMO3:
- Significantly increased problem difficulty
- New submission format
- Expanded prize pool
- Industry-leading compute resources for participants
- New auxiliary prizes to reward community contributions
- Updated rules for using open-source LLMs

### Background & Motivation

The ability to reason mathematically is a **critical milestone for AI**. Mathematical reasoning is the foundation for solving many complex problems, from engineering marvels to intricate financial models. However, current AI capabilities are limited in this area.

The **AI Mathematical Olympiad (AIMO) Prize** is a **$10mn fund** to spur the open development of AI models capable of performing as well as top human participants in the International Mathematical Olympiad (IMO).

### Recent Breakthroughs & Gap Analysis

Recent breakthroughs demonstrate AI achieving human-level results on IMO problems:
- Closed-source models achieved **gold medal performance** at the 2025 IMO
- Commercial models solved **50/50 AIMO2** public leaderboard problems with sufficient compute
- Highest Kaggle score was only **34/50**, demonstrating a significant gap between closed-source and open-source models

### Competition Design

**AIMO3** is designed to accelerate open-source progress and close this gap:

- **110 problems** spanning:
  - Algebra
  - Combinatorics  
  - Geometry
  - Number theory
- **Difficulty range**: National Olympiad level → IMO standard
- **Entirely original problems** created by an international team of problem solvers
- **Zero risk of train-test contamination**
- Problems designed to be **'AI hard'**, requiring genuine mathematical reasoning

Every problem is entirely original, ensuring zero risk of data contamination. Using this transparent and fair evaluation framework, the competition will help to strengthen the benchmarks for assessing AI models' mathematical reasoning skills.

Join us as we work towards a future where AI models' mathematical reasoning skills are accurately and reliably assessed, driving progress and innovation.

## Evaluation

### Public Test Set (During Submission Period)
During the submission period, submission notebooks are run only over the **public test set** and are evaluated by the unnormalized accuracy between their predicted labels and the ground-truth labels (i.e. number of correct answers).

### Private Test Set (After Submission Deadline)
After the submission deadline, submission notebooks will be run **twice** over the private test set and their predictions concatenated into a single submission file. We then evaluate submissions by a **penalized accuracy score**, as follows:

- **Both predicted answers correct**: Score = `1` for that problem
- **One correct, one incorrect**: Score = `0.5` for that problem  
- **Neither correct**: Score = `0` for that problem

A submission's overall score is the sum of its scores for each problem.

### Answer Format
In this competition, every ground-truth label is an **integer between 0 and 99999, inclusive**. Any modulo calculation required is explicitly stated in the problem statement (e.g., "What is the remainder when X is divided by Y?"), meaning all problems have answers in this range without any further adjustments.

> **Note**: This is a change from the first and second Progress Prizes, which used 3-digit answers with an implicit requirement to take your answer modulo 1000.

Answers may require basic computations, including modular arithmetic. For example, computations and additional examples are provided in the Reference Problems PDF found on the Data page.

## Submitting

You must submit to this competition using the provided **Python evaluation API**, which serves test set instances one-by-one in random order for the public leaderboard, and uses fixed, random order for the private leaderboard. To use the API, follow the template in the provided notebook.

## Prizes

### Total Fund: **$2,207,152**

#### Top-Ranking Team Prizes:
| Place | Prize Amount |
|-------|--------------|
| 1st   | $262,144     |
| 2nd   | $131,072     |
| 3rd   | $65,536      |
| 4th   | $32,768      |
| 5th   | $16,384      |

#### Overall Progress Prize Winner
The **Overall Progress Prize Winner** shall be the highest ranking team that achieves a score of **at least 47/50** on both public and private test sets. After any prizes for the five top-ranking teams have been awarded, the remainder of the total fund shall be awarded to the Overall Progress Prize Winner.

- If a team is named the Overall Progress Prize Winner: **minimum $1,589,248**
- If no team qualifies: the remainder rolls over to the next competition

### Additional Prizes: **$110,000**

#### 🏆 Longest Leader Prize: **$20,000**
Awarded to the team whose notebook(s) generates the best scoring submission on the leaderboard for the longest period of time between **November 20, 2025** and **February 2, 2026 11:59 PM UTC**.

**Requirements:**
- Notebooks must adhere to the same requirements regarding licensing, reproducibility, and documentation
- Must be made publicly available by **February 9, 2026 11:59 PM UTC**
- Must remain public until final Progress Prizes are awarded

#### 🧮 Hard Problem Prize: **$30,000**
Awarded to the highest ranked team(s) on the private leaderboard who solved the **most difficult problem(s)** in the private test set.

**How difficulty is measured:**
- Average accuracy score across all selected submissions at the end of competition
- If multiple problems tie for "most difficult": prize split equally among winning teams
- Tiebreaker: submission time (first to submit wins)

#### 📊 Math Corpus Prize: **$30,000**
Awarded to the team who provides the **most valuable dataset** to the community for improving AIMO model performance.

**Requirements:**
- Must be publicly released on **Kaggle** or **HuggingFace** by **February 9, 2026 11:59 PM UTC**
- Must create a Kaggle Discussion post linking to dataset and tagging it for Math Corpus Prize
- Dataset must be in **English**
- Maximum **5M datapoints**, each ≤ **100k characters**
- Must have **open source license** allowing free dissemination

**Evaluation Criteria (100 points total):**
- **Data Novelty** (25 points): Uniqueness from existing datasets
- **Format** (25 points): Easy handling, rich metadata
- **Performance** (50 points): Improvement to mathematical reasoning and AIMO model performance

#### ✍️ Writeup Prizes: **2 × $15,000**
Awarded to the **two best Solution Writeups** from non-winning teams.

**Requirements:**
- Official Kaggle Writeup attached to submission within **1 week** after competition end
- Mirror academic publication standard (reference: [AIMO2 winners' arXiv post](https://arxiv.org/abs/2504.16891))
- **Maximum 30k words** (~50 pages), with main section ≤ **5k words** (~10 pages)

**Evaluation Criteria (100 points total):**
- **Clarity** (10 points): Detailed model creation lifecycle
- **Ablation Studies** (10 points): Performance gain analysis
- **SOTA Comparison** (10 points): Evaluation vs. open-weight and commercial models  
- **Visuals** (10 points): Well-designed graphs and charts
- **Reproducibility** (60 points): Sufficient detail for reproduction

## Timeline

| Date | Event |
|------|--------|
| **November 20, 2025** | Competition Start |
| **April 8, 2026** | Entry Deadline & Team Merger Deadline |
| **April 15, 2026** | Final Submission Deadline |

> All deadlines are at **11:59 PM UTC** unless otherwise noted. Competition organizers reserve the right to update the timeline if necessary.

## Code Requirements

Submissions must be made through **Notebooks** with the following conditions:

### Runtime Limits:
- **CPU Notebook**: ≤ 9 hours
- **GPU Notebook**: ≤ 5 hours  
- **Internet access**: Disabled
- **External data**: Freely & publicly available (including pre-trained models)
- **Submission file**: Must be generated by the API

> **Note**: Submission runtimes are obfuscated. Repeat submissions may show up to 30 minutes variance.

### Upgraded Kaggle Hardware

🚀 **New H100 machines** added to the AIMO hardware pool!

**Important Notes:**
- **AIMO 3 Only**: H100s only available for this competition
- **No Internet**: All H100 sessions must have internet disabled
- Misuse may result in moderation action

## Language and Notation

All problems are **text-only** with mathematical notation in **LaTeX**.

### LaTeX Conventions:
- Packages: `amsmath`, `amssymb`, and `amsthm` 
- Variables: Math mode (e.g., $x$, $y$, $z$)
- Greek letters: $\alpha$, $\beta$, etc.
- Integers: Can be inside or outside math mode
- Environments: `align` and `align*` (using `amsmath` conventions)
- Equations: `$...$`, `$$...$$`, `\[...\]`, `\(...\)`, and `\begin{equation}`

### Mathematical Notation:
- **Sequences**: $\ldots$ can continue finite or infinite sequences
- **Multiplication**: Adjacency ($ab$), `\cdot` ($a \cdot b$), or `\times` ($a \times b$)
- **Factorial**: $n!$ represents $n \cdot (n-1) \cdot \ldots \cdot 1$ (with $0! = 1$)
- **Logarithms**: $\log$, $\ln$, $\lg$ (natural log unless base specified, e.g., $\log_2$)
- **Fractions**: `\frac{a}{b}` or inline `a/b`
- **Absolute value**: $|x|$ represents absolute value
- **Floor/Ceiling**: 
  - $\lfloor x \rfloor$: greatest integer ≤ $x$
  - $\lceil x \rceil$: smallest integer ≥ $x$  
  - $\{x\}$: fractional part = $x - \lfloor x \rfloor$

### Geometric & Set Notation:
- **Triangles**: Standard notation (e.g., triangle $ABC$ with sides $a$, $b$, $c$)
- **Angles**: Standard notation, degrees specified as $^\circ$, otherwise radians
- **Trigonometry**: $\sin$, $\cos$, $\tan$, etc.
- **Sets**: Curly brackets, e.g., $\{1, 2, 3\}$
- **Overline notation**: $\overline{abcd}$ represents integer formed by digits $a$, $b$, $c$, $d$

### Number Systems:
- $\mathbb{N}$: Positive integers ($> 0$)
- $\mathbb{Z}$: All integers  
- $\mathbb{Q}$: Rational numbers
- $\mathbb{R}$: Real numbers
- $\mathbb{Z}_n$: Integers $\{0, 1, 2, \ldots, n-1\}$

### Special Conventions:
- **Binomial coefficients**: $\binom{n}{k}$ with $\binom{n}{0} = 1$ and $\binom{n}{k} = 0$ if $k < 0$
- **Empty set operations**: Sum over empty set = $0$, product = $1$
- **Modular arithmetic**: For integers $a$, $b$, $m$: $a \equiv b \pmod{m}$ means $m | (a-b)$
- **Language**: British or American English accepted
- **Triangle taxonomy**: Bourbakist (equilateral ⊂ isosceles, squares ⊂ rectangles ⊂ parallelograms)
- **Trapezium**: Quadrilateral with at least one pair of parallel opposite sides

### Answer Requirements:
- All answers: **integers in range [0, 99999]**
- Questions worded so final answer lies in this range
- Modulus operations explicitly stated in problems
- May require basic computations including modular arithmetic

## Partnerships and Additional Resources

### Ecosystem Support
The Hosts' aim is not just to run a competition, but to provide a complete **ecosystem** for it.

### Key Partnerships:

#### 🔬 **Fields Model Initiative**
Supported by:
- **LLMC** from National Institute of Informatics, Tokyo
- **Benchmarks+Baselines** from Vienna

**Provides**: Compute resources for training/fine-tuning models

#### ⚡ **Thinking Machines**
**Provides**: Tinker service with API credits

### Resource Allocation:
- **128 H100 GPUs** via Fields Model Initiative
- **Hundreds of thousands of compute hours** available
- **Up to $400** in Tinker API credits
- Applications for additional resources considered case-by-case

### Addressing Pain Points:
1. **Levels playing field**: Reduces advantage of large labs with significant resources
2. **Accessible to mathematicians**: Abstracts engineering complexity through Tinker

### Application Process:
- Applications open in **December** (details in Kaggle Discussion forum)
- Selection based on **promise to devise strong reasoning models**
- Factors beyond application time may be considered

## About the Hosts

### XTX Markets

**XTX Markets** is a leading algorithmic trading company with:

#### Global Presence:
- **200+ employees** across London, Paris, New York, Mumbai, Yerevan, Singapore
- Provides liquidity in Equity, FX, Fixed Income, and Commodity markets
- Trades **over $250bn per day** across markets

#### Technical Infrastructure:
- **100,000 cores** in research cluster
- **20,000 A/V100 GPUs** (and growing)
- **390 petabytes** of usable storage
- **7.5 petabytes** of RAM
- Advanced technological infrastructure at the crossover of finance and technology

#### Philanthropy Focus:
- **Math and science education** and research
- Academic sanctuaries
- Carbon removal
- Employee matching programme
- **Over £100mn donated** since 2017
- Established as a major donor in the UK and globally

---

*Last updated: March 1, 2026*