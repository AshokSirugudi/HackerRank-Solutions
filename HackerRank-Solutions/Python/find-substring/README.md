# [Find A Sub-Word](https://www.hackerrank.com/challenges/find-substring/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

# Input sentences
n = int(input())
sentences = [input() for _ in range(n)]

# Combine all sentences into a single text
text = '\n'.join(sentences)

# Input queries
q = int(input())
queries = [input() for _ in range(q)]

# For each query, count subword occurrences
for query in queries:
    # Build regex pattern
    pattern = r'\B' + re.escape(query) + r'\B'
    # Count occurrences
    count = len(re.findall(pattern, text))
    print(count)

