# [Write a function](https://www.hackerrank.com/challenges/write-a-function/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** pypy3

---

## Solution Code

```python
def is_leap(year):
    leap = False
    
    # Write your logic here
    if (year <= 100000 and year >= 1900):
        leap = False
        if(year%4 == 0 and ((year%100 != 0) or (year%400 == 0 ))):
            leap = True
            
         
    return leap


