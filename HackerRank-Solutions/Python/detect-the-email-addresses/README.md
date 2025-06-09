# [Detect the Email Addresses](https://www.hackerrank.com/challenges/detect-the-email-addresses/problem)

**Status:** Accepted
**Score:** 15.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import re

# Step 1: Read inputs
n = int(input())
lines = []
for _ in range(n):
    lines.append(input())

text = "\n".join(lines)

# Step 2: Regex pattern
pattern = r'[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*@[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)*'

# Step 3: Find all email matches
emails = re.findall(pattern, text)

# Step 4: Unique emails
unique_emails = sorted(set(emails))

# Step 5: Print
print(";".join(unique_emails))

