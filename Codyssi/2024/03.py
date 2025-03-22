#!/usr/bin/env python3

"""
Codyssi 2024 Unformatted Readings Puzzle Solver

This script solves a three-part puzzle involving number base conversions:
1. Calculate the composition sum (sum of all number bases in the file)
2. Convert all readings to decimal (base-10) and find their sum
3. Convert the decimal sum to a custom base-65 representation

The input file format has each line containing a reading and its base:
"<reading> <base>"

Example: "100011101111110010101101110011 2" (binary number followed by base)
"""


def read_puzzle_input():
    """
    Read the puzzle input file and return each line as a list element.

    Args:
        filename (str): Path to the input file. Default is "03.in".

    Returns:
        list: List of strings, each representing a line from the input file.
    """

    with open("03.in", "r") as file:
        return file.read().splitlines()


def part_one(data):
    """
    Solve part 1: Calculate the composition sum.

    The composition sum is the sum of the number bases of all readings.

    Args:
        data (list): List of strings, each containing a reading and its base.

    Returns:
        int: The composition sum.
    """

    return sum(int(line.split()[1]) for line in data)


def part_two(data):
    """
    Solve part 2: Calculate the sum of all readings converted to decimal.

    Each reading is converted from its specified base to decimal (base-10),
    then all converted values are summed.

    Args:
        data (list): List of strings, each containing a reading and its base.

    Returns:
        int: The sum of all readings in decimal.
    """

    total = 0
    for line in data:
        reading, base = line.split()
        base = int(base)
        # Python's int() function can convert from any base (2-36) to decimal
        decimal_value = int(reading, base)
        total += decimal_value
    return total


def part_three(data):
    """
    Solve part 3: Convert the decimal sum to a custom base-65 representation.

    The custom base-65 uses digits 0-9, uppercase A-Z, lowercase a-z, and !@#
    to represent values 0-64.

    Args:
        data (list): List of strings, each containing a reading and its base.

    Returns:
        str: The decimal sum converted to the custom base-65 representation.
    """

    # Define the custom base-65 symbol set
    base65_symbols = (
        "0123456789"  # Values 0-9
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Values 10-35
        "abcdefghijklmnopqrstuvwxyz"  # Values 36-61
        "!@#"  # Values 62-64
    )

    # Get the decimal sum from part 2
    decimal_sum = part_two(data)

    # Handle special case: if sum is 0
    if decimal_sum == 0:
        return "0"

    # Convert from decimal to base-65
    result = ""
    while decimal_sum > 0:
        # Get the remainder when divided by 65 (this is the current digit)
        digit = decimal_sum % 65

        # Prepend the corresponding symbol to our result
        result = base65_symbols[digit] + result

        # Integer division to get the next value to process
        decimal_sum //= 65

    return result


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 7184
    print("Part 2:", part_two(data))    # 393195859205
    print("Part 3:", part_three(data))  # 5Dv0Xij
