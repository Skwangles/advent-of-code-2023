#https://adventofcode.com/2023/day/6

input_str = """Time: 45977295
Distance: 305106211101695"""

rows = input_str.split("\n")
times = rows[0].split(" ")[1:]
distance = rows[1].split(" ")[1:]

counts = []
for i,v in enumerate(times):
    success = 0
    race_time = int(v)
    dist = int(distance[i])
    for charge_time in range(1, race_time):
        time_left = race_time - charge_time
        dist_travelled = time_left * charge_time
        if dist_travelled > dist:
            success += 1
    counts.append(success)
 
def multiplyList(myList):
 
    # Multiply elements one by one
    result = 1
    for x in myList:
        result = result * x
    return result
    
print(multiplyList(counts))