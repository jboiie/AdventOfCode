from collections import deque

def main():
    # Read red tile coordinates in listed order
    reds = []
    with open(r"C:\Programming\Projects\advent-of-code\D9\input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            reds.append((int(x_str), int(y_str)))

    n = len(reds)

    # 1) Build the boundary (red + green tiles along straight segments)
    boundary = set()
    for i in range(n):
        x1, y1 = reds[i]
        x2, y2 = reds[(i + 1) % n]  # wrap around to form a loop

        if x1 == x2:
            step = 1 if y2 >= y1 else -1
            for y in range(y1, y2 + step, step):
                boundary.add((x1, y))
        elif y1 == y2:
            step = 1 if x2 >= x1 else -1
            for x in range(x1, x2 + step, step):
                boundary.add((x, y1))
        else:
            raise ValueError("Adjacent red tiles must share x or y (axis-aligned).")

    # 2) Build a grid covering the whole polygon bounding box
    xs = [x for x, _ in boundary]
    ys = [y for _, y in boundary]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # boundary_grid[y][x] = True if tile is boundary (red or boundary green)
    boundary_grid = [[False] * width for _ in range(height)]
    for (x, y) in boundary:
        boundary_grid[y - min_y][x - min_x] = True

    # 3) Flood-fill from outside to find which tiles are "outside" the loop
    outside = [[False] * width for _ in range(height)]
    q = deque()

    # Enqueue all border cells of the bounding box that are not boundary
    for xi in range(width):
        for yi in (0, height - 1):
            if not boundary_grid[yi][xi] and not outside[yi][xi]:
                outside[yi][xi] = True
                q.append((xi, yi))

    for yi in range(height):
        for xi in (0, width - 1):
            if not boundary_grid[yi][xi] and not outside[yi][xi]:
                outside[yi][xi] = True
                q.append((xi, yi))

    # BFS to mark all reachable "outside" tiles
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if not boundary_grid[ny][nx] and not outside[ny][nx]:
                    outside[ny][nx] = True
                    q.append((nx, ny))

    # 4) Tiles that are not outside are inside the loop; boundary tiles are also allowed.
    allowed = [[False] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if boundary_grid[y][x] or not outside[y][x]:
                allowed[y][x] = True

    # 5) Build 2D prefix sums over allowed tiles for fast rectangle checks
    prefix = [[0] * (width + 1) for _ in range(height + 1)]
    for y in range(height):
        row_sum = 0
        for x in range(width):
            if allowed[y][x]:
                row_sum += 1
            prefix[y + 1][x + 1] = prefix[y][x + 1] + row_sum

    def rect_sum(x1, x2, y1, y2):
        """
        Inclusive rectangle sum of allowed tiles in original coordinates:
        x in [x1, x2], y in [y1, y2]
        """
        xi1 = x1 - min_x
        xi2 = x2 - min_x
        yi1 = y1 - min_y
        yi2 = y2 - min_y
        return (
            prefix[yi2 + 1][xi2 + 1]
            - prefix[yi1][xi2 + 1]
            - prefix[yi2 + 1][xi1]
            + prefix[yi1][xi1]
        )

    # 6) Try all pairs of red tiles as opposite corners of the rectangle
    max_area = 0
    for i in range(n):
        x1, y1 = reds[i]
        for j in range(i + 1, n):
            x2, y2 = reds[j]

            x_lo, x_hi = min(x1, x2), max(x1, x2)
            y_lo, y_hi = min(y1, y2), max(y1, y2)

            width_rect = x_hi - x_lo + 1
            height_rect = y_hi - y_lo + 1
            area = width_rect * height_rect

            # Count how many tiles in this rectangle are allowed
            allowed_count = rect_sum(x_lo, x_hi, y_lo, y_hi)

            # Valid rectangle only if *every* tile is red/green (i.e., allowed)
            if allowed_count == area and area > max_area:
                max_area = area

    print(max_area)


if __name__ == "__main__":
    main()
