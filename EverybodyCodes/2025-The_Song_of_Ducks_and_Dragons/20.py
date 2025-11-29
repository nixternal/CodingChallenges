#!/usr/bin/env python
"""
Triangle Grid Navigation Solver

This module solves three related pathfinding problems on triangle grids:
1. Count adjacent 'T' pairs in a triangle grid
2. Find shortest path from S to E on a standard triangle grid
3. Find shortest path from S to E on a rotating triangle grid

Triangle Grid Topology:
- Triangles alternate between pointing up (△) and pointing down (▽)
- Each triangle has 3 neighbors (sharing edges)
- Position is represented as (row, col) where col determines orientation
"""

from collections import deque


def read_puzzle_input() -> list:
    """Read puzzle input file containing three grid sections."""
    with open("20.in", "r") as file:
        return file.read().split("\n\n")


def get_triangle_neighbors(grid, row, col):
    """
    Get the three edge-adjacent neighbors of a triangle in the grid.

    Triangle grids have alternating orientations based on column parity.

    For even columns (upward-pointing triangles):
    - Left and right neighbors in same row
    - Third neighbor: up-right diagonal (row-1, col+1)

    For odd columns (downward-pointing triangles):
    - Left and right neighbors in same row
    - Third neighbor: down-left diagonal (row+1, col-1)

    Args:
        grid: The triangle grid
        row: Current row index
        col: Current column index

    Yields:
        Tuples of (row, col) for valid neighboring triangles
    """
    # Left neighbor
    if col > 0:
        yield (row, col - 1)

    # Right neighbor
    if col < len(grid[row]) - 1:
        yield (row, col + 1)

    # Diagonal neighbor depends on column parity
    if col % 2 == 0:
        # Even column: up-right diagonal
        if row > 0:
            yield (row - 1, col + 1)
    else:
        # Odd column: down-left diagonal
        yield (row + 1, col - 1)


def rotate_triangle_position(grid, row, col) -> tuple:
    """
    Rotate a triangle grid position 120 degrees.

    This transformation rotates the entire triangle grid coordinate system,
    mapping each triangle to its new position after rotation. The rotation
    preserves the triangle tessellation structure.

    Args:
        grid: The triangle grid (used for dimensions)
        row: Current row index
        col: Current column index

    Returns:
        Tuple of (new_row, new_col) after rotation
    """
    new_row = len(grid) - (col + 3) // 2 - row
    new_col = row * 2 + col % 2
    return (new_row, new_col)


def get_triangle_neighbors_with_rotation(grid, row, col):
    """
    Get neighbors after first rotating the current position.

    This applies a 120-degree rotation to the current position, then
    yields that rotated position plus all its standard triangle neighbors.
    This creates a more complex navigation topology.

    Args:
        grid: The triangle grid
        row: Current row index
        col: Current column index

    Yields:
        Tuples of (row, col) for the rotated position and its neighbors
    """
    rotated_row, rotated_col = rotate_triangle_position(grid, row, col)

    # Validate rotated position is within bounds
    if 0 <= rotated_row < len(grid) and 0 <= rotated_col < len(grid[rotated_row]):
        # First yield the rotated position itself
        yield (rotated_row, rotated_col)

        # Then yield all neighbors of the rotated position
        yield from get_triangle_neighbors(grid, rotated_row, rotated_col)


def part_one(data: list) -> int:
    """
    Count adjacent 'T' pairs in a triangle grid.

    Counts pairs where two 'T' characters are in triangles that share
    an edge. This includes:
    - Horizontal pairs within the same row (left-right neighbors)
    - Diagonal pairs between rows (third edge neighbor)

    Args:
        data: List of input sections (uses first section)

    Returns:
        Number of adjacent 'T' pairs found
    """
    grid = [line.strip().strip(".") for line in data[0].splitlines()]
    pair_count = 0

    # Check horizontal (left-right) pairs within each row
    for row in grid:
        for left_char, right_char in zip(row, row[1:]):
            if left_char == right_char == "T":
                pair_count += 1

    # Check diagonal pairs between adjacent rows
    # Odd columns in row N connect to even columns in row N+1
    # This represents upward triangles connecting to downward triangles below
    for current_row, next_row in zip(grid, grid[1:]):
        for upper_char, lower_char in zip(current_row[1::2], next_row[0::2]):
            if upper_char == lower_char == "T":
                pair_count += 1

    return pair_count


def part_two(data: list) -> int:
    """
    Find shortest path from S to E in a standard triangle grid.

    Uses BFS to find the minimum number of steps needed to reach
    the end position, moving only between edge-adjacent triangles
    and avoiding '#' walls.

    Args:
        data: List of input sections (uses second section)

    Returns:
        Length of shortest path from S to E, or -2 if no path exists
    """
    grid = [line.strip().strip(".") for line in data[1].splitlines()]

    # Find start and end positions
    start_pos = None
    end_pos = None
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == "S":
                start_pos = (row_idx, col_idx)
            if char == "E":
                end_pos = (row_idx, col_idx)

    # BFS to find shortest path
    visited = {start_pos}
    queue = deque([(0, start_pos)])

    while queue:
        distance, (current_row, current_col) = queue.popleft()

        for neighbor_row, neighbor_col in get_triangle_neighbors(
            grid, current_row, current_col
        ):
            # Check if we've reached the end
            if (neighbor_row, neighbor_col) == end_pos:
                return distance + 1

            # Skip if already visited
            if (neighbor_row, neighbor_col) in visited:
                continue

            # Skip walls
            if grid[neighbor_row][neighbor_col] == "#":
                continue

            # Add to queue for exploration
            visited.add((neighbor_row, neighbor_col))
            queue.append((distance + 1, (neighbor_row, neighbor_col)))

    return -2  # No path found


def part_three(data: list) -> int:
    """
    Find shortest path from S to E in a rotating triangle grid.

    Similar to part_two, but each move first rotates the grid position
    120 degrees before determining neighbors. This creates a more complex
    navigation space where the grid effectively "rotates" as you move.

    Args:
        data: List of input sections (uses third section)

    Returns:
        Length of shortest path from S to E, or -3 if no path exists
    """
    grid = [line.strip().strip(".") for line in data[2].splitlines()]

    # Find start and end positions
    start_pos = None
    end_pos = None
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == "S":
                start_pos = (row_idx, col_idx)
            if char == "E":
                end_pos = (row_idx, col_idx)

    # BFS to find shortest path with rotation
    visited = {start_pos}
    queue = deque([(0, start_pos)])

    while queue:
        distance, (current_row, current_col) = queue.popleft()

        for neighbor_row, neighbor_col in get_triangle_neighbors_with_rotation(
            grid, current_row, current_col
        ):
            # Check if we've reached the end
            if (neighbor_row, neighbor_col) == end_pos:
                return distance + 1

            # Skip if already visited
            if (neighbor_row, neighbor_col) in visited:
                continue

            # Skip walls
            if grid[neighbor_row][neighbor_col] == "#":
                continue

            # Add to queue for exploration
            visited.add((neighbor_row, neighbor_col))
            queue.append((distance + 1, (neighbor_row, neighbor_col)))

    return -3  # No path found


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data))  # 133
    print("Part 2:", part_two(data))  # 585
    print("Part 3:", part_three(data))  # 485
