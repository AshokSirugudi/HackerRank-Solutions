# [Find the Runner-Up Score!  ](https://www.hackerrank.com/challenges/find-second-maximum-number-in-a-list/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** pypy3

---

## Solution Code

```python
if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    print(sorted(list(set(arr)))[-2])

