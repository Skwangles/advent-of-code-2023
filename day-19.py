import copy
import numpy as np

# day 18 - https://adventofcode.com/2023/day/19
# This was based very much off the 'seed' planting problem from day 5. I took inspiration for this from network router allow/deny chains.



class Part:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)
    
    def add(self):
        return self.x + self.m + self.a + self.s


class NumRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
class RangedPart:
    def __init__(self, low_x=1, hi_x=4000, low_m=1, hi_m=4000, low_a=1, hi_a=4000, low_s=1, hi_s=4000):
        self.info = {}
        self.info["x"] = NumRange(int(low_x), int(hi_x))
        self.info["m"] = NumRange(int(low_m), int(hi_m))
        self.info["a"] = NumRange(int(low_a), int(hi_a))
        self.info["s"] = NumRange(int(low_s), int(hi_s))
    
    def get_range(self, arr):
        return abs(arr.end - arr.start) +1 # 4000-1 == 3999, but there are 4000 numbers in that range
    
    def __lt__(self, other):
        return (self.info["x"].start,self.info["x"].end,self.info["m"].start,self.info["m"].end,self.info["a"].start,self.info["a"].end,self.info["s"].start,self.info["s"].end) < (other.info["x"].start, other.info["x"].end, other.info["m"].start, other.info["m"].end, other.info["a"].start, other.info["a"].end, other.info["s"].start, other.info["s"].end)
    
    def to_str(self):
        return str(self.info["x"].start) + "-" + str(self.info["x"].end) + ", " + str(self.info["m"].start) + "-" + str(self.info["m"].end) + ", " + str(self.info["a"].start) + "-" + str(self.info["a"].end) + ", " + str(self.info["s"].start) + "-" + str(self.info["s"].end)
    
    def add(self):
        return self.get_range(self.info["x"]) * self.get_range(self.info["m"]) * self.get_range(self.info["a"]) * self.get_range(self.info["s"])


class Chain:
    def __init__(self, checks, operator, num, result):
        self.checks = checks
        self.operator = operator
        self.num = int(num)
        self.result = result

    def is_pass(self, part):
        # Part 1 function
        match self.operator:
            case "<":
                return self.result if part[self.checks] < self.num else False
            case ">":
                return self.result if part[self.checks] > self.num else False
    
    def range_pass(self, part):     
        # part 2 function
        match self.operator:
            case "<":
                if part.info[self.checks].start >= self.num:
                    return False # completely out of range
                
                acc_part = copy.deepcopy(part)
                acc_part.info[self.checks].end = min(part.info[self.checks].end, self.num-1)

                rej_part = None
                if part.info[self.checks].end >= self.num:
                    rej_part = copy.deepcopy(part)
                    rej_part.info[self.checks].start = self.num
                
                return [self.result, acc_part, rej_part]
            case ">":
                if part.info[self.checks].end <= self.num:
                    return False # completely out of range
                
                acc_part = copy.deepcopy(part)
                acc_part.info[self.checks].start = max(acc_part.info[self.checks].start, self.num+1)
                
                rej_part = None
                if part.info[self.checks].start <= self.num:
                    rej_part = copy.deepcopy(part)
                    rej_part.info[self.checks].end = self.num
                
                return [self.result, acc_part, rej_part]

class Proc:
    def __init__(self, chain, default):
        self.chain = chain
        self.default = default

    def eval(self, part):
        for c in self.chain:
            ret = c.is_pass(part)
            if ret:
                return ret # either R, A, or an ID
        return self.default


  
def explore_chain(current: str, rangepart: Part):
    """Uses ranges to explore the possibilities that are accepted/rejected by the chains"""
    global complete_chains
    global chains
    
    # case where a 'self.default' is A/R
    if current == "A":
        complete_chains.append(rangepart)
        print("Accepted", rangepart.to_str())
        return
    elif current == "R":
        return
    
    group = chains[current]
    for c in group.chain:
        if not rangepart:
            print("Consumed")
            return # previous steps completely consumed
        
        res = c.range_pass(rangepart)
        if res:
            match res[0]:
                case "A":
                    print("Accepted", res[1].to_str())
                    complete_chains.append(res[1]) # add accepted part
                    rangepart = res[2]
                case "R":
                    rangepart = res[2] # 'non-passed' part is now being explored
                case _:
                    rangepart = res[2] # 'non-passed' part is now being explored
                    explore_chain(res[0], res[1])

    if rangepart: # default path
        explore_chain(group.default, rangepart) 


########################### - Input - ###################

input_str = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}"""

parts = input_str.strip().split("\n\n")
complete_chains = []
chains: dict[str, Chain] = {}

# Build chains
for r in parts[0].split("\n"):
    id_chain = r.split("{")
    id = id_chain[0]
    chains_str = id_chain[1][:-1].split(",")
    chain_list = []
    default = None
    for c in chains_str:
        if ":" in c:
            info = c.split(":")
            attr = info[0][0]
            op = info[0][1]
            num = info[0][2:]
            result = info[1]
            chain_list.append(Chain(attr, op, num, result))
        else:
            default = c
    if not default:
        raise Exception("No default found")
    chains[id] = Proc(chain_list, default)




is_part1 = True

### ----- Part 1 Solution ------- #
if is_part1:
    accepted = []

    for r in parts[1].split("\n"):
        part = r[1:-1].split(",")
        x = None
        m = None
        a = None
        s = None
        for p in part:
            lttr_num = p.split("=")
            match lttr_num[0]:
                case "x":
                    x = int(lttr_num[1])
                case "m":
                    m = int(lttr_num[1])
                case "a":
                    a = int(lttr_num[1])
                case "s":
                    s = int(lttr_num[1])
        
        part = Part(x, m, a, s)
        current = "in"
        while current != "A" and current != "R":
            group = chains[current]
            res = group.eval(part)
            print(res)
            match res:
                case "A":
                    accepted.append(part)
                    break
                case "R":
                    break
                case _:
                    current = res
                
    total = 0
    for t in accepted:
        total += t.add()  
    print(total)       
else:
    ## Part 2 ##
    explore_chain("in", RangedPart())
    total = 0
    
    for p in sorted(complete_chains):
        total += p.add()
        
    print(total)
