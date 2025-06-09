# [No Idea!](https://www.hackerrank.com/challenges/no-idea/problem)

**Status:** Accepted
**Score:** 50.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
# Read input values
n, m = map(int, input().split())  # Read n and m
arr = list(map(int, input().split()))  # Read array elements
A = set(map(int, input().split()))  # Read liked numbers
B = set(map(int, input().split()))  # Read disliked numbers

# Initialize happiness
happiness = 0

# Calculate happiness
for num in arr:
    if num in A:
        happiness += 1
    elif num in B:
        happiness -= 1

# Output the final happiness score
print(happiness)

