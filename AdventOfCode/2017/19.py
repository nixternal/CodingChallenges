#!/usr/bin/env python

"""
Advent of Code 2017, Day 19: A Series of Tubes

This script solves the Day 19 puzzle from Advent of Code 2017.
The puzzle involves following a path through a grid of ASCII characters,
collecting letters along the way and counting the total steps taken.

Problem description:
- You follow a path on a grid of ASCII characters.
- The path starts at the '|' character in the first row.
- The path consists of '|', '-', '+', letters, and spaces.
- You follow the path until you reach the end (a space character).
- Part 1: Collect all letters you encounter on the path.
- Part 2: Count the total number of steps taken.

Example grid:
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Expected output:
- Part 1: "ABCDEF" (the letters encountered)
- Part 2: 38 (the total number of steps)
"""


def read_puzzle_input() -> list:
    """
    Read the puzzle input from a file named '19.in'.

    Returns:
        list: A list of strings, where each string represents a row in the grid
    """

    with open("19.in", "r") as file:
        return file.read().splitlines()


def follow_path(grid):
    """
    Follow the path through the grid, collecting letters and counting steps.

    The path follows these rules:
    - Start at the '|' character in the first row
    - Continue in the current direction until hitting a '+' intersection
    - At an intersection, choose the path that doesn't go back
    - Collect any letters encountered
    - Count each step taken
    - Stop when reaching the end of the path (a space character)

    Args:
        grid (list): A list of strings representing the grid.

    Returns:
        tuple: A tuple containing:
            - A string of collected letters (Part 1 answer)
            - The total number of steps taken (Part 2 answer)
    """

    # Find the starting position (the '|' character in the first row)
    start_col = grid[0].index('|')
    pos = (0, start_col)

    # Initialize direction to move downward
    # Directions are represented as (row_delta, col_delta)
    # (1, 0) = down, (-1, 0) = up, (0, 1) = right, (0, -1) = left
    direction = (1, 0)  # Start by moving down

    # Track the collected letters and steps
    letters = []  # Will store all letters encountered
    steps = 0     # Will count total steps taken

    while True:
        # Move to the next position
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        steps += 1

        # Get the current character (or handle out of bounds)
        row, col = pos
        # Check if position is within grid boundaries
        if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
            char = grid[row][col]
        else:
            # We've gone out of bounds, so we're done
            break

        # If we hit a space, we've reached the end of the path
        if char == ' ':
            break

        # If we hit a letter, collect it for Part 1
        if char.isalpha():
            letters.append(char)

        # If we hit a '+', we need to change direction
        if char == '+':
            # Try all four possible directions
            for new_dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                # Skip the opposite direction (the one we came from)
                # This prevents backtracking
                if (new_dir[0] == -direction[0] and
                        new_dir[1] == -direction[1]):
                    continue

                # Check if there's a valid path in this direction
                # A valid path is within grid bounds and not a space
                new_row, new_col = row + new_dir[0], col + new_dir[1]
                if (0 <= new_row < len(grid) and
                    0 <= new_col < len(grid[new_row]) and
                        grid[new_row][new_col] != ' '):
                    # Found a valid direction, update and continue
                    direction = new_dir
                    break

    # Return both parts' answers: the collected letters and total steps
    return ''.join(letters), steps


def part_one(data: list) -> str:
    """
    Solve Part 1: Collect all letters encountered on the path.

    Args:
        data (list): The puzzle input as a grid.

    Returns:
        str: The sequence of letters encountered on the path.
    """

    letters, _ = follow_path(data)
    return letters


def part_two(data: list) -> int:
    """
    Solve Part 2: Count the total number of steps taken.

    Args:
        data (list): The puzzle input as a grid.

    Returns:
        int: The total number of steps taken to traverse the path.
    """

    _, steps = follow_path(data)
    return steps


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # GEPYAWTMLK
    print("Part 2:", part_two(data))  # 17628
