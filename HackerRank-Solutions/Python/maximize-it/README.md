# [Maximize It!](https://www.hackerrank.com/challenges/maximize-it/problem)

**Status:** Accepted
**Score:** 50.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from itertools import product

K,M = map(int,input().split())
N = (list(map(int,input().split()))[1:] for _ in range(K))

results = map(lambda x: sum(i**2 for i in x)%M, product(*N))

print(max(results))

