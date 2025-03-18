#!/usr/bin/env python

import re


def read_puzzle_input() -> str:
    """
    Read the file and create a big string of the data, or the corrupted memory
    per the puzzle so the parts can do their magic with it.

    :return: A big ol' string of corrupted memory data
    :rtype: str
    """
    with open("03.in", "r") as file:
        memory = file.read()
    return memory


def get_matches(memory: str) -> list:
    """
    Find all of the digits inside of a "mul()", ie mul(1,2) would give us
    [1,2].

    :param str memory: The memory dump from the puzzle input
    :return: List of all the "mul()" digits
    :rtype: list
    """
    matches = re.findall(r'mul\((\d+),(\d+)\)', memory, re.MULTILINE)
    return matches


def part_one(memory: str) -> int:
    """
    Get all of the "mul()" digits from "get_matches()" function, multiply each
    pair of digits and then add their products together.

    :param str memory: The memory dump from the puzzle input
    :return: The sum, aka the answer of part 1
    :rtype: int
    """
    results = [int(a) * int(b) for a, b in get_matches(memory)]
    return sum(results)


def part_two(memory: str, enabled: bool) -> int:
    """
    In part 2 of the puzzle we only sum the values of our digits if they follow
    a "do()" function in the corrupted memory dump. Not gonna lie, I needed
    Reddit's help with this one.

    :param str memory: The memory dump from the puzzle input
    :param bool enabled: A logic helper to separate the do's & the dont's math
    :return: The sum, aka the answer of part 2
    :rtype: int
    """
    if enabled:
        if "don't()" in memory:
            i = memory.index("don't")
            return part_one(memory[:i]) + part_two(memory[i:], False)
        else:
            return part_one(memory)
    else:
        if "do()" in memory:
            i = memory.index("do()")
            return part_two(memory[i:], True)
        else:
            return 0


if __name__ == "__main__":
    print("Part 1:", part_one(read_puzzle_input()))        # 174960292
    print("Part 2:", part_two(read_puzzle_input(), True))  # 56275602
