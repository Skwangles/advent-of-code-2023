import copy
import numpy as np

# day 20 - https://adventofcode.com/2023/day/20


class FlipFlop:
    def __init__(self) -> None:
        self.flip = False
    
    def get(self, is_hi):
        if is_hi:
            return None
        self.flip = not self.flip
        return self.flip

class Conjunction:
    
    def __init__(self) -> None:
        self.state = False

input_str = """
"""

parts = input_str.strip().split("\n\n")
