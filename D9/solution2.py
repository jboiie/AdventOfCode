from itertools import combinations


def read_input() -> str:
    """Read input.txt from the same folder."""
    with open(r"C:\Programming\Projects\advent-of-code\D9\input.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_tiles(data: str) -> list[tuple[int, int]]:
    """Parse input into a list of (x, y) integer coordinates."""
    tiles = []
    for line in data.splitlines():
        if not line:
            continue
        x_str, y_str = line.split(",")
        tiles.append((int(x_str), int(y_str)))
    return tiles


def calculate_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Rectangle area including both corners."""
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


def get_normalized_edges(
    tiles: list[tuple[int, int]]
) -> list[tuple[int, int, int, int]]:
    """
    Convert ordered tiles into axis-aligned edges.
    Each edge is stored as (min_x, min_y, max_x, max_y).
    """
    edges = []
    n = len(tiles)

    # edges between consecutive tiles
    for i in range(n - 1):
        x1, y1 = tiles[i]
        x2, y2 = tiles[i + 1]
        edges.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    # edge from last back to first
    x1, y1 = tiles[-1]
    x2, y2 = tiles[0]
    edges.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    return edges


def is_fully_contained(
    edges: list[tuple[int, int, int, int]],
    min_x: int,
    min_y: int,
    max_x: int,
    max_y: int,
) -> bool:
    """
    Check if the axis-aligned rectangle [min_x,max_x]×[min_y,max_y]
    is fully contained inside the polygon defined by the edges.

    If any polygon edge's bounding box overlaps the *interior* of the
    rectangle, then the rectangle crosses the boundary -> not valid.
    """
    for e_min_x, e_min_y, e_max_x, e_max_y in edges:
        # Standard AABB overlap on interiors (strict inequalities)
        if (
            min_x < e_max_x
            and max_x > e_min_x
            and min_y < e_max_y
            and max_y > e_min_y
        ):
            return False
    return True


def part2(data: str) -> int:
    """Largest rectangle using only red/green tiles (Part 2)."""
    tiles = parse_tiles(data)
    edges = get_normalized_edges(tiles)

    best_area = 0

    for p1, p2 in combinations(tiles, 2):
        area = calculate_area(p1, p2)
        # prune if we can't beat current best
        if area <= best_area:
            continue

        # rectangle bounds
        min_x, max_x = sorted((p1[0], p2[0]))
        min_y, max_y = sorted((p1[1], p2[1]))

        if is_fully_contained(edges, min_x, min_y, max_x, max_y):
            best_area = area

    return best_area


def main():
    data = read_input()
    ans2 = part2(data)
    print(ans2)


if __name__ == "__main__":
    main()
