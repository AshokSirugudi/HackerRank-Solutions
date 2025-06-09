# [Alien Username](https://www.hackerrank.com/challenges/alien-username/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

# Number of usernames
n = int(input().strip())

# Regular expression pattern
pattern = r'^[_\.][0-9]+[a-zA-Z]*_?$'

# Compile the regex pattern for efficiency
compiled_pattern = re.compile(pattern)

# Process each username
for _ in range(n):
    username = input().strip()
    if compiled_pattern.fullmatch(username):
        print("VALID")
    else:
        print("INVALID")


