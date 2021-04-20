import numpy as np

cases = [1, 2, 3]
string = """1 0 0
0 2 0
0 0 3
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

def peek():
    pass

def step(row, col):
    if(col + 1 > 2):
        return (row + 1, 0)
    else:
        return (row, col + 1)


def solve(row, col, n, prev):
    print("solving", row, col)
    if not n==0:
        x, y = step(row, col)
        solve(x, y, puzzle[x, y], (col, row))
    for case in cases:
        if check(row, col, case) and not case in used[row][col]:
            # assi
            print("==>", row, col, "value", case)
            puzzle[row, col] = case
            # recurse
            x, y = step(row, col)
            if(x == 3):
                print(puzzle)
                exit()
            solve(x, y, puzzle[x, y], (row, col))

    # backtrack
    print("backtrack at", row, col)
    i, j = prev
    used[i][j].append(puzzle[i, j])
    #TODO: prev
    puzzle[i, j] = solve(i, j, 0, (i, j))

solve(0, 0, puzzle[0, 0], (0, 0))

print(used)
print(puzzle)
