#!/usr/bin/env python
"""
Grid-based BFS puzzle solver with fireball mechanics.

The puzzle involves grids where each cell contains a digit (0-9).
Fireballs can spread from cell to adjacent cell if the target cell's
value is <= the current cell's value.
"""

from collections import deque

# Four cardinal directions: right, left, down, up
MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def read_puzzle_input() -> list:
    """Read puzzle input file and split into sections"""
    with open("12.in", "r") as file:
        return file.read().split("\n\n")


def parse_grid(lines):
    """Convert string grid to integer grid once"""
    return [[int(ch) for ch in row] for row in lines]


def bfs_cells(grid, starts, blocked=None):
    """
    Perform BFS from one or more starting positions.

    A cell can be reached if:
    - It's adjacent to a reachable cell
    - Its value <= the value of the cell we're coming from
    - It's not in the blocked set

    Args:
        grid: 2D list of integers
        starts: List of (row, col) tuples for starting positions
        blocked: Set of (row, col) tuples that cannot be visited

    Returns:
        Set of all reachable (row, col) positions
    """
    if blocked is None:
        blocked = set()

    height = len(grid)
    width = len(grid[0])
    visited = set()
    queue = deque()

    # Initialize with all starting positions that aren't blocked
    if not isinstance(starts, list):
        starts = [starts]

    for start_pos in starts:
        if start_pos not in blocked:
            visited.add(start_pos)
            queue.append(start_pos)

    # BFS traversal
    while queue:
        row, col = queue.popleft()
        current_value = grid[row][col]

        # Try all four directions
        for delta_row, delta_col in MOVES:
            new_row = row + delta_row
            new_col = col + delta_col

            # Check if new position is valid and unvisited
            if 0 <= new_row < height and 0 <= new_col < width:
                new_pos = (new_row, new_col)
                if new_pos not in visited and new_pos not in blocked:
                    # Can only spread to cells with value <= current value
                    if grid[new_row][new_col] <= current_value:
                        visited.add(new_pos)
                        queue.append(new_pos)

    return visited


def find_best_single_position(grid, blocked_cells):
    """
    Find the single best cell to place a fireball.

    Tests every non-blocked cell and returns the one that would
    destroy the most cells.

    Args:
        grid: 2D integer grid
        blocked_cells: Set of positions that cannot be used or reached

    Returns:
        Tuple of (best_position, cells_destroyed_count)
    """
    height = len(grid)
    width = len(grid[0])
    best_position = None
    best_count = -1

    for row in range(height):
        for col in range(width):
            position = (row, col)
            if position in blocked_cells:
                continue

            # See how many cells this position would destroy
            destroyed_cells = bfs_cells(grid, [position], blocked_cells)
            cells_destroyed = len(destroyed_cells)

            if cells_destroyed > best_count:
                best_count = cells_destroyed
                best_position = position

    return best_position, best_count


def greedy_three_fireballs(grid):
    """
    Use a greedy algorithm to place 3 fireballs optimally.

    Strategy:
    1. Place first fireball at position that destroys most cells
    2. Block those destroyed cells from consideration
    3. Place second fireball at best remaining position
    4. Block those newly destroyed cells
    5. Place third fireball at best remaining position
    6. Calculate total destruction from all 3 fireballs together

    Note: This greedy approach doesn't guarantee optimal solution,
    but is much faster than checking all combinations.

    Args:
        grid: 2D integer grid

    Returns:
        Total number of cells destroyed by all 3 fireballs
    """
    blocked_cells = set()
    fireball_positions = []

    # Place first fireball
    first_pos, _ = find_best_single_position(grid, blocked_cells)
    fireball_positions.append(first_pos)
    destroyed_by_first = bfs_cells(grid, [first_pos], blocked_cells)
    blocked_cells.update(destroyed_by_first)

    # Place second fireball
    second_pos, _ = find_best_single_position(grid, blocked_cells)
    fireball_positions.append(second_pos)
    destroyed_by_second = bfs_cells(grid, [second_pos], blocked_cells)
    blocked_cells.update(destroyed_by_second)

    # Place third fireball
    third_pos, _ = find_best_single_position(grid, blocked_cells)
    fireball_positions.append(third_pos)

    # Calculate final destruction: all 3 fireballs working together
    # (they can overlap and destroy more cells together than separately)
    final_destroyed = bfs_cells(grid, fireball_positions)
    return len(final_destroyed)


def part_one(data: list) -> int:
    """
    Part 1: Single fireball starting from top-left corner (0,0).
    Count how many cells it destroys.
    """
    lines = data[0].splitlines()
    if not lines:
        return 0

    # Validate grid is rectangular
    width = len(lines[0])
    if any(len(row) != width for row in lines):
        return -1

    grid = parse_grid(lines)
    destroyed = bfs_cells(grid, [(0, 0)])
    return len(destroyed)


def part_two(data: list) -> int:
    """
    Part 2: Two fireballs starting from opposite corners.
    One from top-left (0,0) and one from bottom-right.
    Count total cells destroyed by both working together.
    """
    lines = data[1].splitlines()
    if not lines:
        return 0

    # Validate grid is rectangular
    width = len(lines[0])
    if any(len(row) != width for row in lines):
        return -2

    grid = parse_grid(lines)
    height = len(grid)
    width = len(grid[0])

    # Start from both corners simultaneously
    start_positions = [(0, 0), (height - 1, width - 1)]
    destroyed = bfs_cells(grid, start_positions)
    return len(destroyed)


def part_three(data: list) -> int:
    """
    Part 3: Place 3 fireballs optimally using greedy algorithm.
    Returns total cells destroyed.
    """
    lines = data[2].splitlines()
    if not lines:
        return 0

    grid = parse_grid(lines)
    return greedy_three_fireballs(grid)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 233
    print("Part 2:", part_two(data))  # 5767
    print("Part 3:", part_three(data))  # 4005
