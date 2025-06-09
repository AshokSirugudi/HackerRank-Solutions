# [Tuples ](https://www.hackerrank.com/challenges/python-tuples/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** pypy3

---

## Solution Code

```python
if __name__ == '__main__':
    n = int(input())
    integer_list = map(int, input().split())
    integer_list = tuple(integer_list)
    hashed= hash(integer_list)
    print(hashed)

