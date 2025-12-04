#!/usr/bin/env python
"""
Puzzle solver for counting and removing accessible '@' symbols.

Part 1: Count '@' symbols with fewer than 4 adjacent '@' neighbors
Part 2: Iteratively remove accessible '@' symbols until none remain
"""


def read_puzzle_input() -> list[str]:
    """Read puzzle input from file and return as list of strings."""
    with open("04.in", "r") as file:
        return file.read().splitlines()


# Pre-define direction offsets for 8-directional adjacency
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_adjacent_rolls(
    grid: list[list[str]], r: int, c: int, rows: int, cols: int
) -> int:
    """
    Count adjacent '@' symbols at position (r, c).

    Args:
        grid: 2D grid of characters
        r, c: Row and column position
        rows, cols: Grid dimensions

    Returns:
        Number of adjacent '@' symbols (0-8)
    """
    count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            count += 1
    return count


def part_one(data: list[str]) -> int:
    """
    Grid Traversal w/ Adjacency Counting: count accessible '@' symbols
    (those with < 4 adjacent '@' neighbors).

    Args:
        data: List of strings representing the grid

    Returns:
        Count of accessible rolls
    """
    grid = [list(line) for line in data]
    rows, cols = len(grid), len(grid[0])

    accessible = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                if count_adjacent_rolls(grid, r, c, rows, cols) < 4:
                    accessible += 1

    return accessible


def part_two(data: list[str]) -> int:
    """
    Iterative Erosion (aka Layer Peeling or Onion Peeling): iteratively remove
    accessible '@' symbols until no more can be removed. An '@' is accessible if
    it has fewer than 4 adjacent '@' neighbors.

    Args:
        data: List of strings representing the grid

    Returns:
        Total number of '@' symbols removed
    """
    grid = [list(line) for line in data]
    rows, cols = len(grid), len(grid[0])

    total_removed = 0

    while True:
        # Find all accessible rolls in current state
        to_remove = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == "@" and count_adjacent_rolls(grid, r, c, rows, cols) < 4
        ]

        if not to_remove:
            break  # No more accessible rolls

        # Remove all accessible rolls simultaneously
        for r, c in to_remove:
            grid[r][c] = "."

        total_removed += len(to_remove)

    return total_removed


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # Expected: 1549
    print("Part 2:", part_two(data))  # Expected: 8887
