# [Lists](https://www.hackerrank.com/challenges/python-lists/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** python3

---

## Solution Code

```python
if __name__ == '__main__':
    N = int(input())  # Number of commands
    list_ = []  # Initialize an empty list

    for _ in range(N):
        entry = input().split()  # Read input and split into list
        command = entry[0]  # Extract command name

        if command == "insert":
            list_.insert(int(entry[1]), int(entry[2]))
        elif command == "append":
            list_.append(int(entry[1]))
        elif command == "remove":  # Fixed typo (was "entry")
            list_.remove(int(entry[1]))
        elif command == "pop":
            list_.pop()
        elif command == "print":
            print(list_)  
        elif command == "sort":
            list_.sort()
        elif command == "reverse":
            list_.reverse()

