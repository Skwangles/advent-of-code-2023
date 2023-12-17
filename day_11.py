import re

# https://adventofcode.com/2023/day/11
# Galaxys are shown. Empty rows expand by a certain amount Find shortest distance between all pairings 

expansion_rate = 999_999

input_str = """..."""

rows = input_str.split("\n")

galaxies = []
for y, row in enumerate(rows):
    for x, c in enumerate(row):
        if c == "#":
            galaxies.append([x,y])

rows_to_expand = []
cols_to_expand = []

# Find empty Rows and columns
# Rows
for y, row in enumerate(rows):
    if re.match("^[.]+$", row):
        rows_to_expand.append(y)

# Cols
for x in range(len(rows[0])):
    is_empty = True
    for y, row in enumerate(rows):
        if row[x] != ".":
            is_empty = False
    if is_empty:
        cols_to_expand.append(x)

# Expand universe - Universes expand by 1 million in empty rows
expanded_x_universe = ["" for y in range(len(rows))]
for y, row in enumerate(rows):

    for i, cell in enumerate(list(row)):
        if i in cols_to_expand:
            expanded_x_universe[y] += expansion_rate * "."
        expanded_x_universe[y] += cell

expanded_universe = []
for y, row in enumerate(expanded_x_universe):
    if y in rows_to_expand:
        for i in range(expansion_rate):
            expanded_universe.append(None)
    expanded_universe.append(row)

points = []

# Record all the #
for y, row in enumerate(expanded_universe):
    if row == None: # <-- empty row
        continue
    print("Checking row", y)
    for x, cell in enumerate(row):
        if cell == "#":
            points.append([x, y])

# Get all pairs 
point_pairs = [(a, b) for idx, a in enumerate(points) for b in points[idx + 1:]]

# Shortest distances on a grid moving as the rook == x diff + y diff
sum_of_dist = 0
for pair in point_pairs:
    y_travel = abs(pair[0][1] - pair[1][1])
    x_travel = abs(pair[0][0] - pair[1][0])
    sum_of_dist += y_travel + x_travel

print(sum_of_dist)






    

