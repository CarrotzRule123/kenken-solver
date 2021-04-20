import numpy as np

cases = [1, 2, 3]
prev = (0, 0)
string = """1 0 0
0 0 3
3 0 0
"""
puzzle = np.zeros((3, 3))
used = []
for x in range(0, 3):
    used.append([])
    for y in range(0, 3):
        used[x].append([])

parsed = string.splitlines()
for i in range(0, len(parsed)):
    split = parsed[i].split(" ")
    for j in range(0, len(split)):
        puzzle[i][j] = split[j]

def check(row, col, n):
    for i in puzzle[row]:
        if i == n:
            return False
    for i in puzzle[:,col]:
        if i == n:
            return False
    return True


def solve(row, col, n):
    print("Row:",row," Col:",col)
    i, j = prev
    if not n==0:
        return n
    for case in cases:
        if check(row, col, case) and not case in used[row][col]:
            print("Val:",case)
            return case

    # backtrack
    print("Backtrack")
    used[i][j].append(puzzle[i, j])
    puzzle[i, j] = solve(i, j, 0)
    print("Backtrack end")

##for i in range(0, len(puzzle)):
for i in range(0, 1):
    row = puzzle[i]
    for j in range(0, len(row)):
        row[j] = solve(i, j, row[j])
        prev = (i, j)

print(used)
print(puzzle)
