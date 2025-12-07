def read_grid(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        # Keep spaces, strip only newline
        lines = [line.rstrip("\n") for line in f]

    if not lines:
        raise ValueError("Input file is empty.")

    width = max(len(line) for line in lines)
    # Pad all lines to same width so indexing is safe
    grid = [line.ljust(width) for line in lines]
    return grid


def find_start(grid):
    for r, row in enumerate(grid):
        c = row.find("S")
        if c != -1:
            return r, c
    raise ValueError("No starting point 'S' found in grid.")


def count_timelines(grid):
    rows = len(grid)
    cols = len(grid[0])

    start_r, start_c = find_start(grid)

    # beams maps: column -> number of timelines with a beam at (current_row, column)
    beams = {start_c: 1}
    exited = 0  # total timelines that have exited the manifold

    # Process from the row containing S down to the last row
    for r in range(start_r, rows):
        new_beams = {}

        for c, count in beams.items():
            cell = grid[r][c]

            if cell == "^":
                # Splitter: timeline splits into left and right
                if r == rows - 1:
                    # At bottom row: both branches immediately exit
                    exited += count * 2
                else:
                    nr = r + 1
                    if c - 1 >= 0:
                        new_beams[c - 1] = new_beams.get(c - 1, 0) + count
                    if c + 1 < cols:
                        new_beams[c + 1] = new_beams.get(c + 1, 0) + count
            else:
                # Empty / S / other: beam continues straight down
                if r == rows - 1:
                    # Exits below the last row
                    exited += count
                else:
                    nr = r + 1
                    new_beams[c] = new_beams.get(c, 0) + count

        beams = new_beams

    return exited


def main():
    grid = read_grid("input.txt")
    total_timelines = count_timelines(grid)
    print(total_timelines)


if __name__ == "__main__":
    main()
