#!/usr/bin/env python
"""
Cellular Automaton Simulator
Simulates a grid where cells toggle based on neighboring '#' cells.
"""

from copy import deepcopy
from typing import List

# Neighbor offsets: diagonals + center
NEIGHBOR_OFFSETS = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 0)]


def read_puzzle_input() -> List[str]:
    """Read and split input file into sections."""
    with open("14.in", "r") as file:
        return file.read().split("\n\n")


def parse_grid(grid_text: str) -> List[List[str]]:
    """Convert text grid into 2D list."""
    return [list(row) for row in grid_text.splitlines()]


def calculate_next_state(grid: List[List[str]], row: int, col: int) -> str:
    """
    Calculate next state for a cell by toggling for each active neighbor.
    Starts with True, toggles for each '#' found in neighbor positions.
    """
    rows, cols = len(grid), len(grid[0])
    is_active = True

    for row_offset, col_offset in NEIGHBOR_OFFSETS:
        neighbor_row = row + row_offset
        neighbor_col = col + col_offset

        if (
            0 <= neighbor_row < rows
            and 0 <= neighbor_col < cols
            and grid[neighbor_row][neighbor_col] == "#"
        ):
            is_active = not is_active

    return "#" if is_active else "."


def step_simulation(grid: List[List[str]]) -> tuple[List[List[str]], int]:
    """
    Execute one simulation step and return new grid plus count of active cells.
    """
    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)
    active_count = 0

    for row in range(rows):
        for col in range(cols):
            new_grid[row][col] = calculate_next_state(grid, row, col)
            if new_grid[row][col] == "#":
                active_count += 1

    return new_grid, active_count


def run_simulation(grid: List[List[str]], steps: int) -> int:
    """Run simulation for specified steps and return cumulative active cell count."""
    total_active = 0

    for _ in range(steps):
        grid, active_count = step_simulation(grid)
        total_active += active_count

    return total_active


def count_active_cells(grid: List[List[str]]) -> int:
    """Count total number of active '#' cells in grid."""
    return sum(1 for row in grid for cell in row if cell == "#")


def grids_match(
    grid: List[List[str]], pattern: List[List[str]], center_row: int, center_col: int
) -> bool:
    """Check if pattern matches grid at specified center position."""
    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0])

    # Calculate top-left corner of pattern in grid
    start_row = center_row - pattern_rows // 2
    start_col = center_col - pattern_cols // 2

    for row in range(pattern_rows):
        for col in range(pattern_cols):
            grid_row = start_row + row
            grid_col = start_col + col

            if grid[grid_row][grid_col] != pattern[row][col]:
                return False

    return True


def part_one(data: List[str]) -> int:
    """Simulate grid for 10 steps, return cumulative active cells."""
    grid = parse_grid(data[0])
    return run_simulation(grid, steps=10)


def part_two(data: List[str]) -> int:
    """Simulate grid for 2025 steps, return cumulative active cells."""
    grid = parse_grid(data[1])
    return run_simulation(grid, steps=2025)


def part_three(data: List[str]) -> int:
    """
    Simulate large grid for 1 billion steps with pattern matching optimization.
    Counts active cells only when center pattern matches target.
    Uses cycle detection to skip redundant calculations.
    """
    target_pattern = parse_grid(data[2])
    pattern_rows = len(target_pattern)
    pattern_cols = len(target_pattern[0])

    # Initialize larger grid
    grid_size = 34
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    center_position = 17

    max_steps = 1_000_000_000
    current_step = 0
    total_score = 0
    last_match_step = 0

    # Track intervals between matches to detect cycles
    interval_cache = {}

    while current_step < max_steps:
        current_step += 1

        # Step simulation
        rows, cols = len(grid), len(grid[0])
        new_grid = deepcopy(grid)
        for row in range(rows):
            for col in range(cols):
                new_grid[row][col] = calculate_next_state(grid, row, col)
        grid = new_grid

        # Check if center pattern matches
        if grids_match(grid, target_pattern, center_position, center_position):
            step_score = count_active_cells(grid)
            total_score += step_score

            # Calculate interval since last match
            interval = current_step - last_match_step

            # Cycle detection: if we've seen this interval before
            if interval in interval_cache:
                cached_step, cached_score = interval_cache[interval]
                cycle_length = current_step - cached_step
                cycle_score = total_score - cached_score

                # Skip ahead using detected cycle
                remaining_steps = max_steps - current_step
                full_cycles = remaining_steps // cycle_length

                current_step += full_cycles * cycle_length
                total_score += full_cycles * cycle_score
            else:
                interval_cache[interval] = (current_step, total_score)

            last_match_step = current_step

    return total_score


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 503
    print("Part 2:", part_two(data))  # 1169260
    print("Part 3:", part_three(data))  # 1100855300
