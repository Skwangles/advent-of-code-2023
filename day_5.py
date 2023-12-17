from multiprocessing import Pool

# https://adventofcode.com/2023/day/5

input_str = """..."""


from collections import deque

#seed-to-soil map:
#soil-to-fertilizer map:
#fertilizer-to-water map:
#light-to-temperature map:
#temperature-to-humidity map:
#humidity-to-location map:

class SeedMap:
    def __init__(self, a, b, c):
        self.dest = a
        self.start = b
        self.end = b + (c-1)
        self.length = c
        

class Seed:
    def __init__(self, a, b):
        self.start = a
        self.end = b
    
    def toStr(self):
        return str(self.start) + "-" + str(self.end)


# Mapping
def convert_range(seed, maps, history):
    if len(maps) == 0:
        print(history + [seed.start])
        return seed.start # found bottom, return min

    current_map = maps[0]
    
    outputs = []

    for m in current_map:
        if (seed.start > m.end):
            # Check larger ranges
            continue

        ### Do not modify seed val 
        if seed.end < m.start:
            outputs.append(convert_range(seed, maps[1:], history + ["<:" + seed.toStr()]))
            return min(outputs) 

        if seed.start < m.start:
            # Trim overhang
            new_seed = Seed(seed.start, m.start-1)
            outputs.append(convert_range(new_seed, maps[1:], history + ["~>:" + new_seed.toStr()]))
            seed = Seed(m.start, seed.end)

        ### Inside range ###
        if seed.end <= m.end:
            # Completely inside range
            diff = m.dest - m.start
            new_seed = Seed(seed.start + diff, seed.end + diff)
            outputs.append(convert_range(new_seed, maps[1:], history + ["i:" + new_seed.toStr() ]))
            return min(outputs) 

        if seed.end > m.end:
            # Overhang right
            diff = m.dest - m.start
            new_seed = Seed(seed.start + diff, m.end + diff)
            outputs.append(convert_range(new_seed, maps[1:], history + ["p:" + new_seed.toStr()]))
            
            # continue with remainder
            seed = Seed(m.end + 1, seed.end)
        
    return min(outputs + [convert_range(seed, maps[1:], history + ["o:" + seed.toStr()])]) 


def str_obj(strs):
    parts = strs.split(" ")
    return SeedMap(int(parts[0]), int(parts[1]), int(parts[2]))

def split_and_separate(strs):
    arr = strs.split("\n")[1:]
    parts = map(str_obj, arr)
    values = list(parts)
    return sorted(values, key=lambda x: x.start)

groups = input_str.split("\n\n")

seeds = list(map(lambda x: int(x), groups[0].split(" ")[1:]))
grouped_seeds = []
for i in range(0, len(seeds), 2):
    grouped_seeds.append(Seed(seeds[i], seeds[i] + seeds[i+1] - 1 ))

seed_soil = split_and_separate(groups[1])
soil_fertilizer = split_and_separate(groups[2])
fertilizer_water = split_and_separate(groups[3])
water_light = split_and_separate(groups[4])
light_temp = split_and_separate(groups[5])
temp_humidity = split_and_separate(groups[6])
humidity_location = split_and_separate(groups[7])


pipeline = [seed_soil, soil_fertilizer, fertilizer_water, water_light, light_temp, temp_humidity, humidity_location]


def process_group(group):
    lowest = convert_range(group, pipeline, [group.toStr()])
    print("#########",lowest, "########")
    return lowest

with Pool(8) as p:
    print(sorted(p.map(process_group, grouped_seeds)))


    

