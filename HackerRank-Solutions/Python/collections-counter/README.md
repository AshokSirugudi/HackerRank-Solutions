# [collections.Counter()](https://www.hackerrank.com/challenges/collections-counter/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
import collections
numShoes= int(input())
shoes = collections.Counter(map(int,input().split()))

numCust=int(input())

income=0
for i in range(numCust):
    size,price=map(int,input().split())
    if shoes[size]:
        income= income+price #adding to the income 
        shoes[size] -=1 #decreasing the count for the size

print(income)

