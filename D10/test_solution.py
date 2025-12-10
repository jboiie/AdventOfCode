from itertools import product

# Test with the first machine manually
goal_counts = [26, 32, 28, 47, 23, 20]
buttons_raw = ["(2,4)", "(3,4)", "(0,2,3,5)", "(0,1,2,3)", "(1,3,4,5)"]

# Parse buttons
buttons = []
for b in buttons_raw:
    b = b.strip()
    if b.startswith("(") and b.endswith(")"):
        inside = b[1:-1]
        mask = 0
        if inside != "":
            nums = inside.split(",")
            for num in nums:
                mask |= 1 << int(num)
        buttons.append(mask)

print(f"Buttons: {[bin(b) for b in buttons]}")
print(f"Goal: {goal_counts}")

B = len(buttons)
best = None
max_sum = sum(goal_counts)

# Try brute force with smaller upper bound
for counts in product(range(min(100, max_sum + 1)), repeat=B):
    total = sum(counts)
    
    if best is not None and total >= best:
        continue
    
    produced = [0] * len(goal_counts)
    for j, presses in enumerate(counts):
        if presses == 0:
            continue
        mask = buttons[j]
        for bit in range(len(goal_counts)):
            if mask & (1 << bit):
                produced[bit] += presses
    
    if produced == goal_counts:
        print(f"Found solution: {counts}, total = {total}")
        best = total
        break

if best:
    print(f"Result: {best}")
else:
    print("No solution found within bounds")
