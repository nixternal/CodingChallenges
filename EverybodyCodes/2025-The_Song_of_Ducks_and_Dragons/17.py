#!/usr/bin/env python
"""
Volcano puzzle solver with three parts:
1. Sum digits within a circular radius of volcano
2. Find optimal radius ring with highest score
3. Find smallest radius where a path around volcano is possible within time limit
"""

import heapq
from typing import Dict, List, Tuple, Union, cast


def read_puzzle_input() -> List[str]:
    """Read and split puzzle input into sections."""
    with open("17.in", "r") as file:
        return file.read().split("\n\n")


def parse_grid(grid_text: str) -> List[List[str]]:
    """Convert grid text into a 2D list."""
    return [list(row) for row in grid_text.strip().splitlines()]


def find_character(grid: List[List[str]], target: str) -> Tuple[int, int]:
    """Find the position of a character in the grid."""
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == target:
                return row_idx, col_idx
    raise ValueError(f"Character '{target}' not found in grid")


def is_within_radius(
    point: Tuple[int, int], center: Tuple[int, int], radius: int
) -> bool:
    """Check if a point is within a circular radius of the center."""
    dy = point[0] - center[0]
    dx = point[1] - center[1]
    return dy * dy + dx * dx <= radius * radius


def dijkstra_with_volcano_constraint(
    grid: List[List[Union[int, str]]],
    start: Tuple[int, int],
    volcano_pos: Tuple[int, int],
    radius: int,
    allow_left_of_volcano: bool,
) -> Dict[Tuple[int, int], int]:
    """
    Run Dijkstra's algorithm avoiding the volcano radius and one side.

    Args:
        grid: 2D grid with integer weights (may contain str during conversion)
        start: Starting position (row, col)
        volcano_pos: Volcano position (row, col)
        radius: Radius to avoid around volcano
        allow_left_of_volcano: If True, avoid right side; if False, avoid left side

    Returns:
        Dictionary mapping positions to minimum distances
    """
    rows = len(grid)
    cols = len(grid[0])
    volcano_row, volcano_col = volcano_pos
    distances = {}
    heap = [(0, start[0], start[1])]

    while heap:
        dist, row, col = heapq.heappop(heap)

        # Skip if out of bounds
        if not (0 <= row < rows and 0 <= col < cols):
            continue

        # Skip if inside volcano radius
        if is_within_radius((row, col), volcano_pos, radius):
            continue

        # Skip positions on the forbidden side of the volcano
        if row == volcano_row:
            if allow_left_of_volcano and col > volcano_col:
                continue
            if not allow_left_of_volcano and col < volcano_col:
                continue

        # Skip if already visited
        if (row, col) in distances:
            continue

        distances[(row, col)] = dist

        # Explore neighbors
        for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + delta_row
            next_col = col + delta_col
            cell_value = grid[row][col]
            next_dist = dist + (
                int(cell_value) if isinstance(cell_value, str) else cell_value
            )
            heapq.heappush(heap, (next_dist, next_row, next_col))

    return distances


def part_one(data: List[str]) -> int:
    """
    Sum all digits within a fixed radius (10) of the volcano.

    Args:
        data: Puzzle input sections

    Returns:
        Sum of all digits within radius
    """
    grid = parse_grid(data[0])
    volcano_pos = find_character(grid, "@")
    radius = 10

    total = 0
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if is_within_radius((row_idx, col_idx), volcano_pos, radius):
                if cell.isdigit():
                    total += int(cell)

    return total


def part_two(data: List[str]) -> int:
    """
    Find the radius ring (annulus) with the highest score,
    then return score * radius.

    Args:
        data: Puzzle input sections

    Returns:
        Best score multiplied by its radius
    """
    grid = parse_grid(data[1])
    volcano_row, volcano_col = find_character(grid, "@")

    best_score = 0
    best_result = 0

    # Test different radii to find the ring with maximum score
    for radius in range(1, 1000):
        ring_score = 0
        inner_radius_sq = (radius - 1) ** 2
        outer_radius_sq = radius**2

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                # Skip the volcano itself
                if (row_idx, col_idx) == (volcano_row, volcano_col):
                    continue

                # Check if point is in the ring (between inner and outer radius)
                dist_sq = (row_idx - volcano_row) ** 2 + (col_idx - volcano_col) ** 2
                if inner_radius_sq < dist_sq <= outer_radius_sq:
                    ring_score += int(cell)

        if best_score is None or ring_score > best_score:
            best_score = ring_score
            best_result = ring_score * radius

    return best_result


def part_three(data: List[str]) -> int:
    """
    Find the smallest radius where a path looping around the volcano
    can be completed within the time limit.

    Args:
        data: Puzzle input sections

    Returns:
        Radius multiplied by minimum path cost
    """
    grid = parse_grid(data[2])
    volcano_pos = find_character(grid, "@")
    start_pos = find_character(grid, "S")

    # Convert grid cells to integers (except special markers)
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell not in ["@", "S"]:
                grid[row_idx][col_idx] = int(cell)  # type: ignore[assignment]

    grid[start_pos[0]][start_pos[1]] = 0  # type: ignore[assignment]

    # Cast to the correct type for the dijkstra function
    mixed_grid = cast(List[List[Union[int, str]]], grid)

    # Try increasing radii until we find a valid path
    for radius in range(1000):
        time_limit = (radius + 1) * 30 - 1

        # Calculate shortest paths going left and right around volcano
        distances_left = dijkstra_with_volcano_constraint(
            mixed_grid, start_pos, volcano_pos, radius, allow_left_of_volcano=True
        )
        distances_right = dijkstra_with_volcano_constraint(
            mixed_grid, start_pos, volcano_pos, radius, allow_left_of_volcano=False
        )

        # Find minimum cost to complete the loop below the volcano
        min_loop_cost = float("inf")
        volcano_row, volcano_col = volcano_pos

        for row in range(volcano_row + 1, len(grid)):
            meeting_point = (row, volcano_col)
            if meeting_point in distances_left and meeting_point in distances_right:
                loop_cost = (
                    distances_left[meeting_point]
                    + distances_right[meeting_point]
                    + int(mixed_grid[row][volcano_col])  # type: ignore[arg-type]
                )
                min_loop_cost = min(min_loop_cost, loop_cost)

        if min_loop_cost < time_limit:
            return int(radius * min_loop_cost)

    return -1  # No solution found


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1606
    print("Part 2:", part_two(data))  # 67314
    print("Part 3:", part_three(data))  # 43890
