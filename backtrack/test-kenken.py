import numpy as np

# define constants
PRINT = False
SIZE = 4
STRING = "1400000032104020"
ANS = "1432234132144123"
CASES = np.arange(1, SIZE + 1)
puzzle = np.zeros((SIZE, SIZE))
used = []
for x in range(0, SIZE):
    used.append([])
    for y in range(0, SIZE):
        used[x].append([])

# parse string
count = 0
for i in range(0, SIZE):
    for j in range(0, SIZE):
        puzzle[i][j] = STRING[count]
        count += 1
print(puzzle, "\n")

# constraints checker
#TODO: check boxes
def check(row, col, n):
    for i in puzzle[row]:
        if i == n:
            return False
    for i in puzzle[:,col]:
        if i == n:
            return False
    return True

# get cell value
def peek(x, y):
    if x == SIZE:
        print(puzzle)
        print("status", verify())
        exit()
    return puzzle[x, y]

# get next cell value
def step(x, y):
    if(y == SIZE - 1):
        return (x + 1, 0)
    else:
        return (x, y + 1)

# get previous cell value
def previous(x, y):
    if(y == 0):
        return (x - 1, SIZE - 1)
    else:
        return (x, y - 1)

# print function
def log(*args):
    if PRINT:
        print(*args)

# verify
def verify():
    ans = ""
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            ans += str(int(puzzle[i][j]))
    return ans == ANS

# recursive solver function
def solve(pos, n, prev):
    x1, y1 = pos
    x2, y2 = step(x1, y1)
    log("solving", x1, y1)
    if not n==0:
        solve((x2, y2), peek(x2, y2), (x1, y1))
    for case in CASES:
        if check(x1, y1, case) and not case in used[x1][y1]:
            # assign value
            log("==>", x1, y1, "value", case)
            puzzle[x1, y1] = case
            # recurse
            solve((x2, y2), peek(x2, y2), (x1, y1))

    # backtrack
    log("backtrack at", x1, y1)
    x0, y0 = previous(x1, y1)
    used[x0][y0].append(peek(x0, y0))
    puzzle[x0, y0] = solve((x0, y0), 0, (x0, y0))

# main
solve((0, 0), puzzle[0, 0], (0, 0))
