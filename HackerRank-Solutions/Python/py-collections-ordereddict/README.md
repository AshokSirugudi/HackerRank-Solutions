# [Collections.OrderedDict()](https://www.hackerrank.com/challenges/py-collections-ordereddict/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from collections import OrderedDict
d= OrderedDict()

for _ in range(int(input())):
    item, space, quantity = input().rpartition(' ')
    d[item] = d.get(item,0)+int(quantity)

for item, quantity in d.items():
    print(item,quantity)
    

