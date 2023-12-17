import re
import copy

# https://adventofcode.com/2023/day/12
# Find all permuations of a pattern (? is wildcard) that matches the pattern of # blocks (1,2 = block of 1 #, a space of any size, block of 2 #)

input_str = """?????#?#?.?#?#. 7,3
#??#?#.?.?????? 6,1,5"""

rows = input_str.split("\n")


counted_variations = {}

solved_permuations = {}

def generate_valid_pattern(pattern:str, nums=[], prefix:str = "", paused=False):
    """
    Dyanmic Programming solution - 
    """
    global valid_combos
    global counted_variations
    global solved_permuations

    unique_key = str((pattern, nums))

    output = 0

    if unique_key in solved_permuations:
        return solved_permuations[unique_key]
    
    if (len(nums) == 0 or (len(nums) == 1 and nums[0] == 0)) and "#" not in pattern:
        prefix = prefix + "." * len(pattern)
        if prefix not in counted_variations:
            output += 1 #success!
    
    elif (len(nums) == 0 or (len(nums) == 1 and nums[0] == 0)) or len(pattern) == 0:
        pass

    elif nums[0] == 0:
        if len(nums) == 1:
            output += generate_valid_pattern(pattern[1:] if len(pattern) > 0 else "", [], prefix=prefix+".", paused=True)
        
        elif pattern[0] in "?.":
            output += generate_valid_pattern(pattern[1:] if len(pattern) > 0 else "", nums[1:] if len(nums) > 0 else [], prefix=prefix+".", paused=True)

    elif pattern[0] in "#":
        nums[0] = nums[0] - 1
        output += generate_valid_pattern(pattern[1:] if len(pattern) > 0 else "", copy.deepcopy(nums), prefix=prefix+"#")
    
    elif pattern[0] in "?":

        if paused:
            # case its a "."
            next_pattern = pattern[1:] if len(pattern) > 0 else []
            output += generate_valid_pattern(next_pattern, copy.deepcopy(nums), prefix=prefix+".", paused=True)

        # case its a "#"
        nums[0] = nums[0] - 1
        output += generate_valid_pattern(pattern[1:] if len(pattern) > 0 else "", copy.deepcopy(nums), prefix=prefix+"#")
    
    # '.' = next
    elif not paused and nums[0] != 0:
        pass

    else:
        output += generate_valid_pattern(pattern[1:] if len(pattern) > 0 else "", copy.deepcopy(nums), prefix=prefix+".", paused=True)
    
    add_output_to_solved_permuations(unique_key, output)
    return output

def add_output_to_solved_permuations(key, ans):
    global solved_permuations
    if key in solved_permuations:
        return
    solved_permuations[key] = ans

REPEAT_ROWS = 5
valid_combos = 0
vals = []
for row in rows:
    # reset visited
    solved_permuations = {}
    pattern_blocks = row.split(" ")
    block_sizes = list(map(lambda x: int(x), pattern_blocks[1].split(",")))

    pattern = "?".join([pattern_blocks[0] for x in range(REPEAT_ROWS)])

    valid_combos += generate_valid_pattern(pattern, block_sizes*REPEAT_ROWS, paused=True)

print(valid_combos)







    

