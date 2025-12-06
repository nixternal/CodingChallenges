#!/usr/bin/env python

from math import prod

# Mapping of operator symbols to their corresponding functions
OPS = {"*": prod, "+": sum}


def read_puzzle_input() -> list:
    """Read puzzle input file and return lines as a list."""
    with open("06.in", "r") as f:
        return f.read().splitlines()


def part_one(data: list) -> int:
    """
    Process rows of numbers with operations defined in the last line.

    Args:
        data: List of strings where all but the last are rows of numbers,
              and the last line contains space-separated operators.

    Returns:
        Sum of results from applying each operation to its column.

    Example:
        Input: ["1 2 3", "4 5 6", "+ * +"]
        Columns: [1,4], [2,5], [3,6]
        Operations: +, *, +
        Result: sum([1,4]) + prod([2,5]) + sum([3,6]) = 5 + 10 + 9 = 24
    """
    # Transpose rows into columns of integers
    cols = zip(*(map(int, line.split()) for line in data[:-1]))
    # Extract operators from the last line
    ops = data[-1].split()
    # Apply each operator to its corresponding column and sum results
    return sum(OPS[op](col) for op, col in zip(ops, cols))


def part_two(data: list) -> int:
    """
    Process vertical columns reading right-to-left, where each column is
    a number followed by an operator character.

    Args:
        data: List of strings forming a grid where characters are read
              vertically from right to left.

    Returns:
        Sum of results from applying operations to accumulated numbers.

    Example:
        Input: ["12+", "34*", "56+"]
        Rightmost column: "2", "4", "6", "+" → numbers [246], op +
        Next column: "1", "3", "5", "*" → numbers [135], op *
        Result: sum([246]) + prod([135])
    """
    # Pad all lines to equal length for consistent column extraction
    lines = [line.ljust(max(map(len, data))) for line in data]
    # Generate columns right-to-left
    cols = ("".join(line[i] for line in lines) for i in reversed(range(len(lines[0]))))

    total = 0
    nums = []

    # Process each column
    for col in cols:
        if not col.strip():
            continue
        # Last character is the operator, rest is the number
        nums.append(int(col[:-1]))
        # If we found an operator, apply it and add to total
        if op := OPS.get(col[-1]):
            total += op(nums)
            nums = []

    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 6891729672676
    print("Part 2:", part_two(data))  # 9770311947567
