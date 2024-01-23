import heapq

DEST = 0
IS_HI = 1
CALLER = 2

class Module:
    def __init__(self, name, dest):
        self.id = name
        self.on = False
        self.inputs = {}
        self.dests = dest
    
    def add_input(self, input):
        self.inputs[input] = False

    def get_packets(self, isHi):
        output = []
        for dest in self.dests:
            output.append(create_packet(dest, isHi, self.id))
        return output


class FlipFlop(Module):
    def __init__(self, name, dest):
        self.on = False
        super().__init__(name, dest)

    def call(self, isHi, caller):
        if not isHi:
            self.on = not self.on
            return super().get_packets(self.on)
        return []


class Conjunction(Module):
    def __init__(self, name, dest):
        super().__init__(name, dest)

    def call(self, isHi, caller):
        self.inputs[caller] = isHi

        hasFalse = False
        for i in self.inputs:
            if not self.inputs[i]:
                hasFalse = True
                break
    
        # if not 'all hi' then send a high pulse
        return super().get_packets(hasFalse)

class Broadcaster(Module):
    def __init__(self, name, dest):
        super().__init__(name, dest)

    def call(self, isHi="", caller=""):
        return super().get_packets(False)

def create_packet(dest, state, caller):
    return [dest, state, caller]


modules = {}
strs = """%vh -> qc, rr
&pb -> gf, gv, vp, qb, vr, hq, zj
%zj -> kn, pb
%mm -> dj
%gp -> cp
&dc -> ns
%qc -> gp
%dx -> fq, dj
%tg -> nl, ks
%pr -> nl
%gx -> xf
%hd -> lt, nl
%dq -> dj, jc
%ht -> jv
%bs -> pb, rd
&nl -> ks, cq, tc, xf, gx, hd, lt
&dj -> dc, fq, jz, ht, zs, jc
&rr -> gp, rv, jt, qc, sq
%vr -> qb
%jz -> dj, ht
%hq -> nx
%cf -> jg, rr
%hj -> cf, rr
%mt -> rr
%sq -> rr, vh
%jg -> rr, pd
%gf -> gv
%xv -> dj, dx
%rh -> nl, gx
broadcaster -> hd, zj, sq, jz
%jv -> dj, zs
%rd -> vs, pb
%pd -> rr, mt
&rv -> ns
&vp -> ns
%vs -> pb
%nx -> pb, bs
%zp -> mm, dj
&ns -> rx
%lt -> rh
%pf -> pr, nl
%tc -> qz
%xz -> dj, zp
%qb -> hq
%rl -> pf, nl
%fq -> xz
%kn -> pb, xn
%xf -> tg
%qz -> nl, rl
%ks -> tc
%jt -> kb
%jc -> xv
%kb -> hj, rr
%zs -> dq
%gv -> vr
&cq -> ns
%cp -> rr, jt
%xn -> pb, gf"""

lo = 0
hi = 0

queue = []
rows = strs.strip().split("\n")

# Initalise modules
for line in rows:
    parts = line.strip().split("->")
    dests = parts[1].strip().split(", ")

    if line[0] == "%": 
        modules[parts[0][1:].strip()] = FlipFlop(parts[0].strip()[1:],dests)
    elif line[0] == "&":
        modules[parts[0][1:].strip()] = Conjunction(parts[0].strip()[1:], dests)
    else:
        # broadcaster
        modules[parts[0].strip()] = Broadcaster(parts[0].strip(), dests)


# Add inputs to modules
for line in rows:
    parts = line.strip().split("->")
    dests = parts[1].strip().split(", ")
    for dest in dests:
        if dest in modules:
            modules[dest].add_input(parts[0].strip()[1:])

def part2():
    items = {
    "cq": -1,
    "dc": -1,
    "vp": -1,
    "rv": -1
    }
    visited = set()
    count = 0
    while True:
        count += 1
        queue = []
        # press button (add broadcaster)
        for i in modules["broadcaster"].call(False, "broadcaster"):
            queue.append(i)

        while len(queue) > 0:
            next = queue.pop(0)

            if next[CALLER] in items and next[IS_HI] and count != 1:
                if next[CALLER] not in visited:
                    items[next[CALLER]] = count
                visited.add(next[CALLER])
                if len(visited) == 4:
                    return items

            if next[DEST] == 'rx' :
                if not next[IS_HI]:
                    return count
                continue

            for i in modules[next[DEST]].call(next[IS_HI], next[CALLER]):
                queue.append(i)

def part1():
    lo = 0
    hi = 0
    for i in range(1000):
        queue = []
        lo += 1 # add 'lo' for the 'button' send
        # press button (add broadcaster)
        for i in modules["broadcaster"].call(False, "broadcaster"):
            queue.append(i)

        while len(queue) > 0:
            next = queue.pop(0)

            if next[IS_HI]:
                hi += 1
            else:
                lo += 1

            if next[DEST] == 'rx':
                continue

            for i in modules[next[DEST]].call(next[IS_HI], next[CALLER]):
                queue.append(i)

    return lo * hi

print("Pt1", part1())
print("Pt2 - LCM these:", part2())