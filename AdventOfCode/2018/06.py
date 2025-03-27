#!/usr/bin/env python3

from collections import Counter, deque
from typing import List, Tuple


def read_puzzle_input() -> List[Tuple[int, ...]]:
    """
    Read coordinate points from an input file.

    Returns:
        List of (x, y) coordinate tuples representing points of interest.

    Note:
    - Assumes input file '06.in' contains comma-separated x,y coordinates
    - Each line represents a unique point
    """

    with open("06.in", "r") as file:
        return [
            tuple(map(int, line.strip().split(',')))
            for line in file
        ]


def calculate_manhattan_distance(p1: Tuple[int, int],
                                 p2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan (city block) distance between two points.

    Args:
        p1: First point as (x, y) tuple
        p2: Second point as (x, y) tuple

    Returns:
        Manhattan distance between the points
    """

    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_largest_finite_area(points: List[Tuple[int, int]]) -> int:
    """
    Find the largest area that is not infinite in a coordinate grid.

    Algorithm:
    1. Determine grid boundaries
    2. Identify the closest point for each grid cell
    3. Exclude points with areas touching grid boundaries
    4. Calculate area sizes for remaining points

    Args:
        points: List of coordinate points

    Returns:
        Size of the largest finite area
    """

    # Compute grid boundaries
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    # Track point areas and infinite regions
    area_sizes = Counter()
    infinite_points = set()

    # Iterate through every cell in the grid
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Find closest point to current cell
            distances = [
                calculate_manhattan_distance((x, y), point) for point in points
            ]
            min_distance = min(distances)

            # Check for unique closest point
            closest_points = [
                points[i] for i, dist in enumerate(distances)
                if dist == min_distance
            ]

            # If multiple points are equidistant, skip
            if len(closest_points) > 1:
                continue

            closest_point = closest_points[0]

            # Mark infinite areas (points touching grid boundaries)
            if x in (min_x, max_x) or y in (min_y, max_y):
                infinite_points.add(closest_point)

            # Count area for non-infinite points
            if closest_point not in infinite_points:
                area_sizes[closest_point] += 1

    return max(area_sizes.values(), default=0)


def find_safe_region_size(points: List[Tuple[int, int]],
                          max_total_distance: int = 10_000) -> int:
    """
    Find the size of a region where the total distance to all points is less
    than a threshold.

    Uses a breadth-first search (BFS) approach to explore the safe region
    efficiently.

    Args:
        points: List of coordinate points
        max_total_distance: Maximum allowed total distance to all points

    Returns:
        Number of points within the safe region
    """

    # Estimate search center based on point mean coordinates
    start_x = sum(x for x, _ in points) // len(points)
    start_y = sum(y for _, y in points) // len(points)

    # BFS to explore safe region
    queue = deque([(start_x, start_y)])
    visited = {(start_x, start_y)}
    safe_region_size = 0

    while queue:
        x, y = queue.popleft()

        # Calculate total distance to all points
        total_distance = sum(
            calculate_manhattan_distance((x, y), point) for point in points
        )

        # Count point if within safe region
        if total_distance < max_total_distance:
            safe_region_size += 1

            # Explore adjacent unvisited points
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_point = (x + dx, y + dy)
                if next_point not in visited:
                    visited.add(next_point)
                    queue.append(next_point)

    return safe_region_size


def part_one(data: list) -> int:
    return find_largest_finite_area(data)


def part_two(data: list) -> int:
    return find_safe_region_size(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 4290
    print("Part 2:", part_two(data))  # 37318
