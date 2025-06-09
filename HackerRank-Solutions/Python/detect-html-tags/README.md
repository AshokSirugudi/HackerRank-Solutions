# [Detect HTML Tags](https://www.hackerrank.com/challenges/detect-html-tags/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import re

n = int(input())
tags = set()

for _ in range(n):
    line = input()
    # Regex to capture tag names
    found_tags = re.findall(r'<\s*/?\s*([a-zA-Z0-9]+)', line)
    for tag in found_tags:
        tags.add(tag)

# Sort lex order
sorted_tags = sorted(tags)

# Print as semicolon-separated
print(';'.join(sorted_tags))

