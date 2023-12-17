# https://adventofcode.com/2023/day/10
# This one gives us a map of 'pipes' that go in a loop, e.g. | = vertical pipe, J = West to North Pipe, 7 = West to South, etc.
# Have to then figure out what is inside/outside the loop

input_str = """..."""

rows =  list(input_str.split("\n"))

CONNECTS_TO_RIGHT = "7-J"
CONNECTS_TO_LEFT = "F-L"
CONNECTS_TO_TOP = "|F7"
CONNECTS_TO_BOTTOM = "J|L"

DOWN = +1
UP = -1
LEFT = -1
RIGHT = +1

def is_connected(x_y, compare_x_y):
    if compare_x_y[0] - x_y[0] == -1:
        #left
        if lookup(compare_x_y) in CONNECTS_TO_LEFT:
            return True
    elif compare_x_y[0] - x_y[0] == 1:
        #right
        if lookup(compare_x_y) in CONNECTS_TO_RIGHT:
            return True
    elif compare_x_y[1] - x_y[1] == -1:
        # above
        if lookup(compare_x_y) in CONNECTS_TO_TOP:
            return True
    elif compare_x_y[1] - x_y[1] == 1:
        # below
        if lookup(compare_x_y) in CONNECTS_TO_BOTTOM:
            return True
    return False
    
def lookup(coords, rows=rows):
    return rows[coords[1]][coords[0]]

def id(x_y):
    return str(x_y[0]) + "_" + str(x_y[1])

def get_neighbours(point, rows):
    neighbours = []

    ABOVE = [point[0], point[1]-1]
    if lookup(point) in "|JLS" and id(ABOVE) not in visited and point[1] != 0 and lookup(ABOVE) in CONNECTS_TO_TOP:
        neighbours.append(ABOVE)

    BELOW = [point[0], point[1]+1]
    if lookup(point) in "|F7S" and id(BELOW) not in visited  and point[1] < len(rows) - 1 and lookup(BELOW) in CONNECTS_TO_BOTTOM:
        neighbours.append(BELOW)
    
    LEFT = [point[0]-1, point[1]]
    if lookup(point) in "-J7S" and id(LEFT) not in visited  and point[0] != 0 and lookup(LEFT) in CONNECTS_TO_LEFT:
        neighbours.append(LEFT)
    
    RIGHT = [point[0]+1, point[1]]
    if lookup(point) in "FL-S" and id(RIGHT) not in visited  and point[0] < len(rows[0]) - 1 and lookup(RIGHT) in CONNECTS_TO_RIGHT:
        neighbours.append(RIGHT)
    
    return neighbours

def get_neighbours_asterix(point):
    neighbours = []

    ABOVE = [point[0], point[1]-1]
    if is_inside_bounds(ABOVE, path_only) and lookup(ABOVE, path_only) == "*":
        neighbours.append(ABOVE)

    BELOW = [point[0], point[1]+1]
    if is_inside_bounds(BELOW, path_only) and lookup(BELOW, path_only) == "*":
        neighbours.append(BELOW)
    
    LEFT = [point[0]-1, point[1]]
    if is_inside_bounds(LEFT, path_only) and lookup(LEFT, path_only) == "*":
        neighbours.append(LEFT)
    
    RIGHT = [point[0]+1, point[1]]
    if is_inside_bounds(RIGHT, path_only) and lookup(RIGHT, path_only) == "*":
        neighbours.append(RIGHT)
    
    return neighbours

def is_inside_bounds(point, rows=rows):
    if point[0] < 0 or point[0] >= len(rows[0]):
        return False
    
    if point[1] < 0 or point[1] >= len(rows[0]):
        return False
    
    return True
  
def discover_pipe_path(is_ast=False, rows=rows):
    # manually observing S's location I know the cell below connects to S (my dataset had no 'decoy' connections)
    current = [s[0], s[1]+1] 
    steps = 1

    while current != "S":
        if id(current) in visited:
            return steps
        
        visited[id(current)] = steps

        for neighbour in get_neighbours(current, rows):
            if id(neighbour) in visited:
                continue
            current = neighbour
            break

        steps += 1
        print(steps)

def convert_non_path_to_asterisx(rows):
    return [[(rows[y][x] if (id([x, y]) in visited) else '*') for x in range(len(rows[0]))] for y in range(len(rows))]

def flood_fill_asertix(point):
    # Explore all "*" connected

    if id(point) in visited_asterix or lookup(point, path_only) != "*":
        return
    visited_asterix[id(point)] = 1

    # Mark it as visited
    path_only[point[1]][point[0]] = "X"
    print_map(path_only)

    for neighbour in get_neighbours_asterix(point):
        if id(neighbour) in visited_asterix:
            continue
        flood_fill_asertix(neighbour)

def get_cell_to_the_right(point, previous):
    # Based on the pipe's orientation, get cell directly to the right
    point_to_check = None
    match lookup(point):
        case "|":
            if previous[1] - point[1] == -1:
                # going down - get 'left'
                point_to_check =  [point[0]+LEFT, point[1]]
            else:
                #going up - get 'right'
                point_to_check = [point[0]+RIGHT, point[1]]
        case "-":
            if previous[0] - point[0] == -1:
                # going right - get 'below'
                point_to_check =  [point[0], point[1] + DOWN]
            else:
                #going left - get 'above'
                point_to_check =  [point[0], point[1] + UP]
        case "7":
            if previous[1] != point[1]:
                # going left - get 'above' and 'right' - I only check 1 as a hacky optimisation and it works
                point_to_check =  [point[0], point[1] + UP]
        case "L":
            if previous[1] != point[1]:
                # going left - get 'below' and 'left' - I only check 1 as a hacky optimisation and it works
                point_to_check =  [point[0] + LEFT, point[1]]
        case "J":
            if previous[1] == point[1]:
                # going up - get 'right' and 'below' - I only check 1 as a hacky optimisation and it works
                point_to_check =  [point[0], point[1] + DOWN]
        case "F":
            if previous[1] == point[1]:
                # going down - get 'left' and 'above' - I only check 1 as a hacky optimisation and it works
                point_to_check =  [point[0] + LEFT, point[1]]
    return point_to_check if is_inside_bounds(point, path_only) else None

def explore_asterisx_to_right_of_path():
    global visited
    visited = {}
    current = [s[0], s[1]+1] # I know below is part of the loop through manual observation
    steps = 1
    previous = s
    while current != "S":
        if id(current) in visited:
            return steps
        
        visited[id(current)] = steps

        right = get_cell_to_the_right(current, previous)
        if right:
            flood_fill_asertix(right)

        for neighbour in get_neighbours(current, path_only):
            if id(neighbour) in visited:
                continue
            previous = current
            current = neighbour
            break

        steps += 1
        print(steps)

def print_map(map_obj):
    for p in map_obj:
        print("".join(p))


## ----- Logic Entry ------
        
# find S
s = [-1,-1]
for y in range(len(rows)):
    for x in range(len(rows[0])):
        if rows[y][x] == "S":
            s = [x, y]
            break

if s == [-1, -1]:
    raise Exception("S not found")

visited = {id(s): 1}
points = []
total_inside = 0
visited_asterix = {}
path_only = None

discover_pipe_path()
path_only = convert_non_path_to_asterisx(rows)
explore_asterisx_to_right_of_path()

print_map(path_only)
print(len(visited_asterix))



    

