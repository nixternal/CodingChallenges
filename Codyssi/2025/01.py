#!/usr/bin/env python

from typing import List


def read_puzzle_input() -> List[str]:
    """
    Reads the puzzle input from a given file and returns a list of strings.
    Each line in the file is treated as an individual element in the list.

    Args:
        filename (str): The name of the input file. Defaults to "01.in".

    Returns:
        List[str]: A list of strings representing the puzzle input.
    """

    with open("01.in", "r") as file:
        return file.read().splitlines()


def evaluate_expression(offsets: List[str], signs: str) -> int:
    """
    Constructs and evaluates an arithmetic expression from the given offsets
    and signs.

    The first offset remains unchanged, and each subsequent offset is joined
    with a corresponding sign from the signs string.

    Args:
        offsets (List[str]): A list of numeric strings representing values to
                             be combined.
        signs (str): A string where each character represents an arithmetic
                     operator ('+' or '-').
                     The length of signs must be one less than the number of offsets.

    Returns:
        int: The result of evaluating the constructed arithmetic expression.
    """

    expression = offsets[0] + ''.join(
        f"{sign}{offset}" for sign, offset in zip(signs, offsets[1:])
    )
    return eval(expression)


def part_one(data: List[str]) -> int:
    """
    Solves Part 1 of the puzzle.

    Constructs an arithmetic expression using the original order of offsets and signs.

    Args:
        data (List[str]): The input data, where the last element is the sign string,
                          and all previous elements are numeric offsets.

    Returns:
        int: The computed result of Part 1.
    """

    return evaluate_expression(data[:-1], data[-1])


def part_two(data: list[str]) -> int:
    """
    Solves Part 2 of the puzzle.

    Constructs an arithmetic expression using the original order of offsets,
    but with the signs reversed.

    Args:
        data (List[str]): The input data, where the last element is the sign string,
                          and all previous elements are numeric offsets.

    Returns:
        int: The computed result of Part 2.
    """

    return evaluate_expression(data[:-1], data[-1][::-1])  # Reverse signs str


def part_three(data: list) -> int:
    """
    Solves Part 3 of the puzzle.

    This function pairs adjacent offsets together into single numbers,
    then constructs an arithmetic expression using reversed signs.

    Example:
        If the input offsets are ["10", "2", "3", "4"] and signs are "+-",
        they will be grouped into ["102", "34"] before processing.

    Args:
        data (List[str]): The input data, where the last element is the sign string,
                          and all previous elements are numeric offsets.

    Returns:
        int: The computed result of Part 3.
    """

    # Pair adjacent numbers
    offsets = [data[i] + data[i + 1] for i in range(0, len(data) - 1, 2)]
    return evaluate_expression(offsets, data[-1][::-1])  # Reverse signs str


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # -269
    print("Part 2:", part_two(data))    # -241
    print("Part 3:", part_three(data))  # -1881
