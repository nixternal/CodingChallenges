#!/usr/bin/env python3

import string
from typing import Generator


def read_puzzle_input(filename: str = "05.in") -> str:
    """
    Read the puzzle input from a file.

    Args:
        filename (str, optional): Path to the input file. Defaults to "05.in".

    Returns:
        str: The polymer string from the input file, with whitespace stripped.
    """

    with open(filename, "r") as file:
        return file.read().strip()


def react_polymer(polymer: str) -> str:
    """
    Fully react a polymer by removing adjacent units that are the same type
    (letter) but opposite case.

    This function uses a stack-based approach to efficiently reduce the
    polymer:
        - If the current unit reacts with the last unit in the stack (same
          letter, different case), remove the last unit
        - Otherwise, append the current unit to the stack

    Example:
    - 'aA' reduces to '' (units annihilate each other)
    - 'abBA' reduces to ''
    - 'abAB' remains 'abAB' (no reaction)

    Args:
        polymer (str): The input polymer string to be reduced.

    Returns:
        str: The fully reduced polymer.
    """

    stack = []
    for unit in polymer:
        # Check if the current unit reacts with the last unit in the stack
        if stack and stack[-1] != unit and stack[-1].lower() == unit.lower():
            stack.pop()  # Remove the last unit if it reacts
        else:
            stack.append(unit)  # Otherwise keep the unit
    return "".join(stack)


def generate_reduced_polymers(polymer: str) -> Generator[int, None, None]:
    """
    Generate lengths of polymers after removing each lowercase letter
    and fully reducing.

    Optimization: Uses a generator to avoid creating multiple lists in memory.
    Removes both lowercase and uppercase instances of each letter.

    Args:
        polymer (str): The original polymer string.

    Yields:
        int: Length of the polymer after removing a specific letter type
             and fully reducing.
    """

    for unit in string.ascii_lowercase:
        # Remove both lowercase and uppercase instances of the current letter
        modified_polymer = polymer.replace(unit, "").replace(unit.upper(), "")
        yield len(react_polymer(modified_polymer))


def part_one(data: str) -> int:
    """
    Solve Part 1: Find the length of the polymer after full reduction.

    Args:
        data (str): The input polymer string.

    Returns:
        int: Length of the fully reduced polymer.
    """

    return len(react_polymer(data))


def part_two(data: str) -> int:
    """
    Solve Part 2: Find the shortest possible polymer length
    after removing one letter type.

    Args:
        data (str): The input polymer string.

    Returns:
        int: Length of the shortest possible polymer.
    """

    return min(generate_reduced_polymers(data))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10978
    print("Part 2:", part_two(data))  # 4840
