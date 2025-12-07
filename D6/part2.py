import math

def read_grid(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        # Important: keep trailing spaces, only strip newline
        lines = [line.rstrip("\n") for line in f]

    if not lines:
        return []

    width = max(len(line) for line in lines)
    # Pad all lines to the same width with spaces
    grid = [line.ljust(width) for line in lines]
    return grid

def is_blank_column(grid, col):
    # A column is blank if *every* row has a space in this column
    return all(row[col] == " " for row in grid)

def split_into_problems(grid):
    """
    Split columns into problems using completely blank columns as separators.
    Returns a list of lists of column indices, each list = one problem.
    """
    height = len(grid)
    width = len(grid[0])

    problems = []
    current = []

    for col in range(width):
        if is_blank_column(grid, col):
            # Separator: end current problem (if any)
            if current:
                problems.append(current)
                current = []
        else:
            current.append(col)

    if current:
        problems.append(current)

    return problems

def parse_problem(grid, cols):
    """
    For a given list of column indices (one problem),
    extract:
      - the operator ('+' or '*')
      - the list of numbers (one per column, read top->bottom excluding last row)
    """
    height = len(grid)

    # Find operator from bottom row within these columns
    operators = set()
    for c in cols:
        ch = grid[height - 1][c]
        if ch in "+*":
            operators.add(ch)

    if len(operators) != 1:
        raise ValueError(f"Expected exactly one operator per problem, got {operators}")

    op = operators.pop()

    numbers = []
    for c in cols:
        # Collect digits from all rows except the last (operator row)
        digits = []
        for r in range(height - 1):
            ch = grid[r][c]
            if ch.isdigit():
                digits.append(ch)

        if digits:
            num = int("".join(digits))
            numbers.append(num)

    if not numbers:
        raise ValueError("Problem has no numbers!")

    return op, numbers

def evaluate_problem(op, numbers):
    if op == "+":
        return sum(numbers)
    elif op == "*":
        return math.prod(numbers)
    else:
        raise ValueError(f"Unknown operator: {op}")

def main():
    grid = read_grid("input.txt")
    if not grid:
        print("Empty input.")
        return

    problems = split_into_problems(grid)

    # We’re supposed to read problems right-to-left,
    # but since we only sum their results, order doesn't matter.
    total = 0
    for cols in problems:
        op, numbers = parse_problem(grid, cols)
        result = evaluate_problem(op, numbers)
        total += result

    print(total)

if __name__ == "__main__":
    main()
