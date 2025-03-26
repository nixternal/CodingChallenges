#!/usr/bin/env python

import heapq
from typing import List, Optional, Tuple


def read_puzzle_input(filename: str = "10.in") -> List[List[int]]:
    """
    Read and parse the input grid from a file.

    Args:
        filename (str): Path to the input file containing the grid.

    Returns:
        List[List[int]]: 2D grid of integer danger levels.
    """

    with open(filename, "r") as file:
        return [[int(x) for x in line.split()] for line in file]


def find_minimum_danger_path(grid: List[List[int]],
                             start: Tuple[int, int] = (0, 0),
                             end: Optional[Tuple[int, int]] = None) -> int:
    """
    Find the minimum danger path using Dijkstra's algorithm with a priority
    queue.

    This function solves path-finding problems by calculating the minimum
    accumulated danger when moving through the grid, considering only
    right and down movements.

    Args:
        grid (List[List[int]]): 2D grid of danger levels
        start (Tuple[int, int]): Starting coordinates (default: top-left)
        end (Tuple[int, int]): Target coordinates (default: bottom-right)

    Returns:
        int: Minimum danger level to reach the target
    """

    rows, cols = len(grid), len(grid[0])

    # Default to bottom-right if no end specified
    end = end or (rows - 1, cols - 1)

    # Priority queue tracks (danger, row, col)
    pq = [(grid[start[0]][start[1]], start[0], start[1])]

    # Track minimum danger to reach each cell
    min_danger = [[float('inf')] * cols for _ in range(rows)]
    min_danger[start[0]][start[1]] = grid[start[0]][start[1]]

    # Movement directions: right and down
    directions = [(0, 1), (1, 0)]

    while pq:
        current_danger, r, c = heapq.heappop(pq)

        # Stop if target reached
        if (r, c) == end:
            return current_danger

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Boundary check
            if 0 <= nr < rows and 0 <= nc < cols:
                new_danger = current_danger + grid[nr][nc]

                # Update if better path found
                if new_danger < min_danger[nr][nc]:
                    min_danger[nr][nc] = new_danger
                    heapq.heappush(pq, (new_danger, nr, nc))

    raise ValueError("No path found")


def part_one(grid: List[List[int]]) -> int:
    """
    Calculate the minimum level across rows and columns.

    Args:
        grid (List[List[int]]): 2D grid of danger levels

    Returns:
        int: Minimum level across rows and columns
    """

    return min(
        min(sum(col) for col in zip(*grid)),
        min(sum(row) for row in grid)
    )


def part_two(grid: List[List[int]]) -> int:
    return find_minimum_danger_path(grid, end=(14, 14))  # (15, 15) from puzzle


def part_three(grid: List[List[int]]) -> int:
    return find_minimum_danger_path(grid)  # Bottom-right target


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 208
    print("Part 2:", part_two(data))    # 74
    print("Part 3:", part_three(data))  # 274
