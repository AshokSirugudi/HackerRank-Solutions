# [Find a Word](https://www.hackerrank.com/challenges/find-a-word/problem)

**Status:** Accepted
**Score:** 15.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

n = int(input())
sentences = [input() for _ in range(n)]
m = int(input())
words = [input() for _ in range(m)]

for word in words:
    count = 0
    # Match word with boundaries OR non-letter/digit/underscore characters
    pattern = re.compile(rf'(?<![\w]){re.escape(word)}(?![\w])')
    for sentence in sentences:
        count += len(pattern.findall(sentence))
    print(count)


