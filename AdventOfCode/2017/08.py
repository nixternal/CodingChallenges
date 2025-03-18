#!/usr/bin/env python

import operator
from collections import defaultdict

# Dictionary mapping comparison operators to their
# corresponding Python functions
OPS = {
    '>': operator.gt,   # Greater than
    '>=': operator.ge,  # Greater than or equal to
    '<': operator.lt,   # Less than
    '<=': operator.le,  # Less than or equal to
    '==': operator.eq,  # Equal to
    '!=': operator.ne   # Not equal to
}


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns it as a list of lines.

    Returns:
        list: A list of strings, where each string represents a line from the
              input file.
    """

    with open("08.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Executes the instructions and returns the maximum value in any register
    at the end.

    The function processes each instruction, modifies register values based
    on conditions, and determines the largest value among all registers after
    execution.

    Args:
        data (list): A list of strings, where each string represents an
                     instruction.

    Returns:
        int: The highest value in any register at the end of execution.
    """

    # Dictionary to store register values, initialized to 0
    registers = defaultdict(int)

    for line in data:
        # Parse the instruction components
        reg, cmd, offset, _, if_reg, op, val = line.split()
        offset, val = int(offset), int(val)  # Convert values to integers

        # Check the condition: if true, modify the target register
        if OPS[op](registers[if_reg], val):
            registers[reg] += offset if cmd == 'inc' else -offset

    # Return the maximum value found in any register
    return max(registers.values())


def part_two(data: list) -> int:
    """
    Executes the instructions and tracks the highest value held by any
    register at any point.

    In addition to computing the final register values, this function also
    keeps track of the maximum value ever reached by any register during
    execution.

    Args:
        data (list): A list of strings, where each string represents an
                     instruction.

    Returns:
        int: The highest value any register held during execution.
    """

    # Dictionary to store register values, initialized to 0
    registers = defaultdict(int)

    # Variable to track the highest value ever held by any register
    max_reg_val = 0

    for line in data:
        # Parse the instruction components
        reg, cmd, offset, _, if_reg, op, val = line.split()
        offset, val = int(offset), int(val)  # Convert values to integers

        # Check the condition: if true, modify the target register
        if OPS[op](registers[if_reg], val):
            registers[reg] += offset if cmd == 'inc' else -offset
            # Update the maximum value ever held in any register
            max_reg_val = max(max_reg_val, registers[reg])

    # Return the highest value recorded at any point during execution
    return max_reg_val


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 5946
    print("Part 2:", part_two(data))  # 6026
