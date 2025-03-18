#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns a list of passphrases.

    The function opens the file "04.in" (which should contain one passphrase
    per line), reads its contents, and splits them into a list of strings
    (one per line).

    Returns:
        list: A list where each element is a passphrase (a single line from
              the file).
    """

    with open("04.in", "r") as file:
        return file.read().splitlines()


def is_valid(passphrase: str, sort: bool = False) -> bool:
    """
    Determines whether a given passphrase is valid according to the puzzle
    rules.

    A passphrase is a string of space-separated words. The validity check
    depends on the `sort` parameter:

    - If `sort` is False (default): The passphrase is valid if all words are
      unique.
    - If `sort` is True: The passphrase is valid if no two words are anagrams
      of each other.

    Args:
        passphrase (str): The passphrase to validate.
        sort (bool, optional): If True, checks for anagrams in addition to
                               duplicates. Defaults to False.

    Returns:
        bool: True if the passphrase is valid, False otherwise.
    """

    words = passphrase.split()  # Split the passphrase into a list of words
    if sort:  # Part 2
        # Normalize each word by sorting its characters (to detect anagrams)
        sorted_words = [''.join(sorted(word)) for word in words]

        # Ensure no duplicates
        return len(sorted_words) == len(set(sorted_words))

    # Ensure no duplicates
    return len(words) == len(set(words))


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle: Counts how many passphrases are valid.

    A passphrase is valid if it contains no duplicate words.

    Args:
        data (list): A list of passphrases (each passphrase is a string).

    Returns:
        int: The number of valid passphrases.
    """

    return sum(is_valid(phrase) for phrase in data)


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle: Counts how many passphrases are valid under
    new rules.

    A passphrase is valid if it contains no duplicate words and no two words
    are anagrams.

    Args:
        data (list): A list of passphrases (each passphrase is a string).

    Returns:
        int: The number of valid passphrases under the new rules.
    """

    return sum(is_valid(phrase, True) for phrase in data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 337
    print("Part 2:", part_two(data))  # 231
