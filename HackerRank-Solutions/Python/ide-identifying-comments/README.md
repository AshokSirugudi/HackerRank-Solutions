# [Building a Smart IDE: Identifying comments](https://www.hackerrank.com/challenges/ide-identifying-comments/problem)

**Status:** Accepted
**Score:** 20.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

import sys
import re

def extract_comments(lines):
    inside_multiline = False

    for line in lines:
        stripped_line = line.lstrip()

        # Case: Inside multi-line comment, print until we see */
        if inside_multiline:
            print(stripped_line)
            if '*/' in stripped_line:
                inside_multiline = False
            continue

        # Case: Multi-line comment starting and ending on the same line
        multi_inline = re.findall(r'/\*.*?\*/', stripped_line)
        if multi_inline:
            for comment in multi_inline:
                print(comment)
            # Remove inline multi-line comment and check for single-line after
            stripped_line = re.sub(r'/\*.*?\*/', '', stripped_line)

        # Case: Multi-line comment starts, doesn't end on same line
        if '/*' in stripped_line and '*/' not in stripped_line:
            idx = stripped_line.index('/*')
            print(stripped_line[idx:])
            inside_multiline = True
            continue

        # Case: Single-line comment //
        single_comment = re.search(r'//.*', stripped_line)
        if single_comment:
            print(single_comment.group())

# Read input
lines = sys.stdin.read().splitlines()
extract_comments(lines)

