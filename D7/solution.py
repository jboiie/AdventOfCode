def read_grid(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        # Keep all characters except the newline
        lines = [line.rstrip("\n") for line in f]

    # Filter out any completely empty lines, just in case
    lines = [line for line in lines if line]

    if not lines:
        raise ValueError("Input file is empty or only contains blank lines.")

    # Ensure all lines are the same width (typical AoC-style input already is)
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]
    return grid


def find_start(grid):
    for r, row in enumerate(grid):
        c = row.find("S")
        if c != -1:
            return r, c
    raise ValueError("No starting point 'S' found in grid.")


def count_splits(grid):
    rows = len(grid)
    cols = len(grid[0])

    start_r, start_c = find_start(grid)

    splits = 0
    # Set of beam columns at the current row
    beams = {start_c}

    # We process from the row containing 'S' downwards
    for r in range(start_r, rows):
        new_beams = set()

        for c in beams:
            cell = grid[r][c]

            if cell == "^":
                # Beam is stopped and split
                splits += 1
                # Spawn new beams one row below, left and right (if within bounds)
                nr = r + 1
                if nr < rows:
                    if c - 1 >= 0:
                        new_beams.add(c - 1)
                    if c + 1 < cols:
                        new_beams.add(c + 1)
            else:
                # Empty space or 'S' -> beam continues straight down
                nr = r + 1
                if nr < rows:
                    new_beams.add(c)

        beams = new_beams
        if not beams:
            # No more beams in the manifold
            break

    return splits


def main():
    grid = read_grid("input.txt")
    total_splits = count_splits(grid)
    print(total_splits)


if __name__ == "__main__":
    main()
