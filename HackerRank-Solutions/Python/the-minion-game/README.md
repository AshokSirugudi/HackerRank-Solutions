# [The Minion Game](https://www.hackerrank.com/challenges/the-minion-game/problem)

**Status:** Accepted
**Score:** 40.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
def minion_game(string):
    # your code goes here
    vowel = ['A','E','I','O','U']
    K=0
    S=0
    for i in range(len(string)):
        if string[i] in vowel:
            K =K + len(string) - i
        else:
            S = S+ len(string) - i

    if S>K: 
        print("Stuart %d" %S)
    elif K>S:
        print("Kevin %d" % K)
    else:
        print("Draw")

