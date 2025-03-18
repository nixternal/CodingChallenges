#!/usr/bin/env python
"""
Advent of Code 2017 - Day 5: Maze of Twisty Trampolines, All Alike
This script reads a list of integer offsets from a file and simulates
a series of jumps based on specific rules to determine how many steps
are required to escape.

Part 1:
- Each step, the program jumps based on the current offset.
- The offset at the current position increases by 1 before the jump.

Part 2:
- If the offset is 3 or more, it decreases by 1 instead of increasing.
- Otherwise, it still increases by 1.
"""

from typing import List


def read_puzzle_input() -> List[int]:
    """
    Reads the input file and converts each line into an integer.

    :param filename: Name of the input file containing offsets.
    :return: A list of integers representing the jump offsets.
    """

    with open("05.in", "r") as file:
        return list(map(int, file.read().splitlines()))


def part_one(data: List[int]) -> int:
    """
    Solves Part 1 of the puzzle.

    Rules:
    - Start at index 0.
    - Read the offset at the current index.
    - Before moving, increase the value at the current index by 1.
    - Move forward or backward in the list based on the offset.
    - Repeat until jumping out of bounds.
    - Return the total number of steps taken.

    :param data: A list of integer offsets (a copy is recommended).
    :return: The number of steps required to exit the list.
    """

    steps = 0
    index = 0

    while 0 <= index < len(data):   # Continue while within bounds
        offset = data[index]        # Get the jump value
        data[index] += 1            # Increase the offset before jumping
        index += offset             # Move to the new index
        steps += 1                  # Count the step

    return steps                    # Return the total number of steps taken


def part_two(data: List[int]) -> int:
    """
    Solves Part 2 of the puzzle.

    Rules (similar to Part 1, but with a modification):
    - If the offset is 3 or greater, decrease it by 1 before jumping.
    - Otherwise, increase it by 1 before jumping.
    - Return the number of steps required to exit the list.

    :param data: A list of integer offsets (a copy is recommended).
    :return: The number of steps required to exit the list.
    """

    steps = 0
    index = 0

    while 0 <= index < len(data):   # Continue while within bounds
        offset = data[index]        # Get the jump value

        # Modify offset based on its value
        if offset >= 3:
            data[index] -= 1        # Decrease if 3 or more
        else:
            data[index] += 1        # Otherwise, increase

        index += offset             # Move to the new index
        steps += 1                  # Count the step

    return steps                    # Return the total number of steps taken


if __name__ == "__main__":
    """
    Main execution block:
    - Reads input data from file.
    - Runs Part 1 and Part 2 using copies of the original data.
    - Prints the results.
    """

    data = read_puzzle_input()      # Read input from file

    # Run each part with a fresh copy of data to avoid modification issues
    print("Part 1:", part_one(data[:]))  # Expected output: 343364
    print("Part 2:", part_two(data[:]))  # Expected output: 25071947
