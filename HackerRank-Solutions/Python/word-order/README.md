# [Word Order](https://www.hackerrank.com/challenges/word-order/problem)

**Status:** Accepted
**Score:** 50.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
# Enter your code here. Read input from STDIN. Print output to STDOUT

from collections import OrderedDict
words = OrderedDict()

for _ in range(int(input())):
    word = input()
    words.setdefault(word,0)
    words[word]+=1
    
print(len(words))
print(*words.values())

    

