import re
import copy

input_str = """..."""

# https://adventofcode.com/2023/day/14
# Ball roll simulation - O are balls that roll, and are hit by # immovable blocks
# Simulate a cyclic motion of roll north, west, south, east - 1 billion times

rows = input_str.split("\n")

# make the strings mutable
for y in range(len(rows)):
    rows[y] = list(rows[y])

visited_states = {}

def go_north(rows):
    for x in range(len(rows[0])):
        top = 0
        for y, row in enumerate(rows):
            match row[x]:
                case "#":
                    top = y+1
                case "O":
                    if top < y:
                        rows[top][x] = "O"
                        rows[y][x] = "."                
                        top += 1
                    elif top == y:
                        top += 1
                case ".":
                    continue
    #print_map(rows)
    return go_west(rows)

def go_east(rows):
    for y, row in enumerate(rows):
        top = len(row) - 1
        for x in reversed(range(len(rows[0]))): 
            match row[x]:
                case "#":
                    top = x-1
                case "O":
                    if top > x:
                        rows[y][top] = "O"
                        rows[y][x] = "."                
                        top -= 1
                    elif top == x:
                        top -= 1
                case ".":
                    continue
    #print_map(rows)
    return rows   

def go_south(rows):
    for x in range(len(rows[0])):
        top = len(rows) -1
        for y in reversed(range(len(rows))):
            match rows[y][x]:
                case "#":
                    top = y-1
                case "O":
                    if top > y:
                        rows[top][x] = "O"
                        rows[y][x] = "."                
                        top -= 1
                    elif top == y:
                        top -= 1
                case ".":
                    continue
    #print_map(rows)
    return go_east(rows)

def go_west(rows):
    for y, row in enumerate(rows):
        top = 0
        for x in range(len(rows[0])):
            
            match row[x]:
                case "#":
                    top = x+1
                case "O":
                    if top < x:
                        rows[y][top] = "O"
                        rows[y][x] = "."                
                        top += 1
                    elif top == x:
                        top += 1
                case ".":
                    continue
    #print_map(rows)
    return go_south(rows)

def print_map(rows):
    for r in rows:
        print("".join(r))
    print("--")

def count_load(rows):
    total = 0
    for x in range(len(rows[0])):
        for y, row in enumerate(rows):
            match row[x]:
                case "O":
                    total += len(rows) - y
    return total
    
def get_id(rows):
    output = ""
    for r in rows:
        output += "".join(r) + "/"
    return output

count = 0
print_map(rows)
end_val = 1_000_000_000

while count < end_val:

    print((count+1)/(end_val))

    curr_id = get_id(rows)

    if curr_id in visited_states:
        # If we have already seen a state, we have a loop we can jumpforward in
        print("jump forward")
        jump_forward = count - visited_states[curr_id][1]
        if count + jump_forward + 1 < end_val:
            rows = visited_states[curr_id][0]
            count += jump_forward + 1
            continue

    rows = go_north(rows)

    visited_states[curr_id] = [copy.deepcopy(rows), count]

    count += 1

    
print(count_load(rows))



    







    

