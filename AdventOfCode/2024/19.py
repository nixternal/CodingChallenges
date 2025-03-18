#!/usr/bin/env python

"""
This script processes a puzzle input to analyze designs based on predefined
patterns. It determines whether a design can be constructed using the patterns
and calculates the total number of ways a design can be constructed. The
script consists of two parts:
    1. Counting the number of valid designs.
    2. Summing all possible ways to construct valid designs.

Key components:
- Patterns (PATTERNS): A global set of string fragments.
- Maximum length of a pattern (MAXLENGTH): Global integer derived from PATTERNS
- Cached functions for computational efficiency.
"""

from functools import cache

# Global variables to store the pattern set and its maximum length
PATTERNS = None
MAXLENGTH = 0


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '19.in' and initializes global
    variables.

    Returns:
        list: A list of strings where:
              - The first line contains the patterns separated by ", ".
              - The subsequent lines are designs to be analyzed.

    Side effects:
        Sets the global PATTERNS variable to a set of patterns.
        Sets the global MAXLENGTH variable to the maximum length of any pattern
    """

    global PATTERNS
    global MAXLENGTH
    with open("19.in", "r") as file:
        data = file.read().splitlines()
    PATTERNS = set(data[0].split(", "))
    MAXLENGTH = max(map(len, PATTERNS))
    return data


@cache
def design_possible(design) -> bool:
    """
    Checks if a given design can be constructed using the predefined patterns.

    Args:
        design (str): The design string to analyze.

    Returns:
        bool: True if the design can be constructed using the patterns,
              False otherwise.
    """

    if design == "":
        return True
    for i in range(min(len(design), MAXLENGTH) + 1):
        if design[:i] in PATTERNS and design_possible(design[i:]):
            return True
    return False


@cache
def total_possibilities(design) -> int:
    """
    Calculates the total number of ways a given design can be constructed using
    the patterns.

    Args:
        design (str): The design string to analyze.

    Returns:
        int: The total number of ways the design can be constructed.
    """

    if design == "":
        return 1
    count = 0
    for i in range(min(len(design), MAXLENGTH) + 1):
        if design[:i] in PATTERNS:
            count += total_possibilities(design[i:])
    return count


def part_one(data: list) -> int:
    return sum(1 if design_possible(design) else 0 for design in data[2:])


def part_two(data: list) -> int:
    return sum(total_possibilities(design) for design in data[2:])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 228
    print("Part 2:", part_two(data))  # 584553405070389
