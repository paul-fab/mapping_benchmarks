"""Fix the broken 6.2 JSON response (multi-paragraph executive_summary split into separate strings)."""
import json

raw = open("output/research/_raw_6.2.txt", "r", encoding="utf-8").read()

# The problem: executive_summary is split across two "strings" separated by ,\n\n
# Line 5 ends with: ...settings.",
# Line 7 starts with: "The field...
# This creates invalid JSON - two strings where there should be one.
# Fix by finding the break point and merging.

lines = raw.split("\n")
print(f"Total lines: {len(lines)}")
print(f"Line 5 (end): ...{lines[4][-60:]!r}")
print(f"Line 6: {lines[5]!r}")
print(f"Line 7 (start): {lines[6][:60]!r}")

# Reconstruct: merge line 5 + newlines + line 7 into a single string value
# Remove the trailing ", from line 5 and the leading " from line 7
fixed_lines = []
i = 0
while i < len(lines):
    if i == 4:  # Line 5 (0-indexed = 4)
        # Remove trailing ",
        merged = lines[4].rstrip()
        if merged.endswith('",'):
            merged = merged[:-2]  # Remove the ","
        elif merged.endswith('"'):
            merged = merged[:-1]  # Remove the "
        # Add literal \n\n
        merged += "\\n\\n"
        # Skip blank line 6
        # Add line 7 content, removing leading whitespace and opening quote
        line7 = lines[6].lstrip()
        if line7.startswith('"'):
            line7 = line7[1:]  # Remove opening "
        merged += line7
        fixed_lines.append(merged)
        i = 7  # Skip lines 5, 6, 7 (we consumed them)
    else:
        fixed_lines.append(lines[i])
        i += 1

fixed = "\n".join(fixed_lines)

try:
    parsed = json.loads(fixed)
    print(f"\nParsed successfully! Keys: {list(parsed.keys())}")
    print(f"Executive summary length: {len(parsed['executive_summary'])} chars")
    
    with open("output/research/category_6.2_analysis.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print("Saved to category_6.2_analysis.json")
except json.JSONDecodeError as e:
    print(f"\nStill failed: {e}")
    # Save the attempted fix for inspection
    with open("output/research/_fix_attempt_6.2.txt", "w", encoding="utf-8") as f:
        f.write(fixed)
    print("Saved fix attempt to _fix_attempt_6.2.txt")
