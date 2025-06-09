# [Find a string](https://www.hackerrank.com/challenges/find-a-string/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
def count_substring(string, sub_string):
    count=0
    for i in range(0,len(string)):
        if string[i:].startswith(sub_string):
            count=count+1
    return count
    
    
    return


