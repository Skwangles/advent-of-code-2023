import re
import copy

# https://adventofcode.com/2023/day/15
# Labels of a 'lens' in a box between 0-255 (HASH func gives this by lbl). Num is the focal size 1-9, =/- is 'add/update' or 'remove' - Order is important
# Then calculate focal strength by a specific algo

# input_str = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
# rows = input_str.split(",")
rows = open("input.csv").readline().split(",")

def HASH(my_str):
    current_val = 0
    for c in my_str:
        current_val += ord(c)
        current_val *= 17
        current_val %= 256
    return current_val

def is_in(lbl, arr):
    return lbl in list(map(lambda v: v[0], arr))

boxes = [[] for x in range(256)]
lenses = [{} for x in range(256)]

def remove_lens(lbl):
    global boxes
    boxnum = HASH(lbl)
    if lbl in boxes[boxnum]:
        boxes[boxnum].remove(lbl)

def add_lens(lbl, num):
    global boxes
    global lenses
    boxnum = HASH(lbl)
    if lbl not in boxes[boxnum]:
        boxes[boxnum].append(lbl)
    lenses[boxnum][lbl] = int(num)

def focusing_power(boxnum):
    total = 0
    box = boxes[boxnum]
    for i in boxes[boxnum]:
        total += (1 + boxnum) * (box.index(i) + 1) * lenses[boxnum][i]
    return total

total = 0
for r in rows:
    
    lbl = None
    num = None
    if "=" in r:
        lbl = r[:-2]
        num = r[-1]
        add_lens(lbl, num)

    elif "-" in r:
        lbl = r[:-1]
        remove_lens(lbl)

total = 0
for i in range(256):
    total += focusing_power(i)


print(total)


    







    

