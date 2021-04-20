import numpy as np
import itertools as it
import json

cages = [
    ([(0, 0), (0, 1)], "add", 3),
    ([(0, 2), (1, 2)], "add", 5),
    ([(2, 1), (2, 2)], "add", 4),
    ([(1, 0), (2, 0)], "add", 5),
    ([(1, 1)], "nan", 1)
]
cases = {
    "add3": [(1, 2)],
    "add4": [(1, 3)],
    "add5": [(1, 4), (2, 3)],
}
SIZE = 3
used = []
test = [0]
puzzle = np.zeros((SIZE, SIZE))
for x in range(0, len(cages)):
    used.append([])

# setup functions

def sort_lambda(cage):
    coords, key, val = cage
    if key == "nan":
        return 0
    return len(find_cases(key, val))

def generate_cases():
    for case in cases:
        new = []
        for pair in cases[case]:
            for x in it.permutations(pair):
               new.append(x)
        cases[case] = new

# util functions

def assign(pos, val):
    x, y = pos
    puzzle[x, y] = val

def assign_cage(case, cage):
    for i in range(0, len(case)):
        assign(cage[i], case[i])

def find_cases(key, val):
    return cases[key + str(val)]

def clear_cage(cage):
    for i in range(0, len(cage)):
        x, y = cage[i]
        puzzle[x, y] = 0

# def step()

# main functions

def check(row, col, n):
    for i in puzzle[row, :]:
        if i == n:
            return False
    for i in puzzle[:, col]:
        if i == n:
            return False
    return True

# def check_all(cage, ans, i):
#     for j in range(0, len(cage)):
#         x, y = cage[j]
#         if not check(x, y, ans[j]):
#             return False
#     if ans in used[i]:
#         return False
#     return True

# def solve(i):
#     if(i >= len(cages)):
#         print(puzzle)
#         exit()
#     coords, key, val = cages[i]
#     if key == "nan":
#         assign(coords[0], val)
#         solve(i + 1)

#     ans = find_cases(key, val)
#     for x in range(0, len(ans)):
#         print(key, val, check_all(coords, ans[x], i), ans[x])
#         if check_all(coords, ans[x], i):
#             used[i].append(ans[x])
#             assign_cage(ans[x], coords)
#             solve(i + 1)

#     used[i] = []
#     clear_cage(cages[i - 1][0])
#     solve(i - 1)

def solve(i, j):
    coords, key, val = cages[i]
    if key == "nan":
        assign(coords[0], val)
        solve(i + 1, 0)

    x, y = coords[j]
    # if key =="add":
    cases = np.arange(0, val - 1)
    print(cases)
    for x in range(0, len(cases)):
        print(key, val, check(x, y, cases[x]), cases[x])

    # ans = find_cases(key, val)
    # for x in range(0, len(ans)):
    #     print(key, val, check_all(coords, ans[x], i), ans[x])
    #     if check_all(coords, ans[x], i):
    #         used[i].append(ans[x])
    #         assign_cage(ans[x], coords)
    #         solve(i + 1)

    # used[i] = []
    # clear_cage(cages[i - 1][0])
    # solve(i - 1)

cages = sorted(cages, key=sort_lambda)
solve(0, 0)
print(puzzle)





