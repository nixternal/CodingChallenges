#!/usr/bin/env python
"""
Advent of Code 2020 - Day 2: Password Philosophy

This program validates passwords according to two different policy systems:
1. Part 1: Character frequency validation (old job's policy)
2. Part 2: Position-specific validation (new job's policy)

Input format: Each line contains a policy and password in the format:
"min-max letter: password" (e.g., "1-3 a: abcde")
"""


def read_puzzle_input() -> list:
    """
    Read the puzzle input from a file named '02.in'.

    Returns:
        list: A list of strings, where each string is a line from the input file.
              Each line contains a password policy and password to validate.
    """

    with open("02.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Validate passwords using the OLD policy system (character frequency).

    Policy: The password must contain the specified letter between min and max times (inclusive).
    Example: "1-3 a: abcde" means the password "abcde" must contain 'a' between 1 and 3 times.

    Args:
        data (list): List of strings, each containing a policy and password

    Returns:
        int: Number of valid passwords according to the old policy
    """

    count = 0

    for line in data:
        # Parse the line: "1-3 a: abcde" becomes ["1-3", "a", "abcde"]
        # We remove the colon first to make splitting easier
        policy, letter, password = line.replace(":", "").split(" ")

        # Extract min and max from policy (e.g., "1-3" becomes min=1, max=3)
        min_count, max_count = list(map(int, policy.split("-")))

        # Count how many times the required letter appears in the password
        letter_count = password.count(letter)

        # Check if the count is within the valid range (inclusive)
        if min_count <= letter_count <= max_count:
            count += 1

    return count


def part_two(data: list) -> int:
    """
    Validate passwords using the NEW policy system (position-specific).

    Policy: Exactly ONE of the two specified positions must contain the required letter.
    Positions are 1-indexed (first character is position 1, not 0).

    Example: "1-3 a: abcde" means exactly one of position 1 OR position 3 must be 'a'.
    - Position 1 is 'a' (matches)
    - Position 3 is 'c' (doesn't match)
    - Since exactly one position matches, this password is VALID.

    Args:
        data (list): List of strings, each containing a policy and password

    Returns:
        int: Number of valid passwords according to the new policy
    """

    count = 0

    for line in data:
        # Parse the line: "1-3 a: abcde" becomes ["1-3", "a", "abcde"]
        policy, letter, password = line.replace(":", "").split(" ")

        # Extract the two positions from policy (e.g., "1-3" becomes pos1=1, pos2=3)
        pos1, pos2 = list(map(int, policy.split("-")))

        # Get the characters at the specified positions
        # Subtract 1 because the policy uses 1-indexed positions, but Python uses 0-indexed
        char_at_pos1 = password[pos1 - 1]
        char_at_pos2 = password[pos2 - 1]

        # Check if exactly ONE of the positions contains the required letter
        # This is true when:
        # 1. The characters at both positions are different, AND
        # 2. At least one of them matches the required letter
        # (If they're different and one matches, then exactly one matches)
        if char_at_pos1 != char_at_pos2 and (
            char_at_pos1 == letter or char_at_pos2 == letter
        ):
            count += 1

    return count


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data))  # 460
    print("Part 2:", part_two(data))  # 251
