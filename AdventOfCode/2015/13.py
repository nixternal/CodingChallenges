#!/usr/bin/env python

"""
A program to calculate optimal seating arrangements based on happiness
relationships. This solution addresses the Advent of Code day 13 problem,
calculating maximum total happiness in a circular seating arrangement.
"""

import re
from itertools import permutations


def read_puzzle_input() -> str:
    """
    Reads the puzzle input from the file '13.in'.

    Returns:
        str: The raw puzzle input as a string.
    """

    with open("13.in", "r") as file:
        return file.read()


def calculate_path_sum(path, h):
    """
    Calculates the total happiness for a given seating arrangement.

    Args:
        path: A tuple containing the seating order of people
        h: Nested dictionary of happiness values between pairs of people

    Returns:
        int: The total happiness value for the seating arrangement,
             calculated as the sum of bidirectional happiness between adjacent
             seats
    """

    pairs = list(zip(path, path[1:] + path[:1]))
    return sum(h[a][b] + h[b][a] for a, b in pairs)


def calculate_max_happiness(data: str) -> int:
    """
    Calculates the maximum possible total happiness from the input data.

    Args:
        data: A string containing happiness relationships in the format
             "Alice would gain/lose X happiness units by sitting next to Bob."

    Returns:
        int: The maximum possible total happiness achievable by any seating
             arrangement

    Note:
        The function uses regex to parse the input and creates a nested
        dictionary of happiness values. It then tries all possible
        permutations to find the optimal seating arrangement.
    """

    r = r"(\w+).+(\w) (\d+).+?(\w+)\."
    matches = re.findall(r, data)

    # Create nested dictionary of happiness values
    h = {}

    for a, mood, units, b in matches:
        if a not in h:
            h[a] = {}

        # Convert gai(n)/los(e) to +/- numbers based on compairsons.
        # n = gain, e = lose
        mood_multiplier = 1 if mood == "n" else (-1 if mood == "e" else 0)
        h[a][b] = int(units) * mood_multiplier

    return max(calculate_path_sum(p, h) for p in permutations(h.keys()))


def part_one(data: str) -> int:
    """
    Solves part one of the puzzle: finding maximum happiness with original
    group.

    Args:
        data: The puzzle input string

    Returns:
        int: Maximum achievable happiness with the original group
    """

    return calculate_max_happiness(data)


def part_two(data: str) -> int:
    """
    Solves part two of the puzzle: finding maximum happiness with yourself
    added.

    Adds a new person 'Rich' who has 0 happiness relationship with everyone
    else and recalculates the maximum possible happiness.

    Args:
        data: The puzzle input string

    Returns:
        int: Maximum achievable happiness with yourself added to the group
    """

    # Extract set of all people from the input
    people = set(line.split(' ')[0] for line in data.splitlines())

    # Add neutral happiness relationships with me being added to the seating
    for p in people:
        data += f"{p} x gain 0 x Rich.\nRich x gain 0 x {p}.\n"

    return calculate_max_happiness(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 733
    print("Part 2:", part_two(data))  # 725
