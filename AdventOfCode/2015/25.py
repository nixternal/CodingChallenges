#!/usr/bin/env python
"""
This script calculates the value at a specific position in a triangular grid
of codes, where each code is generated based on the previous one using a
modular multiplication algorithm.

The main goal is to calculate the code at row 2981, column 3075 efficiently.
"""


def generate_next_code(current_code: int, steps: int) -> int:
    """
    Triangular Numbers aka Diagonal Grid Indexing (Cantor)

    Efficiently computes the code after a specified number of steps using
    modular exponentiation.

    The codes are generated using the recurrence relation:
        next_code = (current_code * 252533) % 33554393

    Instead of iterating `steps` times, use modular exponentiation to compute:
        result = (current_code * (252533^steps) % 33554393) % 33554393

    Args:
        current_code (int): The initial code value.
        steps (int): The number of iterations to advance.

    Returns:
        int: The resulting code after `steps` iterations.

    Time Complexity:
        O(log(steps)) due to the use of fast modular exponentiation.
    """

    # Compute (252533^steps) % 33554393 efficiently.
    multiplier = pow(252533, steps, 33554393)

    return (current_code * multiplier) % 33554393


def get_code_count(row: int, column: int) -> int:
    """
    Modular Exponentiation

    Calculates the position of the code in the triangular grid.

    The codes are arranged in a triangular grid:
        (1, 1) -> 1st code
        (2, 1) -> 2nd code
        (1, 2) -> 3rd code
        (3, 1) -> 4th code
        ...

    For a given row and column, the position is determined by summing all
    previous rows & adding the column index in the current row. Mathematically:
        position = sum(1 to (row + column - 1)) + column

    Args:
        row (int): The row number (1-based index).
        column (int): The column number (1-based index).

    Returns:
        int: The position of the code in the sequence.

    Example:
        For row=2, column=3:
            The code position is sum(range(1, 4)) + 3 = 6 + 3 = 9

    Time Complexity:
        O(row + column), as it involves summing integers up to row + column - 1
    """

    return sum(range(row + column - 1)) + column


def part_one() -> int:
    """
    Solves problem by calculating the code at position (2981, 3075).

    Steps:
    1. Determine position of the code in the sequence using `get_code_count`.
    2. Calculate the code at this position using `generate_next_code`.

    Returns:
        int: The code at row 2981, column 3075.

    Time Complexity:
        O(log(code_count)), where code_count is the position of the code in
        the grid.
    """

    # Step 1: Calculate the position of the code.
    code_count = get_code_count(2981, 3075)

    # Step 2: Calculate the code at the specified position.
    current_code = 20151125  # Starting code from problem statement.

    return generate_next_code(current_code, code_count - 1)


if __name__ == "__main__":
    print("Part 1:", part_one())  # 9132360
