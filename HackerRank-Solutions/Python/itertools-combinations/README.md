# [itertools.combinations()](https://www.hackerrank.com/challenges/itertools-combinations/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT


from itertools import *

s,k = input().split(' ')
k=int(k)
for l in range(1, k+1):
    for c in combinations(sorted(s),l):
        print(''.join(c))
        

