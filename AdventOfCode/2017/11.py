#!/usr/bin/env python


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named "11.in".
    Assumes the input is a comma-separated list of hexagonal movement
    directions.

    Returns:
        list: A list of movement directions as strings.
    """
    with open("11.in", "r") as file:
        return file.read().strip().split(',')


def hex_distance(steps: list) -> tuple[int, int]:
    """
    Calculates the final distance from the starting point and the maximum
    distance reached at any point while following a series of steps in a
    hexagonal grid.

    Uses cube coordinates (x, y, z) to track movement.

    Args:
        steps (list): A list of movement directions as strings.

    Returns:
        tuple[int, int]: A tuple containing:
            - The final distance from the starting point.
            - The maximum distance reached at any point during the path.
    """
    # Mapping of movement directions to coordinate changes in cube coordinates
    moves = {
        "n":  (0, 1, -1),
        "s":  (0, -1, 1),
        "ne": (1, 0, -1),
        "nw": (-1, 1, 0),
        "se": (1, -1, 0),
        "sw": (-1, 0, 1)
    }

    # Initialize coordinates at the origin
    x = y = z = 0
    # Track the maximum distance reached during the path
    max_distance = 0

    # Process each step in the input list
    for step in steps:
        dx, dy, dz = moves[step]  # Get coordinate change for the step
        x, y, z = x + dx, y + dy, z + dz  # Update position
        # Update max distance
        max_distance = max(max_distance, max(abs(x), abs(y), abs(z)))

    # Compute final distance from the origin
    return max(abs(x), abs(y), abs(z)), max_distance


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle: Computes the final distance from the
    starting point.

    Args:
        data (list): List of movement directions.

    Returns:
        int: The final distance from the start.
    """
    return hex_distance(data)[0]


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle: Computes the maximum distance reached at any
    point.

    Args:
        data (list): List of movement directions.

    Returns:
        int: The maximum distance reached.
    """
    return hex_distance(data)[1]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 805
    print("Part 2:", part_two(data))  # 1535

