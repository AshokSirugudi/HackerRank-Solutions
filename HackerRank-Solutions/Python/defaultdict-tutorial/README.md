# [DefaultDict Tutorial](https://www.hackerrank.com/challenges/defaultdict-tutorial/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from collections import defaultdict

# number of elements in group A,B
n, m = map(int, input().split())

d = defaultdict(list)  

for i in range(1, n + 1):
    word = input()
    d[word].append(str(i))  

#above loops group A words and stores words position in d[word] 


for _ in range(m):
    query = input()
    print(" ".join(d.get(query, ["-1"])))  

#above queries Group B words- if query exists in d joins with space or returns -1



    

