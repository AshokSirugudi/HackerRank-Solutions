# [itertools.combinations_with_replacement()](https://www.hackerrank.com/challenges/itertools-combinations-with-replacement/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from itertools import combinations_with_replacement

s,k = input().split()




for c in combinations_with_replacement(sorted(s), int(k)):
    print("".join(c))
    

