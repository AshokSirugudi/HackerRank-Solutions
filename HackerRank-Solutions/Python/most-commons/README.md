# [Company Logo](https://www.hackerrank.com/challenges/most-commons/problem)

**Status:** Accepted
**Score:** 30.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
from collections import Counter

try:
    s = input().strip()  # Read input safely
    chars = Counter(s).items()

    for char, n in sorted(chars, key=lambda c: (-c[1], c[0]))[:3]:
        print(char, n)

except EOFError:
    print("No input received")  # Handles missing input

