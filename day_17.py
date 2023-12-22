import copy
import heapq

# https://adventofcode.com/2023/day/17
# This is not a complete solution - I managed to solve part 1 fine, but part 2 was a bit finicky. I got 'close enough' in part 2, that a little guess and check got me the answer
# (I was 8 off), the current state of the solution is my attempt to get the solution always. Bit of a shame, but a good challenge

rows = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

COST = 0
COUNT = 1
POINT = 2
DIR = 3
PATH = 4

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

name_lookup = {(0,-1): "UP",(0,1): "DOWN", (-1,0): "LEFT", (1,0): "RIGHT"}

DEFAULT_COST = 999_999_999
DEFAULT_COUNT = 0
DEFAULT_PREV = None

board = [r for r in rows.strip().split("\n")]
board_clone = [[*r] for r in board]

END = [len(board[0])-1, len(board)-1]

def get_dir_char(dir):
    match dir:
        case "LEFT":
            return "<"
        case "RIGHT":
            return ">"
        case "DOWN":
            return "v"
        case "UP":
            return "^"
    return "*"

def reconstruct_path(current):
    current = (current[POINT], current[DIR])
    total_path = [current]
    while get_id(current) in visited:
        current = visited[get_id(current)]
        total_path.insert(0, current)
    return total_path

def print_best(path, board=board, board_clone=copy.deepcopy(board_clone), ast=True):
    print(path)
    points = list(map(lambda x: x[0], path))
    print(points)
    if ast:
        for x in range(len(board[0])):
            for y in range(len(board)):
                if [x,y] not in points:
                    board_clone[y][x] = "*"

    for val in path:
        board_clone[val[0][1]][val[0][0]] = get_dir_char(val[1])

    for r in board_clone:
        print("".join(r))
    print()

def print_board(path, board=board, board_clone=copy.deepcopy(board_clone), ast=True):
    for r in board_clone:
        print("".join(r))
    print()

def get_id(point):
    output = ""
    for p in point:
        output += str(p) + ","
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

def lookup_board(point):
    return int(board[point[1]][point[0]])

def explore_around(point, dir, heat, low, high, ):
    neighbours = []

    dirs = {LEFT, RIGHT, UP, DOWN}
    dir_ignore = {}

    match dir:
        case "UP":
            dir_ignore = {UP, DOWN}
        case "DOWN":
            dir_ignore = {UP, DOWN}
        case "LEFT":
            dir_ignore = {LEFT, RIGHT}
        case "RIGHT":
            dir_ignore = {LEFT, RIGHT}

    for next_dir in dirs-dir_ignore:
        loss = heat
        x_mod, y_mod = next_dir
        for i in range(1, high+1):
            new_point = [point[0] + x_mod*i, point[1] + y_mod*i]
            if not is_point_outside(new_point):
                loss += lookup_board(new_point)
                if i >= low:
                    neighbours.append(package_tuple(new_point, point[COST] + loss, name_lookup[next_dir], 1))
            

    return neighbours

def is_point_outside(point):
    return point[0] < 0 or point[0] >= len(board[0]) or point[1] < 0 or point[1] >= len(board)

visited = set()

def package_tuple(point, cost, dir, count, path=[]):
    return (cost, count, point, dir, path)

def a_star(start, goal=END):
    global board_clone
    global visited
    global best

    open_set = []
    heapq.heappush(open_set, package_tuple(start, 0, "RIGHT", 0))
    heapq.heappush(open_set, package_tuple(start, 0, "DOWN", 0))

    while len(open_set) > 0:
        print(len(open_set), len(visited))
        current = heapq.heappop(open_set)

        if current[POINT] == goal:
            return current

        if get_id((current[POINT], current[DIR])) in visited:
                continue
        visited.add(get_id((current[POINT], current[DIR])))

        for neighbor in explore_around(current[POINT], current[DIR], current[COST], 4, 10):
            heapq.heappush(open_set, package_tuple(neighbor[POINT], neighbor[COST], neighbor[DIR], neighbor[COUNT], current[PATH] + [(neighbor[POINT], neighbor[DIR])]))

    return None


results = a_star([0,0], END)
print(results[COST])






    







    

