# https://adventofcode.com/2023/day/7

input_str = """..."""

from collections import Counter

PRIORITY_ORDER = "J23456789TQKA"
# five of a kind
# four of a kind
# full house - 3 and 2
# three of a kind
# two pair
# one pair
# high card

# highest first card wins on match, then second, etc.

rows =  list(map(lambda x: x.split(" "), input_str.split("\n")))

def calculate_hand(hand):
    number_version = tuple(PRIORITY_ORDER.index(v) for v in hand[0])
    j_num = sum(v == 0 for v in number_version)
    hand_type = list(map(lambda x: x[1], Counter([x for x in number_version if x != 0]).most_common()))

    if hand_type == []:
        hand_type = [j_num]
    else:
        hand_type[0] += j_num
    match hand_type:
        case [1,1,1,1,1]:
            return (1 ,number_version)
        case [2,1,1,1]:
            return (2, number_version)
        case [2,2,1]:
            return (3, number_version)
        case [3,1,1]:
            return (4, number_version)
        case [3, 2]:
            return (5, number_version)
        case [4, 1]:
            return (6, number_version)
        case [5]:
            return (7, number_version)
    print(hand_type)
    print("No match")
    return None

final_order = sorted((calculate_hand(h), int(h[1]), h[0]) for h in rows)
total = 0
for i,v in enumerate(final_order):
    total += v[1] * (i+1)
print(total)