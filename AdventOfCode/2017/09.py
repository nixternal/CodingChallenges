#!/usr/bin/env python

"""
This script processes a stream of characters according to the rules of Advent
of Code 2017, Day 9. It calculates the total score of nested groups and
counts the number of non-canceled garbage characters.

Functions:
    - process_stream: Parses the input stream and returns both the total
                      score and garbage count.
    - solve_part1: Extracts the total group score from the processed stream.
    - solve_part2: Extracts the count of garbage characters from the
                   processed stream.
"""


def read_puzzle_input() -> str:
    # Read input from file
    with open("09.in", "r") as file:
        return file.read().strip()


def process_stream(stream: str):
    """
    Parses the input stream and calculates the total score of nested groups
    and the number of garbage characters.

    Parameters:
        stream (str): The input character stream.

    Returns:
        tuple: (total_score, garbage_count)
    """

    total_score = 0
    garbage_count = 0
    depth = 0
    in_garbage = False
    ignore_next = False

    for char in stream:
        if ignore_next:
            ignore_next = False
            continue

        if in_garbage:
            if char == '>':  # End of garbage
                in_garbage = False
            elif char == '!':  # Ignore next character
                ignore_next = True
            else:
                garbage_count += 1  # Count garbage characters
        else:
            if char == '{':  # Start a new group
                depth += 1
                total_score += depth
            elif char == '}':  # Close a group
                depth -= 1
            elif char == '<':  # Start garbage collection
                in_garbage = True

    return total_score, garbage_count


def part_one(data: str) -> int:
    """
    Solves Part 1 by computing the total score of all groups in the stream.

    Parameters:
        stream (str): The input character stream.

    Returns:
        int: The total score of the groups.
    """

    return process_stream(data)[0]


def part_two(data: str) -> int:
    """
    Solves Part 2 by computing the number of non-canceled garbage characters.

    Parameters:
        stream (str): The input character stream.

    Returns:
        int: The number of garbage characters.
    """

    return process_stream(data)[1]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 17390
    print("Part 2:", part_two(data))  # 7825
