#!/usr/bin/env python


def read_puzzle_input() -> list[tuple[int, ...]]:
    """Read and parse input into list of coordinate tuples."""
    with open("25.in") as f:
        return [tuple(map(int, line.split(","))) for line in f if line.strip()]


def manhattan(a: tuple, b: tuple) -> int:
    """Calculate Manhattan distance between two points."""
    return sum(abs(x - y) for x, y in zip(a, b))


def find(parent: list[int], x: int) -> int:
    """Find root with path compression."""
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]


def union(parent: list[int], rank: list[int], x: int, y: int) -> None:
    """Union by rank."""
    root_x, root_y = find(parent, x), find(parent, y)
    if root_x == root_y:
        return

    if rank[root_x] < rank[root_y]:
        root_x, root_y = root_y, root_x

    parent[root_y] = root_x
    if rank[root_x] == rank[root_y]:
        rank[root_x] += 1


def part_one(points: list[tuple[int, ...]]) -> int:
    """Count constellations (connected components with distance <= 3)."""
    n = len(points)
    parent = list(range(n))
    rank = [0] * n

    # Union points that are within distance 3
    for i, p1 in enumerate(points):
        for j in range(i + 1, n):
            if manhattan(p1, points[j]) <= 3:
                union(parent, rank, i, j)

    # Count unique roots
    return sum(i == find(parent, i) for i in range(n))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 381
