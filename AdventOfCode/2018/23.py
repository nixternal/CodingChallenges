#!/usr/bin/env python

import re
from heapq import heappop, heappush


def read_puzzle_input() -> list:
    with open("23.in", "r") as file:
        return file.read().splitlines()


def parse_nanobots(data: list) -> list:
    """Parse nanobot data from input lines."""
    nanobots = []
    for line in data:
        x, y, z, radius = map(int, re.findall(r"-?\d+", line))
        nanobots.append((x, y, z, radius))
    return nanobots


def manhattan_distance(x1, y1, z1, x2, y2, z2) -> int:
    """Calculate Manhattan distance between two 3D points."""
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def part_one(data: list) -> int:
    """Find how many nanobots are in range of the strongest nanobot."""
    nanobots = parse_nanobots(data)

    # Find the nanobot with the largest signal radius
    strongest = max(nanobots, key=lambda bot: bot[3])
    sx, sy, sz, sr = strongest

    # Count nanobots within range of the strongest
    in_range = sum(
        1
        for bot in nanobots
        if manhattan_distance(bot[0], bot[1], bot[2], sx, sy, sz) <= sr
    )

    return in_range


def part_two(data: list) -> int:
    """Find the shortest Manhattan distance to a point in range of the most nanobots."""
    nanobots = parse_nanobots(data)

    def count_in_range(x, y, z):
        """Count how many nanobots can reach the given point."""
        return sum(
            1
            for bx, by, bz, br in nanobots
            if manhattan_distance(x, y, z, bx, by, bz) <= br
        )

    # Find the bounding box of all coordinates
    all_coords = [coord for bot in nanobots for coord in bot[:3]]
    coord_range = max(all_coords) - min(all_coords)

    # Start with a box size that covers the entire search space
    size = 1
    while size < coord_range:
        size *= 2

    # Priority queue: (-count, distance_to_origin, box_size, x, y, z)
    queue = [(-len(nanobots), 0, size, 0, 0, 0)]
    visited = set()

    while queue:
        neg_count, dist, size, x, y, z = heappop(queue)

        if (size, x, y, z) in visited:
            continue
        visited.add((size, x, y, z))

        if size == 0:
            return dist

        # Subdivide the current box into smaller regions
        new_size = size // 2
        for dx in [0, new_size, -new_size]:
            for dy in [0, new_size, -new_size]:
                for dz in [0, new_size, -new_size]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    count = count_in_range(nx, ny, nz)
                    ndist = abs(nx) + abs(ny) + abs(nz)
                    heappush(queue, (-count, ndist, new_size, nx, ny, nz))

    return -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 609
    print("Part 2:", part_two(data))  # 130370534
