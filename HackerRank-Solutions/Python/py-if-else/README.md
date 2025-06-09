# [Python If-Else](https://www.hackerrank.com/challenges/py-if-else/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
#!/bin/python3

import math
import os
import random
import re
import sys



if __name__ == '__main__':
    n = int(input().strip())

if ((n%2 == 1) or (n%2== 0 and (6<=n<=20))):
    print("Weird")
if (n%2==0) and ((2<=n<=5) or (n>20)):
    print("Not Weird") 

