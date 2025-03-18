#!/usr/bin/env python
"""
This script solves a two-part problem based on movement commands in the form
of "L2, R3, etc." It calculates the Manhattan distance from the starting point
to the endpoint and identifies the distance to the first location visited
twice.

Algorithms used:
1. Taxicab Geometry for movement in a grid.
2. Circular Indexing for direction tracking.
3. Set-based Search for finding repeated locations efficiently.
"""


def read_puzzle_input() -> list:
    """
    Reads the input from a file named "01.in", which contains comma-separated
    movement commands. Each command starts with a direction ('L' or 'R')
    followed by a number of steps.

    Returns:
        list: A list of movement commands as strings, e.g., ['L1', 'R2', 'L3'].
    """
    with open("01.in", "r") as file:
        return [x.strip() for x in file.read().split(',')]


def part_one(data: list) -> int:
    """
    Calculates the Manhattan distance from the starting point to the endpoint
    after following all commands.

    Algorithm:
    - Taxicab Geometry: A grid-based movement system where the distance
      between two points is the sum of the absolute differences of their
      Cartesian coordinates.
    - Circular Indexing: The directions (North, East, South, West) are stored
      in a circular list, and turning is handled using modular arithmetic.

    Args:
        data (list): A list of movement commands, e.g., ['L1', 'R2', 'L3'].

    Returns:
        int: The Manhattan distance between the starting point & the endpoint.
    """

    # Starting position and direction (facing north)
    x, y = 0, 0
    direction = 0  # 0 = north, 1 = east, 2 = south, 3 = west

    # Define movement vectors for each direction
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for move in data:
        turn = move[0]         # 'L' or 'R'
        steps = int(move[1:])  # The number of steps to move

        # Update direction
        if turn == 'L':
            direction = (direction - 1) % 4  # Turn left (counterclockwise)
        elif turn == 'R':
            direction = (direction + 1) % 4  # Turn right (clockwise)

        # Move in the current direction
        dx, dy = directions[direction]
        x += dx * steps
        y += dy * steps

    # Calculate and return the Manhattan distance
    return abs(x) + abs(y)


def part_two(data: list) -> int:
    """
    Identifies the Manhattan distance to the first location visited twice.

    Algorithm:
    - Taxicab Geometry: As in part one, to calculate distances.
    - Set-based Search: Used to efficiently track previously visited locations
      and detect the first repeated location.

    Args:
        data (list): A list of movement commands, e.g., ['L1', 'R2', 'L3'].

    Returns:
        int: The Manhattan distance to the first location visited twice.
             Returns 0 if no location is revisited.
    """

    # Starting position and direction (facing north)
    x, y = 0, 0
    direction = 0  # 0 = north, 1 = east, 2 = south, 3 = west

    # Define movement vectors for each direction
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Track all visited locations
    visited = set()
    visited.add((x, y))  # Add the starting position

    for move in data:
        turn = move[0]         # 'L' or 'R'
        steps = int(move[1:])  # The number of steps to move

        # Update the current direction based on the turn
        if turn == 'L':
            direction = (direction - 1) % 4  # Turn left (counterclockwise)
        elif turn == 'R':
            direction = (direction + 1) % 4  # Turn right (clockwise)

        # Move one step at a time to track intermediate positions
        dx, dy = directions[direction]

        for _ in range(steps):
            x += dx
            y += dy
            if (x, y) in visited:
                # If the current location has already been visited, return the
                # Manhattan distance
                return abs(x) + abs(y)
            visited.add((x, y))  # Mark the current location visited

    # Return 0 if no location is revisited
    return 0


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 299
    print("Part 2:", part_two(data))  # 181
