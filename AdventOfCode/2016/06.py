#!/usr/bin/env python

from collections import Counter


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns it as a list of strings.

    The input file is expected to be named "06.in" and located in the same
    directory as the script. Each line in the file is treated as a separate
    string in the returned list.

    Returns:
        list: A list of strings, where each string represents a line from the
              input file.
    """

    with open("06.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> str:
    """
    Solves Part 1 of the puzzle by finding the most common character in each
    column of the input data.

    For each column (position) in the input strings, this function determines
    the most frequently occurring character. If the input strings are of
    unequal lengths, shorter strings are padded with a space (' ') to match
    the length of the longest string.

    Args:
        data (list): A list of strings representing the puzzle input.

    Returns:
        str: A string composed of the most common character in each column.
    """

    result = []

    # Determine the length of the longest string
    max_len = max(len(s) for s in data)

    for i in range(max_len):
        # Extract the i'th character from each string
        column = [s[i] if i < len(s) else None for s in data]
        # Use Counter to count occurrences of each character in the column
        most_common = Counter(column).most_common(1)
        if most_common:
            # Append the most common character to the result
            result.append(most_common[0][0])

    return ''.join(result)


def part_two(data: list) -> str:
    """
    Solves Part 2 of the puzzle by finding the least common character in each
    column of the input data.

    For each column (position) in the input strings, this function determines
    the least frequently occurring character. If the input strings are of
    unequal lengths, shorter strings are padded with a space (' ') to match
    the length of the longest string.

    Args:
        data (list): A list of strings representing the puzzle input.

    Returns:
        str: A string composed of the least common character in each column.
    """

    result = []

    # Determin the length of the longest string
    max_len = max(len(s) for s in data)

    for i in range(max_len):
        # Extract the i'th character from each string
        column = [s[i] if i < len(s) else None for s in data]
        # Use Counter to count occurrences of each character in a column
        char_counts = Counter(column)
        # Append the least common character. Lambda function doesn't give
        # pyright error
        result.append(min(char_counts, key=lambda k: char_counts[k]))
        # The following works as well, it just gives a pyright error in neovim
        # result.append(min(char_counts, key=char_counts.get))
    return ''.join(result)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # qqqluigu
    print("Part 2:", part_two(data))  # lsoypmia
