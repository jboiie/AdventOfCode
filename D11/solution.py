#!/usr/bin/python3
import os
from functools import cache

# Path to input.txt in the same directory as solution.py
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(DIR, "input.txt")

with open(INPUT_PATH, "r") as f:
    D = f.read()

E = {}
for line in D.splitlines():
    x, ys = line.split(':')
    ys = ys.split()
    E[x] = ys

@cache
def part1(x):
    if x == 'out':
        return 1
    return sum(part1(y) for y in E[x])

@cache
def part2(x, seen_dac, seen_fft):
    if x == 'out':
        return 1 if seen_dac and seen_fft else 0

    total = 0
    for y in E[x]:
        total += part2(
            y,
            seen_dac or y == "dac",
            seen_fft or y == "fft"
        )
    return total

print(part1("you"))
print(part2("svr", False, False))
