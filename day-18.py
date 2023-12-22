import copy
import numpy as np

# day 18 - https://adventofcode.com/2023/day/18/input
# you must solve this using Picks Theorem, and the Shoelace formula
# The main issue arises because the 'coordinates' are usually seen as in the top left of the square in the 'shoelace' formula, so we can't just use that raw.
# Picks formula takes into account the border and can give us the # of points (1m^2 squares) on the border, and inside.

input_str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

### Modify manually to change ###
is_part1 = True 

class Instruct:
    def __init__(self, dir, num, colour):
        self.dir = dir
        self.num = int(num)
        self.colour = colour

class Point:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour


rows = input_str.strip().split("\n")

instructions = []



for r in rows:
    dir_num_col = r.split(" ")

    if is_part1:
        instructions.append(Instruct(dir_num_col[0], dir_num_col[1], dir_num_col[2]))
    else:
        dir_lttrs = "RDLU"
        hex_broken = int(dir_num_col[2][2:7], 16)
        instructions.append(Instruct(dir_lttrs[int(dir_num_col[2][-2])], hex_broken, "")) 


shape_points = [Point(0,0, instructions[0].colour)]

x = 0
y = 0

border = 0

for ins in instructions:
    # y +/- has been flipped to be consistent with coordinates

    match ins.dir:
        case "R":
            x += ins.num
        case "D":
            y -= ins.num
        case "L":
            x -= ins.num
        case "U":
            y += ins.num
    border += ins.num
    shape_points.append(Point(x, y, ins.colour))

arr = []

abs_val = 0
for i in range(len(shape_points)-1):

    curr = copy.deepcopy(shape_points[i])
    next = copy.deepcopy(shape_points[i+1])

    abs_val += curr.x*-next.y - next.x*-curr.y


def create_map(shape_points):
    global arr
    max_x = copy.deepcopy(max(shape_points, key=lambda p: p.x))
    min_x = copy.deepcopy(min(shape_points, key=lambda p: p.x))
    max_y = copy.deepcopy(max(shape_points, key=lambda p: p.y))
    min_y = copy.deepcopy(min(shape_points, key=lambda p: p.y))

    # convert points to +ve coords
    for p in shape_points:
        p.x -= min_x.x
        p.y -= max_y.y # we have inverted y axis

    arr_x_size = abs(max_x.x - min_x.x)
    arr_y_size = abs(max_y.y - min_y.y)
    arr = [["." for r in range(abs(arr_x_size)+1)] for y in range(abs(arr_y_size)+1)]


def update_map(curr, next, i):
    global arr
    arr[-curr.y][curr.x] = "#"
    y_diff = abs(curr.y - next.y)
    x_diff = abs(curr.x - next.x)
    isYdiff = y_diff != 0
    for i in range(1, y_diff if isYdiff else x_diff):
        if isYdiff:
            if curr.y - next.y > 0:
                arr[-curr.y + i][curr.x] = "#"
            else:
                arr[-curr.y - i][curr.x] = "#"
        else:
            if curr.x - next.x > 0:
                arr[-curr.y][curr.x - i] = "#"
            else:
                arr[-curr.y][curr.x + i] = "#"

# total = 0
# for r in arr:
#     for x in r:
#         if x == "#":
#             total += 1

print(0.5 * abs(abs_val) - (border//2) + 1 + border )

# for r in arr:
#     print("".join(r))



