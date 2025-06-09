# [Building a Smart IDE: Programming Language Detection](https://www.hackerrank.com/challenges/programming-language-detection/problem)

**Status:** Accepted
**Score:** 30.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import sys
import re

def detect_language(code_lines):
    code = '\n'.join(code_lines)

    # Check for Java
    if re.search(r'\bpublic\s+class\b', code) or 'System.out.println' in code or 'import java' in code:
        return "Java"

    # Check for C
    if '#include' in code or re.search(r'\bint\s+main\s*\(', code) or 'printf' in code or 'scanf' in code:
        return "C"

    # Check for Python
    if re.search(r'\bdef\b', code) or re.search(r'\bprint\b', code) or '#' in code:
        return "Python"

    # Fallback
    return "Unknown"

# Read input
lines = sys.stdin.read().splitlines()
print(detect_language(lines))

