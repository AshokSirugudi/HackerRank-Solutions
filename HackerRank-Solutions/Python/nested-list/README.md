# [Nested Lists](https://www.hackerrank.com/challenges/nested-list/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** pypy3

---

## Solution Code

```python
if __name__ == '__main__':
    list_ = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        list_.append([name,score])
        
 # Get the second lowest score
    second_lowest = sorted(set(score for _, score in list_))[1]

    # Get names of students with the second lowest score
    result = sorted([name for name, score in list_ if score == second_lowest])

    # Print each name on a new line
    print('\n'.join(result))



