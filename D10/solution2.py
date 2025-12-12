#!/usr/bin/python3
import os
import z3

# Path to input.txt in the same directory as this script
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(DIR, "input.txt")

with open(INPUT_PATH, "r") as f:
    D = f.read()

total_p2 = 0

for line in D.splitlines():
    line = line.strip()
    if not line:
        continue

    words = line.split()
    # words[0] is the indicator string like "[.##.]" (ignored for part 2)
    buttons = words[1:-1]      # list of "(..)" tokens
    joltage = words[-1]        # "{a,b,c,...}"

    # parse button NS lists
    NS = []
    for button in buttons:
        # button is like "(0,2,3)" or "(3)"
        inner = button[1:-1].strip()
        if inner == "":
            ns = []
        else:
            ns = [int(x) for x in inner.split(',')]
        NS.append(ns)

    # parse joltage requirements {..}
    joltage_inner = joltage[1:-1].strip()
    if joltage_inner == "":
        joltage_ns = []
    else:
        joltage_ns = [int(x) for x in joltage_inner.split(',')]

    # Build Z3 optimization problem:
    # variables: one Int per button, >= 0
    V = [z3.Int(f'B{i}') for i in range(len(buttons))]

    constraints = []
    # For each counter i, sum of V[j] for buttons j that affect i == joltage_ns[i]
    for i in range(len(joltage_ns)):
        terms = []
        for j in range(len(buttons)):
            if i in NS[j]:
                terms.append(V[j])
        # if no button affects this counter, the system is unsatisfiable unless joltage_ns[i]==0
        constraints.append(sum(terms) == joltage_ns[i])

    o = z3.Optimize()
    o.minimize(sum(V))

    for c in constraints:
        o.add(c)
    for v in V:
        o.add(v >= 0)

    res = o.check()
    if res != z3.sat:
        raise RuntimeError(f"Unsatisfiable or solver failed on line: {line}")

    M = o.model()
    # Sum model values for all declared variables (buttons)
    for v in V:
        # some buttons might not appear in model if optimizer sets them to 0 implicitly;
        # using model.eval to safely get value (default 0 if not present via M.get)
        val = M.eval(v, model_completion=True).as_long()
        total_p2 += val

print(total_p2)
