# [sWAP cASE](https://www.hackerrank.com/challenges/swap-case/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
def swap_case(s):
    output= ''
    for char in s:
        if char.isupper():
            output  += char.lower()
        else:
            output += char.upper()
            
    return output
        
        
    return


