# [Collections.namedtuple()](https://www.hackerrank.com/challenges/py-collections-namedtuple/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import namedtuple
n=int(input())
Info= namedtuple('Info',input().split())
s=''

total_marks= 0

for _ in range(n):
    values = input().split()
    student = Info(*values)
    total_marks= total_marks+int(student.MARKS)

print(round(total_marks/float(n),2))

