# [IP Address Validation](https://www.hackerrank.com/challenges/ip-address-validation/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import re

# Pre-compiled regex patterns
ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$')
ipv6_pattern = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')

n = int(input())
for _ in range(n):
    line = input().strip()
    if ipv4_pattern.match(line):
        print("IPv4")
    elif ipv6_pattern.match(line):
        print("IPv6")
    else:
        print("Neither")

