import re
import copy

#https://adventofcode.com/2023/day/13
# Find the row # or col # where the board is mirrored
# Pt 2 is to find the row/col which mirrors with 1 single difference (a smudge)

input_str = """....####.#####...
..##..###.##.##.#
..##..###.##.##.#
....####.#####...
.....#.####.#.#.#
###.#####.####...
.#...#..##.#..###
##.....#.#.###...
..##.##..#..###..
####.#.#...#.##..
##.###..#.#....##
...##...#..##..#.
..#.####.##......
##.######....####
....#.#..#####..."""

maps = input_str.split("\n\n")

def get_col(rows, avoid=None):
    for x in range(1,len(rows[0])):
        is_mirror = True
        failures = 0
        for y, row in enumerate(rows):
            left = "".join(reversed(row[:x]))
            right = row[x:]
            if len(left) > len(right):
                for i, val in enumerate(left[:len(right)]):
                    if right[i] != val:
                        failures += 1
                if failures > 1:
                    is_mirror = False
                    break
            else:
                for i, val in enumerate(right[:len(left)]):
                    if left[i] != val:
                        failures += 1
                if failures > 1:
                    is_mirror = False
                    break
        if failures == 1 and is_mirror:
            return x    
    return None     

def get_row(rows, avoid=None):
    for y, _ in enumerate(rows[:-1]):
        left = list(reversed(rows[:y+1]))
        right = rows[y+1:]
        failures = 0
        if len(left) > len(right):
            for i, val in enumerate(left[:len(right)]):
                for j, valval in enumerate(val):
                    if right[i][j] != valval:
                        failures += 1
            if failures > 1:
                continue
        else:
            for i, val in enumerate(right[:len(left)]):
                for j, valval in enumerate(val):
                    if left[i][j] != valval:
                        failures += 1
            if failures > 1:
                continue
        if failures == 1:
            return y+1
    return None

total = 0
for m in maps:
    rows = m.split("\n")

    col = get_col(rows)
    if not col:
        total += 100 * get_row(rows)
    else:
        total += col

print(total)


    







    

