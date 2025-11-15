#!/usr/bin/env python

from collections import deque


def read_puzzle_input():
    with open("03.in", "r") as file:
        return file.read().split("\n\n")


def calculate_distance_sum(grid_text, use_diagonals=False):
    """Calculate sum of distances from marked cells to nearest unmarked cells using BFS."""
    lines = grid_text.splitlines()
    grid = [list(line.rstrip("\n")) for line in lines if line.strip() != ""]
    if not grid:
        return 0

    height = len(grid)
    width = len(grid[0])

    # Build padded grid with '.' border so outside is considered unmarked
    padded_height = height + 2
    padded_width = width + 2
    padded = [["."] * padded_width for _ in range(padded_height)]
    for row in range(height):
        for col in range(width):
            padded[row + 1][col + 1] = grid[row][col]

    # Distance array: -1 means unvisited
    distances = [[-1] * padded_width for _ in range(padded_height)]
    queue = deque()

    # Initialize BFS queue with all '.' cells (including padding border)
    for row in range(padded_height):
        for col in range(padded_width):
            if padded[row][col] == ".":
                distances[row][col] = 0
                queue.append((row, col))

    # Define movement directions
    if use_diagonals:
        directions = [
            # 4-directional
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            # Diagonals
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
    else:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 4-directional only

    # BFS to calculate distances
    while queue:
        row, col = queue.popleft()
        for delta_row, delta_col in directions:
            next_row = row + delta_row
            next_col = col + delta_col
            if (
                0 <= next_row < padded_height
                and 0 <= next_col < padded_width
                and distances[next_row][next_col] == -1
            ):
                distances[next_row][next_col] = distances[row][col] + 1
                queue.append((next_row, next_col))

    # Sum distances for original '#' cells (offset by 1 due to padding)
    total = 0
    for row in range(height):
        for col in range(width):
            if grid[row][col] == "#":
                total += distances[row + 1][col + 1]

    return total


def part_one(data):
    return calculate_distance_sum(data[0], use_diagonals=False)


def part_two(data):
    return calculate_distance_sum(data[1], use_diagonals=False)


def part_three(data):
    return calculate_distance_sum(data[2], use_diagonals=True)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 126
    print("Part 2:", part_two(data))  # 2667
    print("Part 3:", part_three(data))  # 10322
