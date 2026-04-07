import json
import os

def check_results():
    filepath = os.path.join(os.path.dirname(__file__), 'batch_results.jsonl')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    print(f"--- Checking {filepath} ---")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if idx >= 2: # Check just the first 2 lines
                break
                
            try:
                obj = json.loads(line)
                key = obj.get('key', 'Unknown Key')
                print(f"\n[{idx+1}] Original Key: {key}")
                
                # Check if response succeeded
                if 'response' not in obj or 'candidates' not in obj['response']:
                    print("  [ERROR] No valid response/candidates found for this row.")
                    continue
                    
                raw_text = obj['response']['candidates'][0]['content']['parts'][0]['text']
                
                # The model probably returned wrapped json (e.g. ```json ... ```) or raw json
                raw_text = raw_text.strip()
                if raw_text.startswith('```json'):
                    raw_text = raw_text[7:]
                if raw_text.endswith('```'):
                    raw_text = raw_text[:-3]

                # Quick hack: models often fail to double-escape LaTeX strings in JSON properly
                # Let's fix common backslashes before loading
                # (This just replaces literal \ with \\, except for standard json escapes)
                # But it's easier to strictly re-encode it for display
                # We will import re
                # The most bulletproof way to fix LLM JSON returning unescaped \log, \frac, \boxed, etc.
                # is to replace ALL backslashes with double backslashes, then fix the ones that were
                # supposed to be structural JSON escapes (like \" or \n)
                fixed_text = raw_text.replace('\\', '\\\\')
                fixed_text = fixed_text.replace('\\\\"', '\\"')
                fixed_text = fixed_text.replace('\\\\n', '\\n')
                fixed_text = fixed_text.replace('\\\\t', '\\t')
                fixed_text = fixed_text.replace('\\\\r', '\\r')
                
                try:
                    data = json.loads(fixed_text)
                except json.JSONDecodeError as e:
                    print(f"  [WARNING] JSON decode failed even after patching: {e}")
                    print(fixed_text[:500])
                    continue
                
                print(f"  Summary: {data.get('original_problem_summary')}")
                
                variants = data.get('variants', [])
                print(f"  Generated Variants Count: {len(variants)}")
                
                if len(variants) > 0:
                    v1 = variants[0]
                    print(f"\n  -- Variant 1 ({v1.get('variant_id', 'N/A')}) --")
                    print(f"  Problem: {v1.get('problem')}")
                    sol = v1.get('solution', '')
                    print(f"  Solution:\n{sol}\n")
                    print(f"  Reasoning: {v1.get('variant_reasoning')}")
                    
                if len(variants) > 1:
                    v2 = variants[1]
                    print(f"\n  -- Variant 2 ({v2.get('variant_id', 'N/A')}) --")
                    print(f"  Problem: {v2.get('problem')}")
                    sol = v2.get('solution', '')
                    print(f"  Solution:\n{sol}\n")
            except Exception as e:
                print(f"  [ERROR] Failed to parse JSON on line {idx+1}: {e}")

if __name__ == "__main__":
    check_results()
