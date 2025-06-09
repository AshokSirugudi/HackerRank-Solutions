# [Finding the percentage](https://www.hackerrank.com/challenges/finding-the-percentage/problem)

**Status:** Accepted
**Score:** 10.0
**Submitted At:** N/A
**Language:** pypy3

---

## Solution Code

```python
if __name__ == '__main__':
    n = int(input())  # Number of students
    student_marks = {}  # Dictionary to store marks

    for _ in range(n):
        entry = input().split()  # Read input line and split
        name, scores = entry[0], list(map(float, entry[1:]))  # Extract name and scores
        student_marks[name] = scores  # Store in dictionary

    query_name = input()  # Student name to query
    avg_score = sum(student_marks[query_name]) / len(student_marks[query_name])  # Compute average
    print(f"{avg_score:.2f}")  # Print result with 2 decimal places

