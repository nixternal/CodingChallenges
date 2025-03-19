#!/usr/bin/env python

"""
Puzzle Solution Script

This script solves a multi-part puzzle involving calculations and range
operations. Each part processes input data in different ways to produce
numerical answers.

Input format: Each line contains space-separated expressions (Part 1) or
range pairs (Parts 2-3). Range pairs are formatted as "start-end"
(e.g., "5-10").
"""


def read_puzzle_input() -> list:
    """
    Read puzzle input from the file '03.in'.

    Returns:
        list: A list of strings where each string is a line from the input file
    """
    with open("03.in", "r") as file:
        return file.read().splitlines()


def calc_total_number(expression: str) -> int:
    """
    Calculate a value based on a mathematical expression.

    Steps:
    1. Evaluate the expression string as a Python expression using eval()
    2. Take the absolute value of the result
    3. Add 1 to the absolute value

    Args:
        expression (str): A string containing a mathematical expression

    Returns:
        int: The absolute value of the evaluated expression plus 1

    Example:
        calc_total_number("5*3") returns 16 (|15| + 1)
        calc_total_number("-7+2") returns 6 (|−5| + 1)
    """
    return abs(eval(expression)) + 1


def part_one(data: list) -> int:
    """
    Process all mathematical expressions in the data and sum their calculated
    values.

    For each line in the data:
    1. Split the line into separate expressions by spaces
    2. Calculate the value of each expression using calc_total_number()
    3. Sum all calculated values

    Args:
        data (list): List of strings, each containing space-separated
                     expressions

    Returns:
        int: Sum of all calculated values
    """
    return sum(calc_total_number(expression)
               for line in data
               for expression in line.split())


def part_two(data: list) -> int:
    """
    Count the total number of unique boxes across all piles.

    For each line in the data:
    1. Create an empty set to track unique box numbers
    2. For each pile (represented as "start-end"):
       a. Split into start and end values
       b. Add all numbers in the range [start, end] to the set
    3. Count unique box numbers (length of the set)
    4. Sum these counts across all lines

    Args:
        data (list): List of strings, each containing space-separated range
                     pairs

    Returns:
        int: Total count of unique box numbers

    Example:
        If a line contains "1-3 2-5", the unique boxes are [1,2,3,4,5]
        (count: 5)
    """
    total = 0
    for line in data:
        boxes = set()  # Using set for O(1) lookups and automatic uniqueness
        for pile in line.split():
            a, b = map(int, pile.split('-'))  # Convert start & end to integers
            boxes.update(range(a, b + 1))  # Add integers from a-b (inclusive)
        total += len(boxes)
    return total


def part_three(data: list) -> int:
    """
    Find the maximum number of unique boxes when processing lines in pairs.

    Process:
    1. Process the data line-by-line, building a set of unique box numbers
    2. When an odd-indexed line is processed (lines are 0-indexed):
       a. Check if the current set size is larger than the previous maximum
       b. If so, update the maximum
       c. Reset the set for the next pair of lines

    Args:
        data (list): List of strings, each containing space-separated range
                     pairs

    Returns:
        int: Maximum number of unique boxes found in any pair of consecutive
             lines

    Note:
        - Line pairs are processed together (lines 0&1, lines 2&3, etc.)
        - The maximum is checked after processing each complete pair
    """
    max_boxes = 0
    boxes = set()

    for i, line in enumerate(data):
        # Process each pile in the current line
        for pile in line.split():
            a, b = map(int, pile.split('-'))
            boxes.update(range(a, b + 1))

        # After every second line (odd index), check if we have a new maximum
        if i % 2 == 1:  # This is an odd-indexed line (second in a pair)
            max_boxes = max(max_boxes, len(boxes))
            boxes = set()  # Reset for the next pair

    return max_boxes


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 46890
    print("Part 2:", part_two(data))    # 39786
    print("Part 3:", part_three(data))  # 959
