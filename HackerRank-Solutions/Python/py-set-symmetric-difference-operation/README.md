# [Set .symmetric_difference() Operation](https://www.hackerrank.com/challenges/py-set-symmetric-difference-operation/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
num1=int(input())
english_student = set(input().split())
num2=int(input())
french_student= set(input().split())

print(len(english_student.symmetric_difference(french_student)))


