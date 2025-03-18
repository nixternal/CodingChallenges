#!/usr/bin/env python

"""
https://en.wikipedia.org/wiki/Cramers_rule - algorithm used for P1 & P2
"""

import re


def read_puzzle_input() -> list:
    with open("13.in", "r") as file:
        return file.read().split("\n\n")


def part_one(data: list) -> int:
    """
    Solves the first part of the puzzle by calculating a total sum based on
    input data blocks.

    Each block contains numerical information that is parsed and used to
    calculate scaling factors (ca and cb) using geometric relationships.
    The conditions ensure valid solutions and contribute to the total sum.

    (ax, ay) - Total moves in X & Y direction w/ a single press of Button A
    (bx, by) - Total moves in X & Y direction w/ a single press of Button B
    (px, py) - Coordinates of the location of the Prize

    Button A press costs 3 tokens
    Button B press costs 1 token

    Parameters:
        data (list): A list of input data blocks as strings.

    Returns:
        int: The total sum calculated for part one of the puzzle.
    """

    total = 0
    for block in data:
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        # Count of A Button presses
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        # Count of B Button presses
        cb = (px - ax * ca) / bx
        if ca % 1 == cb % 1 == 0:  # ca & cb must be integers
            if ca <= 100 and cb <= 100:
                total += int(ca * 3 + cb)
    return total


def part_two(data: list) -> int:
    """
    Solves the second part of the puzzle by modifying the input conditions and
    calculating a total sum.

    This function adds a large offset (presses = 10_000_000_000_000) to the
    coordinates of point P before performing the calculations. The logic for
    calculating scaling factors (ca and cb) remains the same as in part one,
    but the offset simulates an extended state of the system.

    Parameters:
        data (list): A list of input data blocks as strings.

    Returns:
        int: The total sum calculated for part two of the puzzle.
    """

    presses = 10_000_000_000_000
    total = 0
    for block in data:
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        px += presses
        py += presses
        # Count of A Button presses
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        # Count of B Button presses
        cb = (px - ax * ca) / bx
        if ca % 1 == cb % 1 == 0:  # ca & cb must be integers
            total += int(ca * 3 + cb)
    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 29711
    print("Part 2:", part_two(data))  # 94955433618919
