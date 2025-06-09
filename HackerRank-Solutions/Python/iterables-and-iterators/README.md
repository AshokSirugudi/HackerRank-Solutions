# [Iterables and Iterators](https://www.hackerrank.com/challenges/iterables-and-iterators/problem)

**Status:** Accepted
**Score:** 40.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from itertools import combinations

N= int(input())
L= input().split()
K= int(input())

C =  list(combinations(L,K))
F = filter(lambda c: 'a' in c,C)
print("{0:3}".format(len(list(F))/len(C)))


