from collections import deque
from itertools import product


def read_input():
    with open(r"C:\Programming\Projects\advent-of-code\D10\input.txt", "r") as f:
        return f.read().strip()


def parse_input(data):
    machines = []
    for line in data.splitlines():
        parts = line.split(" ")

        # goal mask (# positions)
        goal_mask = 0
        for i, c in enumerate(parts[0][1:-1]):
            if c == "#":
                goal_mask |= 1 << i

        # goal counters for part 2
        goal_counts = list(map(int, parts[-1][1:-1].split(",")))

        # button masks
        raw = eval("[" + ",".join(parts[1:-1]) + "]")
        buttons = []
        for b in raw:
            m = 0
            if isinstance(b, int):
                m |= 1 << b
            else:
                for bit in b:
                    m |= 1 << bit
            buttons.append(m)

        machines.append((goal_mask, goal_counts, buttons))
    return machines


# ---------------------------
# Part 1
# ---------------------------

def solve_part1_machine(goal_mask, buttons):
    """
    BFS over bitmasks.
    Start at mask 0 and find the minimum presses needed to reach goal_mask.
    """
    q = deque([(0, 0)])   # (mask, steps)
    visited = {0}

    while q:
        cur, steps = q.popleft()

        if cur == goal_mask:
            return steps

        for b in buttons:
            nxt = cur ^ b
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, steps + 1))

    return 0  # unreachable (shouldn't happen per puzzle constraints)


def part1(machines):
    total = 0
    for goal_mask, goal_counts, buttons in machines:
        total += solve_part1_machine(goal_mask, buttons)
    return total


# ---------------------------
# Part 2
# ---------------------------

def solve_part2_machine(goal_counts, buttons):
    """
    Each bit i requires sum_j(x[j] * affects(button_j, bit_i)) == goal_counts[i].
    Try all button press combinations in a small bounded space.
    """
    B = len(buttons)
    max_presses = max(goal_counts)

    best = None

    for counts in product(range(max_presses + 1), repeat=B):
        total = sum(counts)
        if best is not None and total >= best:
            continue

        produced = [0] * len(goal_counts)

        for j, press_count in enumerate(counts):
            mask = buttons[j]
            for bit in range(len(goal_counts)):
                if mask & (1 << bit):
                    produced[bit] += press_count

        if produced == goal_counts:
            best = total

    return best


def part2(machines):
    total = 0
    for goal_mask, goal_counts, buttons in machines:
        total += solve_part2_machine(goal_counts, buttons)
    return total


# ---------------------------
# Main
# ---------------------------

def main():
    data = read_input()
    machines = parse_input(data)

    print("Part 1:", part1(machines))
    print("Part 2:", part2(machines))


if __name__ == "__main__":
    main()
