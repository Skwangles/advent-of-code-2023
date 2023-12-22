import copy
import numpy as np

# day 18 - https://adventofcode.com/2023/day/19
#
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
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

class Part:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)
    
    def add(self):
        return self.x + self.m + self.a + self.s


class Chain:
    def __init__(self, checks, operator, num, result):
        self.checks = checks
        self.operator = operator
        self.num = int(num)
        self.result

    def is_pass(self, part):
        match self.checks:
            case "x":
                match self.operator:
                    case "<":
                        return self.result if part.x < self.num else False
                    case ">":
                        return self.result if part.x > self.num else False
            case "m":
                match self.operator:
                    case "<":
                        return self.result if part.m < self.num else False
                    case ">":
                        return self.result if part.m > self.num else False
                        
            case "a":
                match self.operator:
                    case "<":
                        return self.result if part.a < self.num else False
                    case ">":
                        return self.result if part.a > self.num else False
                        
            case "s":
                match self.operator:
                    case "<":
                        return self.result if part.s < self.num else False
                    case ">":
                        return self.result if part.s > self.num else False

class Proc:
    def __init__(self, chain, default):
        self.chain = chain
        self.default = default

    def eval(self, part):
        for c in self.chain:
            ret = c.is_pass(part)
            if ret:
                return ret # either R, A, or an ID


parts = input_str.strip().split("\n\n")

chains = {}

# Build chains
for r in parts[0].split("\n"):
    id_chain = r.split("{")
    id = id_chain[0]
    chains = id_chain[1][:-1].split(",")
    chain_list = []
    default = None
    for c in chains:
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


accepted = 0
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







