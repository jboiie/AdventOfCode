class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def main():
    # Read points from input.txt
    with open("input.txt") as f:
        points = [tuple(map(int, line.strip().split(",")))
                  for line in f if line.strip()]

    n = len(points)

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    # Build all pairwise distances once
    dists = []
    append = dists.append

    for i in range(n):
        x1, y1, z1 = xs[i], ys[i], zs[i]
        for j in range(i + 1, n):
            dx = x1 - xs[j]
            dy = y1 - ys[j]
            dz = z1 - zs[j]
            append((dx*dx + dy*dy + dz*dz, i, j))

    # Sort by distance
    dists.sort()

    # ------------------------
    # Part 1
    # ------------------------
    dsu1 = DSU(n)
    pairs_considered = 0

    for _, i, j in dists:
        dsu1.union(i, j)      # we always "connect" this pair, even if it's a no-op
        pairs_considered += 1
        if pairs_considered == 1000:
            break

    # Component sizes after 1000 pairs considered
    comp_sizes = {}
    for i in range(n):
        root = dsu1.find(i)
        comp_sizes[root] = comp_sizes.get(root, 0) + 1

    sizes = sorted(comp_sizes.values(), reverse=True)
    if len(sizes) < 3:
        raise ValueError(f"Expected at least 3 circuits for part 1, got {len(sizes)}: {sizes}")

    part1 = sizes[0] * sizes[1] * sizes[2]

    # ------------------------
    # Part 2
    # ------------------------
    dsu2 = DSU(n)
    components = n
    last_i = last_j = None

    for _, i, j in dists:
        # Only real merges reduce the number of components
        if dsu2.union(i, j):
            components -= 1
            last_i, last_j = i, j
            if components == 1:
                break

    if last_i is None or last_j is None:
        raise ValueError("Graph never became fully connected in part 2.")

    # Multiply X coordinates of the last two boxes that were actually connected
    x1 = xs[last_i]
    x2 = xs[last_j]
    part2 = x1 * x2

    # Print answers (you can adjust formatting as you like)
    print(part1)
    print(part2)


if __name__ == "__main__":
    main()
