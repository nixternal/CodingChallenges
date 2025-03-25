#!/usr/bin/env python

from collections import Counter


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '02.in' and returns it as a list
    of strings. Each string represents a box ID.

    Returns:
        list: A list of box ID strings.
    """

    with open("02.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Computes the checksum for the list of box IDs.
    The checksum is calculated by counting how many box IDs contain:
    - Exactly two of any letter
    - Exactly three of any letter

    The final checksum is the product of these two counts.

    Args:
        data (list): List of box ID strings.

    Returns:
        int: The checksum value.
    """

    twos = 0  # Count of box IDs with a letter appearing exactly twice
    threes = 0  # Count of box IDs with a letter appearing exactly three times

    for line in data:
        # Use Counter to simplify character frequency counting
        counts = Counter(line)

        # Check if any letter appears exactly twice
        twos += 2 in counts.values()

        # Check if any letter appears exactly three times
        threes += 3 in counts.values()

    # Return checksum as the product of twos and threes counts
    return threes * twos


def part_two(data: list) -> str:
    """
    Finds the two box IDs that differ by exactly one character in the same
    position. Returns the common letters of these two IDs (excluding the
    differing character).

    Args:
        data (list): List of box ID strings.

    Returns:
        str: The common letters of the two matching box IDs.
    """

    for i, id1 in enumerate(data):
        for id2 in data[i + 1:]:  # Avoid redundant comparisons

            # Count differences directly using sum with a generator
            diffs = [(c1, c2) for c1, c2 in zip(id1, id2) if c1 != c2]

            # If exactly one character is different, return the common part
            if len(diffs) == 1:
                return "".join(c1 for c1, c2 in zip(id1, id2) if c1 == c2)

    return ""  # Return empty string if no matching IDs are found


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 9633
    print("Part 2:", part_two(data))  # lujnogabetpmsydyfcovzixaw
