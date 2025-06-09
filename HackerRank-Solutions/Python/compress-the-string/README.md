# [Compress the String! ](https://www.hackerrank.com/challenges/compress-the-string/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from itertools import groupby

print(*[(len(list(c)), int(k)) for k,c  in groupby(input())])


