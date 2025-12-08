#!/usr/bin/env python

from collections import defaultdict


def read_puzzle_input() -> list[tuple[int, int, int]]:
    """Read 3D points from input file."""
    points = []
    with open("08.in", "r") as file:
        for line in file.read().splitlines():
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    return points


def compute_distances(points: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Compute squared Euclidean distances between all point pairs.
    Returns list of (distance, point_i, point_j) tuples, sorted by distance.
    """
    distances = []
    for i, (x1, y1, z1) in enumerate(points):
        for j, (x2, y2, z2) in enumerate(points):
            if i > j:  # Only compute each pair once
                squared_distance = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
                distances.append((squared_distance, i, j))

    return sorted(distances)


def find_root(parent: dict[int, int], node: int) -> int:
    """Find root of node with path compression."""
    if node == parent[node]:
        return node
    parent[node] = find_root(parent, parent[node])
    return parent[node]


def union_sets(parent: dict[int, int], node_a: int, node_b: int) -> bool:
    """
    Unite sets containing node_a and node_b.
    Returns True if they were in different sets, False otherwise.
    """
    root_a = find_root(parent, node_a)
    root_b = find_root(parent, node_b)

    if root_a == root_b:
        return False

    parent[root_a] = root_b
    return True


def get_component_sizes(parent: dict[int, int]) -> list[int]:
    """Get sizes of all connected components, sorted."""
    sizes = defaultdict(int)
    for node in parent:
        sizes[find_root(parent, node)] += 1
    return sorted(sizes.values())


def part_one(points: list[tuple[int, int, int]]) -> int:
    """
    Connect the 1000 closest point pairs and return product of
    three largest component sizes.
    """
    distances = compute_distances(points)
    parent = {i: i for i in range(len(points))}

    # Connect the 1000 closest pairs
    for _, point_i, point_j in distances[:1000]:
        union_sets(parent, point_i, point_j)

    # Get three largest component sizes and return their product
    component_sizes = get_component_sizes(parent)
    return component_sizes[-1] * component_sizes[-2] * component_sizes[-3]


def part_two(points: list[tuple[int, int, int]]) -> int:
    """
    Build minimum spanning tree by connecting closest pairs.
    Return product of coordinates when tree becomes connected.
    """
    distances = compute_distances(points)
    parent = {i: i for i in range(len(points))}

    connections_made = 0
    num_points = len(points)

    # A tree with n nodes has n-1 edges
    for _, point_i, point_j in distances:
        if union_sets(parent, point_i, point_j):
            connections_made += 1
            if connections_made == num_points - 1:
                # Tree is complete - all points connected
                return points[point_i][0] * points[point_j][0]

    # Should not reach here if input forms a valid tree
    return -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 244188
    print("Part 2:", part_two(data))  # 8361881885
