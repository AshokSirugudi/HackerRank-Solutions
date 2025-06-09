# [Validating Email Addresses With a Filter ](https://www.hackerrank.com/challenges/validate-list-of-email-address-with-filter/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
def fun(s):
    # return True if s is a valid email, else return False
    # using regex expression
    import re
    pattern = re.compile(r"^[\w-]+@[0-9a-zA-Z]+\.[a-zA-Z]{1,3}$")
    return pattern.match(s)
    


