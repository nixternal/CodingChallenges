#!/usr/bin/env python

from functools import lru_cache
from typing import List, Set, Tuple


def read_puzzle_input(filename: str = "07.in") -> List[str]:
    """Read the puzzle input file and return lines as a list."""
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_start_position(grid: List[str]) -> Tuple[int, int]:
    """
    Find the starting position marked with 'S' in the grid.

    Returns:
        Tuple of (row, col) coordinates

    Raises:
        ValueError if no 'S' is found in the grid
    """
    for row_idx, row in enumerate(grid):
        col_idx = row.find("S")
        if col_idx != -1:
            return (row_idx, col_idx)
    raise ValueError("No starting position 'S' found in grid")


def part_one(grid: List[str]) -> int:
    """
    Count the number of beam splits encountered.

    Simulates beams moving downward. When a beam hits a '^' splitter,
    it counts as one split and creates two new beams (left and right).

    Args:
        grid: The puzzle grid with '.' for empty space, '^' for splitters, and 'S' for start

    Returns:
        Total number of splits encountered across all beam paths
    """
    num_rows = len(grid)
    num_cols = len(grid[0])
    start_row, start_col = find_start_position(grid)

    # Track active beam positions (row, col)
    # Using a set automatically handles merging duplicate beams
    active_beams: Set[Tuple[int, int]] = {(start_row, start_col)}
    total_splits = 0

    while active_beams:
        next_beams: Set[Tuple[int, int]] = set()

        for row, col in active_beams:
            next_row = row + 1

            # Beam exits the bottom
            if next_row >= num_rows:
                continue

            cell = grid[next_row][col]

            if cell == "^":
                # Hit a splitter - increment counter and branch
                total_splits += 1

                # Add left beam if it stays in bounds
                if col - 1 >= 0:
                    next_beams.add((next_row, col - 1))

                # Add right beam if it stays in bounds
                if col + 1 < num_cols:
                    next_beams.add((next_row, col + 1))
            else:
                # Empty space - beam continues straight down
                next_beams.add((next_row, col))

        active_beams = next_beams

    return total_splits


def part_two(grid: List[str]) -> int:
    """
    Count the total number of distinct timeline branches (exit points).

    Uses memoization to efficiently calculate how many distinct paths emerge
    from each position. When a beam splits, the total timelines is the sum
    of timelines from each branch. When a beam exits, that counts as 1 timeline.

    Args:
        grid: The puzzle grid

    Returns:
        Total number of distinct timeline branches
    """
    num_rows = len(grid)
    num_cols = len(grid[0])
    start_row, start_col = find_start_position(grid)

    @lru_cache(maxsize=None)
    def count_timelines(row: int, col: int) -> int:
        """
        Recursively count how many distinct timelines branch from this position.

        Args:
            row: Current row position
            col: Current column position

        Returns:
            Number of distinct timeline branches from this position
        """
        next_row = row + 1

        # Beam exits the bottom - this is one complete timeline
        if next_row >= num_rows:
            return 1

        cell = grid[next_row][col]

        if cell == "^":
            # Hit a splitter - sum timelines from both branches
            timeline_count = 0

            # Left branch
            if col - 1 >= 0:
                timeline_count += count_timelines(next_row, col - 1)
            else:
                # Left branch exits immediately through the side
                timeline_count += 1

            # Right branch
            if col + 1 < num_cols:
                timeline_count += count_timelines(next_row, col + 1)
            else:
                # Right branch exits immediately through the side
                timeline_count += 1

            return timeline_count
        else:
            # Empty space - continue straight down
            return count_timelines(next_row, col)

    return count_timelines(start_row, start_col)


if __name__ == "__main__":
    puzzle_data = read_puzzle_input()

    print("Part 1:", part_one(puzzle_data))  # 1703
    print("Part 2:", part_two(puzzle_data))  # 171692855075500
