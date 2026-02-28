# AIMO Progress Prize 3 - Dataset Description

## 📊 Dataset Overview

The competition data comprises **110 mathematics problems** similar in style to those of the **AIME** (American Invitational Mathematics Examination).

### Key Characteristics:
- **Answer format**: Non-negative integer between **0 and 99999** (inclusive)
- **Difficulty range**: National Olympiad → International Mathematical Olympiad (IMO)
- **Content**: Text-only with mathematical notation in **LaTeX**
- **Geometry**: No diagrams used (text descriptions only)

> 📖 For detailed notational conventions, see the **Overview** → *Note on Language and Notation* section.

## 🎯 Problem Distribution

### Dataset Structure:

| Component | Size | Purpose |
|-----------|------|---------|
| **Public Test Set** | 50 problems | Leaderboard scoring during competition |
| **Private Test Set** | 50 problems | Final evaluation after competition ends |
| **Reference Data** | 10 problems | Practice & understanding (with full solutions) |
| **Total** | **110 problems** | Complete competition dataset |

### Balancing Criteria:
- ✅ **Difficulty**: Evenly distributed across skill levels
- ✅ **Subject areas**: Balanced representation of mathematical domains
- ✅ **Similar distributions**: Public and private sets have comparable difficulty profiles

## 💻 Competition Data & API

> ⚠️ **Important**: This is a **Code Competition**. You must use the provided **Python evaluation API**.

### Submission Process:
1. **API Usage**: Test set served question-by-question in **random order**
2. **Demo Reference**: Follow the example in notebook: **"AIMO 3 Submission Demo"**
3. **Placeholder Data**: Visible `test.csv` contains non-representative placeholder problems
4. **Actual Scoring**: Placeholder data replaced with real test data during evaluation

### 🔄 API Workflow:
```
Your Submission → Python API → Random Problem Order → Predictions → Scoring
```

## 🔒 Private Set Rerun Protocol

### Security Measures:
Due to the **limited number of problems**, special precautions secure the test set against probing:

#### During Competition:
- Test set comprises **only the 50 public problems**
- No access to private set problems

#### After Competition Ends:
- **All submissions rerun twice** on the 50 private set problems
- Final score = **average accuracy** across both runs
- Must complete **both reruns successfully** or submission receives no score

### 🛡️ Submission Robustness Requirements:
- **Unexpected inputs**: Handle edge cases gracefully
- **Runtime management**: Stay within time limits
- **Memory usage**: Avoid memory overflow
- **Error handling**: Robust to various problem formats

> ⚠️ **Critical**: A submission that fails either private set rerun will **not be scored**.

## 📁 Data Files

### File Structure:

| File | Content | Description |
|------|---------|-------------|
| **`reference.csv`** | 10 problems | Practice problems with full solutions available |
| **`test.csv`** | 50 problems | **Placeholder only** - replaced during scoring |
| **`sample_submission.csv`** | Sample format | Template for proper submission formatting |

> 💡 **Note**: The problems visible in `test.csv` are **only placeholders** to help with submission development.

## 📋 Data Schema

### Field Definitions:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| **`id`** | String | Unique problem identifier | `"problem_001"` |
| **`problem`** | String | LaTeX statement of the mathematical problem | `"Find the value of $x^2 + y^2$..."` |
| **`answer`** | Integer | Solution (range: 0-99999 inclusive) | `42`, `1337`, `99999` |

### Answer Format Details:
- **Range**: `0 ≤ answer ≤ 99999`
- **Type**: Integer only (no decimals, fractions, or expressions)
- **Modulo operations**: Explicitly stated in problem when required
- **Basic computations**: May involve modular arithmetic

## 📖 Reference Materials

### Available Resources:
- **Reference Problems PDF**: Complete solutions for all 10 reference problems
- **LaTeX Notation Guide**: Detailed conventions in Overview document
- **Submission Demo**: Working example notebook
- **Sample Submission**: Properly formatted submission template

### 📚 Recommended Study Approach:
1. **Study reference problems** and their solutions thoroughly
2. **Practice with API** using the demo notebook
3. **Test submission format** with sample file
4. **Understand LaTeX conventions** from the notation guide
5. **Develop robust error handling** for unexpected inputs

---

*Dataset prepared for AIMO Progress Prize 3 - March 2026*