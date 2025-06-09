# [Designer Door Mat](https://www.hackerrank.com/challenges/designer-door-mat/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
n,m = map(int,input().split())

#defining the pattern 
pattern = [('.|.'*(2*i + 1)).center(m,'-') for i in range(n//2)]
print
print('\n'.join(pattern))
print('WELCOME'.center(m,'-'))
print('\n'.join(pattern[::-1]))

