# [Merge the Tools!](https://www.hackerrank.com/challenges/merge-the-tools/problem)

**Status:** Accepted
**Score:** 40.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
def merge_the_tools(string, k):
    # your code goes here
    for i in range(0,len(string),k):
        unique=''
        for c in string[i:i+k]:
            if (c not in unique):
                unique = unique + c
        print(unique)
        
    


