#!/usr/bin/env python

"""
This script processes a text file ("08.in") containing lines of alphanumeric
characters and hyphens. It performs different character reduction operations
based on specific rules and computes results for three parts.

Reduction Rules:
1. A numerical character adjacent to an alphabetical character or a
   hyphen (`-`) results in both being removed.
2. Reductions occur sequentially (not simultaneously), meaning each reduction
   may affect the next one.
3. Some parts of the puzzle ignore hyphens during reductions.

Parts:
- Part 1: Count all alphabetical characters in the input file.
- Part 2: Count the remaining characters after applying the full reduction
          rules (including hyphens).
- Part 3: Count the remaining characters after reducing only number-letter
          pairs (excluding hyphens).
"""


def read_puzzle_input() -> list:
    """
    Reads the input file "08.in" and returns a list of strings
    (each line as an element).

    Returns:
        list: A list of strings representing the lines from the input file.
    """

    with open("08.in", "r") as file:
        return file.read().splitlines()


def reduce_line(line: str, allow_hyphen: bool) -> str:
    """
    Reduces a given line by removing character pairs based on the specified
    rules.

    Rules:
    - If a digit is next to a letter, both are removed.
    - If `allow_hyphen` is True, a digit next to a hyphen also results in
      both being removed.
    - Reductions occur one at a time from left to right.

    Args:
        line (str): The input line to be reduced.
        allow_hyphen (bool): Whether hyphen reductions should be allowed.

    Returns:
        str: The reduced line after all possible reductions are performed.
    """

    stack = []  # Stack to process character removals in sequence

    for char in line:
        # Check if the current character forms a removable pair with the last
        # stacked character
        if stack and (
                (char.isdigit() and (stack[-1].isalpha() or
                                     (allow_hyphen and stack[-1] == '-'))) or
                (char.isalpha() and stack[-1].isdigit()) or
                (char == '-' and stack[-1].isdigit() and allow_hyphen)):
            stack.pop()  # Remove the last character (perform reduction)
        else:
            stack.append(char)  # Keep the character

    return ''.join(stack)  # Return the fully reduced string


def part_one(data: list) -> int:
    """
    Counts the total number of alphabetical characters in the input file.

    Args:
        data (list): List of input lines.

    Returns:
        int: The total count of alphabetical characters.
    """

    return sum(char.isalpha() for line in data for char in line)


def part_two(data: list) -> int:
    """
    Counts the number of characters remaining after applying full reduction
    rules (removing number-letter and number-hyphen pairs).

    Args:
        data (list): List of input lines.

    Returns:
        int: The total count of characters remaining after reduction.
    """

    return sum(len(reduce_line(line, allow_hyphen=True)) for line in data)


def part_three(data: list) -> int:
    """
    Counts the number of characters remaining after applying a modified
    reduction rule, where number-letter pairs are removed but hyphens are
    ignored.

    Args:
        data (list): List of input lines.

    Returns:
        int: The total count of characters remaining after reduction
             (excluding hyphen removal).
    """

    return sum(len(reduce_line(line, allow_hyphen=False)) for line in data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 4581
    print("Part 2:", part_two(data))    # 770
    print("Part 3:", part_three(data))  # 1390
