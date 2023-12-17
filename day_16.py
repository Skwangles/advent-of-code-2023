import re
import copy

# https://adventofcode.com/2023/day/16
# Given a map with mirrors /\ and splitters (|-) where flat edge spawns two beams going outwards from its points
# find how many tiles have been visited.

rows = open("input-16").read()

stack = []

contraption = [r for r in rows.split("\n")]

visited = {}

def get_id(points):
    output = ""
    for val in points:
        output += str(points) + ","
    return output

def get_direct(prev, next):
    if prev[0] - next[0] > 0:
        return "LEFT"
    if prev[0] - next[0] < 0:
        return "RIGHT"
    if prev[1] - next[1] < 0:
        return "DOWN"
    if prev[1] - next[1] > 0:
        return "UP"
    return None
    
def lookup(points):
    try:
        return contraption[points[1]][points[0]]
    except:
        print(points)
        raise Exception("Out of range")

def navigate(prev, next):
    global stack
    global visited
    
    if next == [109, 109]:
        pass

    if next[0] >= len(contraption[0]) or next[0] < 0 or next[1] >= len(contraption) or next[1] < 0:
        return

    id = get_id(next)

    direction = get_direct(prev, next)

    if id in visited:
        if direction in visited[id]:
            return #skip paths we've already explored
        visited[id].append(direction)
    else:
        visited[id] = [direction]

    current = copy.deepcopy(next)

    match direction:
        case "UP":
            match lookup(next):
                case "/":
                    next[0] += 1
                    stack.append([next, current])
                case "\\":
                    next[0] -= 1
                    stack.append([next, current])
                case "-":
                    left = copy.deepcopy(next)
                    right = copy.deepcopy(next)
                    left[0] -= 1
                    right[0] += 1
                    stack.append([left, current])
                    stack.append([right, current])
                case _:
                    next[1] -= 1
                    stack.append([next, current])
        case "DOWN":
            match lookup(next):
                case "/":
                    next[0] -= 1
                    stack.append([next, current])
                case "\\":
                    next[0] += 1
                    stack.append([next, current])
                case "-":
                    left = copy.deepcopy(next)
                    right = copy.deepcopy(next)
                    left[0] -= 1
                    right[0] += 1
                    stack.append([left, current])
                    stack.append([right, current])
                case _:
                    next[1] += 1
                    stack.append([next, current])
        case "LEFT":
            match lookup(next):
                case "/":
                    next[1] += 1
                    stack.append([next, current])
                case "\\":
                    next[1] -= 1
                    stack.append([next, current])
                case "|":
                    up = copy.deepcopy(next)
                    down = copy.deepcopy(next)
                    up[1] -= 1
                    down[1] += 1
                    stack.append([up, current])
                    stack.append([down, current])
                case _:
                    next[0] -= 1
                    stack.append([next, current])
        case "RIGHT":
            match lookup(next):
                case "/":
                    next[1] -= 1
                    stack.append([next, current])
                case "\\":
                    next[1] += 1
                    stack.append([next, current])
                case "|":
                    up = copy.deepcopy(next)
                    down = copy.deepcopy(next)
                    up[1] -= 1
                    down[1] += 1
                    stack.append([up, current])
                    stack.append([down, current])
                case _:
                    next[0] += 1
                    stack.append([next, current])

# [[next, previous]....] - previous helps determine the 'direction', next is the only one of the two that is visited
# The following generates all possible entry points from the edge
initial_config = [[[0, y],[-1,y]] for y in range(len(contraption))]
initial_config += [[[len(contraption[0])-1, y],[len(contraption[0]),y]] for y in range(len(contraption))]
initial_config += [[[x, 0],[x, -1]] for x in range(len(contraption[0]))]
initial_config += [[[x, len(contraption)-1],[x, len(contraption)]] for x in range(len(contraption[0]))]

# Find the best entry point
best_num = -1
best = []

for config in initial_config:
    stack = []
    print("Testing:", config)
    visited = {}
    stack.append(config)
    while len(stack) > 0:
        next_point = stack.pop()
        navigate(next_point[1], next_point[0])

    if len(visited) > best_num:
        best_num = len(visited)
        best = [config]
    elif len(visited) == best_num:
        best.append(config)
    print(best_num)
    
print(best)
print(best_num)


    







    

