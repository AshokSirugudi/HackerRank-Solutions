# [Reduce Function](https://www.hackerrank.com/challenges/reduce-function/problem)

**Status:** Accepted
**Score:** 30.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python


def product(fracs):
    t = reduce(lambda x,y:x*y, fracs) 
    # complete this line with a reduce statement
    return t.numerator, t.denominator


