#!/usr/bin/env python

import os
import re


def parse_input() -> list:
    """
    Reads the input file and splits the contents into a list of lines.

    Returns:
        list: A list of strings, where each string is line from the input file.
    """

    with open(
            os.path.splitext(os.path.basename(__file__))[0] + '.in',
            'r') as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Calculate the sum of numeric values that are ONLY adjacent to non-numeric
    symbols excluding ".".

    Adjacency is determined in an 8-directional manner, meaning a cell is
    adjacent if it is directly above, below, left, right, or diagonally
    connected.

    Args:
        data (list): The input data, where each element is a string
                     representing the line of input.

    Returns:
        int: The sum of all numeric values that meet the adjacency condition.
    """

    # Original Code
    # sum_parts = 0

    # # Identify all adjacent positions of non-numeric symbols
    # sym_adj = set()
    # for i, line in enumerate(data):
    #     for m in re.finditer(r"[^.\d]", line):
    #         j = m.start()
    #         sym_adj |= {
    #                 (r, c) for r in range(i-1, i+2) for c in range(j-1, j+2)
    #         }

    # # Sum up numeric values adjacent to symbols
    # for i, line in enumerate(data):
    #     for m in re.finditer(r"\d+", line):
    #         if any((i, j) in sym_adj for j in range(*m.span())):
    #             sum_parts += int(m.group())

    # return sum_parts

    # ChatGPT optimization recommendation:
    rows = len(data)
    cols = max(len(line) for line in data)
    symbol_positions = set()

    # Identify all adjacent positions of non-numeric symbols
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if not char.isdigit() and char != ".":
                for r in range(max(0, i - 1), min(rows, i + 2)):
                    for c in range(max(0, j - 1), min(cols, j + 2)):
                        symbol_positions.add((r, c))

    # Calculate the sum of numbers adjacent to symbols
    sum_parts = 0
    for i, line in enumerate(data):
        for m in re.finditer(r"\d+", line):
            start, end = m.span()
            if any((i, j) in symbol_positions for j in range(start, end)):
                sum_parts += int(m.group())

    return sum_parts


def part_two(data: list) -> int:
    """
    Calculate the sum of the products of a pair of gear ratios associated with
    gear positions.

    A gear position is marked by an asterisk ("*"). Numbers are associated with
    the gear positions if they are within an 8-directional adjacency. If
    exactly 2 numbers are associated with a gear, their product is added to the
    sum.

    Args:
        data (list): The input data, where each element is a string
                     representing the line of input.

    Returns:
        int: The sum of the products of pairs of numbers associated with the
             gear ratios.
    """

    # Original code
    # ratio_sum = 0

    # # Identify gear positions and initialize them with empty lists
    # gears = dict()
    # for i, line in enumerate(data):
    #     for m in re.finditer(r"\*", line):  # Match asterisks
    #         gears[(i, m.start())] = []

    # # Associate numbers with gear positions
    # for i, line in enumerate(data):
    #     for m in re.finditer(r"\d+", line):  # Match consecutive digits
    #         for r in range(i-1, i+2):
    #             for c in range(m.start()-1, m.end()+1):
    #                 if (r, c) in gears:
    #                     gears[(r, c)].append(int(m.group()))

    # # Calculate sum of products for pairs of associated numbers
    # for nums in gears.values():
    #     if len(nums) == 2:  # Consider only pairs of numbers
    #         ratio_sum += nums[0] * nums[1]

    # return ratio_sum

    # ChatGPT optimization recommendation
    rows = len(data)
    cols = max(len(line) for line in data)
    gears = {}

    # Step 1: Identify gear positions
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "*":
                gears[(i, j)] = []

    # Step 2: Find all numbers and associate them with nearby gears
    for i, line in enumerate(data):
        for match in re.finditer(r"\d+", line):
            num = int(match.group())
            start, end = match.span()

            # Check adjacency to all nearby gear positions
            for r in range(max(0, i - 1), min(rows, i + 2)):
                for c in range(max(0, start - 1), min(cols, end + 1)):
                    if (r, c) in gears:
                        gears[(r, c)].append(num)

    # Step 3: Calculate the sum of products for valid gear ratios
    ratio_sum = 0
    for nums in gears.values():
        if len(nums) == 2:
            ratio_sum += nums[0] * nums[1]

    return ratio_sum


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_one(data))  # 525911
    print("Part 2:", part_two(data))  # 75805607
