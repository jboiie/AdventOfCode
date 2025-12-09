def main():
    points = []

    # Read points from input.txt (each line: x,y)
    with open(r"C:\Programming\Projects\advent-of-code\D9\input.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            x, y = int(x_str), int(y_str)
            points.append((x, y))

    max_area = 0
    n = len(points)

    # Check all pairs of red tiles as opposite corners
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # If x or y is the same, it's a 1-tile tall or 1-tile wide rectangle (still valid)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            if area > max_area:
                max_area = area

    print(max_area)


if __name__ == "__main__":
    main()
