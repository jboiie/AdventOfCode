from itertools import product

INPUT_PATH = r"C:\Programming\Projects\advent-of-code\D10\input.txt"


def parse_input():
    machines = []

    with open(INPUT_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            # --------------------------------------------
            # LAST PART IS GOAL COUNTS: "{26,3,1}"
            # Remove { } then split by comma
            # --------------------------------------------
            gc_raw = parts[-1].strip()
            if gc_raw.startswith("{") and gc_raw.endswith("}"):
                gc_raw = gc_raw[1:-1]  # remove {}
            goal_counts = list(map(int, gc_raw.split(",")))

            # --------------------------------------------
            # BUTTONS ARE ALL ELEMENTS BETWEEN FIRST & LAST
            # Could be:
            #   (0)
            #   (0,1)
            #   SINGLE_NUMBER
            # --------------------------------------------
            raw_buttons = parts[1:-1]
            buttons = []

            for b in raw_buttons:
                b = b.strip()

                if b.startswith("(") and b.endswith(")"):
                    inside = b[1:-1]
                    mask = 0
                    if inside != "":
                        nums = inside.split(",")
                        for num in nums:
                            mask |= 1 << int(num)
                    buttons.append(mask)
                else:
                    # single bit index
                    bit = int(b)
                    buttons.append(1 << bit)

            machines.append((goal_counts, buttons))

    return machines


def solve_machine_bruteforce(goal_counts, buttons):
    """
    Brute force for testing. This is slow.
    """
    B = len(buttons)
    num_bits = len(goal_counts)
    
    best = None
    max_sum = sum(goal_counts) + 10
    
    # Generate all combinations up to max_sum
    from itertools import combinations_with_replacement
    
    for total_presses in range(1, max_sum + 1):
        # Partition total_presses among B buttons
        for partition in product(range(total_presses + 1), repeat=B):
            if sum(partition) != total_presses:
                continue
            
            produced = [0] * num_bits
            for j, presses in enumerate(partition):
                mask = buttons[j]
                for bit in range(num_bits):
                    if mask & (1 << bit):
                        produced[bit] += presses
            
            if produced == goal_counts:
                return total_presses
    
    return 0


def solve_machine(goal_counts, buttons):
    """
    Solve using simple iteration with early termination.
    """
    B = len(buttons)
    num_bits = len(goal_counts)
    
    best = None
    max_sum = sum(goal_counts) + 10
    
    # Try all combinations of button presses
    for counts in product(range(max_sum + 1), repeat=B):
        total = sum(counts)
        
        # Skip if worse than current best
        if best is not None and total >= best:
            continue
        
        # Calculate produced counts
        produced = [0] * num_bits
        for j, presses in enumerate(counts):
            if presses == 0:
                continue
            mask = buttons[j]
            for bit in range(num_bits):
                if mask & (1 << bit):
                    produced[bit] += presses
        
        # Check if matches goal
        if produced == goal_counts:
            best = total
    
    return 0 if best is None else best


def part2():
    machines = parse_input()
    total = 0
    for goal_counts, buttons in machines:
        total += solve_machine(goal_counts, buttons)
    return total


if __name__ == "__main__":
    print(part2())
