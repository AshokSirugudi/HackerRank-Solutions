# [Detect HTML Attributes](https://www.hackerrank.com/challenges/html-attributes/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import re
import sys

html = sys.stdin.read()

pattern = re.compile(r'<(\w+)([^>]*)>')
tags = {}

for tag, attr_str in pattern.findall(html):
    attrs = re.findall(r'(\w+)\s*=\s*([\'"]).*?\2', attr_str)
    attr_names = sorted(set(name for name, _ in attrs))
    if tag not in tags:
        tags[tag] = attr_names
    else:
        tags[tag] = sorted(set(tags[tag] + attr_names))

for tag in sorted(tags.keys()):
    print(f"{tag}:{','.join(tags[tag])}")


    

