#!/usr/bin/env python

"""
Puzzle Solver - Text Processing Challenge

This script solves a three-part puzzle that involves different text processing
techniques and calculating "memory units" based on the processed text.
"""


def read_puzzle_input() -> list:
    """
    Read the puzzle input data from a file.

    Returns:
        list: A list of strings, each representing a line from the input file.
    """

    with open("04.in", "r") as file:
        return file.read().splitlines()


def calculate_memory_units(data: list) -> int:
    """
    Calculate the total "memory units" for a list of strings.

    For each character:
    - If it's a letter: Convert to memory units by subtracting 64 from its
      ASCII value (e.g., 'A' = 1, 'B' = 2, etc.)
    - If it's a digit: Use the digit's numeric value

    Args:
        data (list): A list of strings to process

    Returns:
        int: The total memory units calculated from all characters
    """

    memory_units = 0

    for line in data:
        for char in line:
            # Calculate memory units based on character type
            if char.isalpha():
                # Convert letters to values (A=1, B=2, etc.)
                memory_units += ord(char) - 64
            else:
                # Use numeric value for digits
                memory_units += int(char)

    return memory_units


def part_one(data: list) -> int:
    """
    Part 1 solution: Calculate memory units from unmodified input data.

    Args:
        data (list): The raw input data

    Returns:
        int: Total memory units from the raw data
    """

    return calculate_memory_units(data)


def part_two(data: list) -> int:
    """
    Part 2 solution: Compress data by keeping the first and last 10% of each
    line, replacing the middle with the count of removed characters.

    Example:
    "ABCDEFGHIJ" becomes "A8J" (keep first and last character, 8 removed from
    middle)

    Args:
        data (list): The raw input data

    Returns:
        int: Total memory units from the compressed data
    """

    compressed_message = []

    for line in data:
        # Calculate how many characters to keep at each end
        keep = max(1, len(line) // 10)

        # Create the compressed line
        # Format:
        # [first keep chars][count of middle removed chars][last keep chars]
        middle_removed = len(line) - (keep * 2)
        new_line = f"{line[:keep]}{middle_removed}{line[-keep:]}"

        compressed_message.append(new_line)

    return calculate_memory_units(compressed_message)


def part_three(data: list) -> int:
    """
    Part 3 solution: Compress data using run-length encoding (RLE).

    Run-length encoding replaces consecutive identical characters with a count
    followed by the character. For example:
    "AAABBC" becomes "3A2B1C"

    Args:
        data (list): The raw input data

    Returns:
        int: Total memory units from the run-length encoded data
    """

    compressed_message = []

    for line in data:
        if not line:
            compressed_message.append("")
            continue

        # Initialize RLE variables
        compressed_line = []
        current_char = line[0]
        count = 1

        # Process each character
        for i in range(1, len(line)):
            if line[i] == current_char:
                # Increment count for repeated character
                count += 1
            else:
                # Add count + character to result and reset counter
                compressed_line.append(f"{count}{current_char}")
                current_char = line[i]
                count = 1

        # Add the final character run
        compressed_line.append(f"{count}{current_char}")

        # Join all runs into a single string
        compressed_message.append("".join(compressed_line))

    return calculate_memory_units(compressed_message)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 136231
    print("Part 2:", part_two(data))    # 25925
    print("Part 3:", part_three(data))  # 45242
