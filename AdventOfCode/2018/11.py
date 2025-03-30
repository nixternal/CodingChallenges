#!/usr/bin/env python

"""
Fuel Cell Grid Analyzer

This program solves the "Chronal Charge" problem from Advent of Code 2018,
Day 11. The problem involves finding the square region of a power grid with
the highest total power level.

Problem Description:
    - We have a 300x300 grid of fuel cells
    - Each cell has a power level calculated based on its coordinates and a
      serial number
    - Part 1: Find the 3×3 square with the highest total power level
    - Part 2: Find the square of any size with the highest total power level

The solution uses a summed-area table (also known as an integral image) for
efficient calculation of rectangular sums, achieving O(1) lookup time for any
size square.
"""


def power_level(x: int, y: int, serial_number: int) -> int:
    """
    Calculate the power level of a specific fuel cell.

    Args:
        x: The x-coordinate (1-indexed)
        y: The y-coordinate (1-indexed)
        serial_number: The grid serial number input

    Returns:
        The power level of the cell as an integer

    The power level calculation follows these steps:
    1. Find the rack ID (x-coordinate + 10)
    2. Multiply rack ID by y-coordinate
    3. Add the serial number
    4. Multiply by rack ID again
    5. Extract the hundreds digit
    6. Subtract 5
    """

    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    return (power // 100 % 10) - 5


def build_grid(serial_number: int, size: int = 300) -> list:
    """
    Build the complete power grid of the specified size.

    Args:
        serial_number: The grid serial number
        size: The size of the grid (default: 300)

    Returns:
        A 2D list representing the power level of each cell
    """

    # Using a list comprehension to efficiently build the grid
    return [
        [power_level(x, y, serial_number) for y in range(1, size + 1)]
        for x in range(1, size + 1)
    ]


def build_summed_area_table(grid: list) -> list:
    """
    Construct a summed-area table (integral image) from the power grid.

    A summed-area table allows O(1) calculation of the sum of any rectangular
    region in the original grid, drastically improving performance.

    Args:
        grid: The 2D power level grid

    Returns:
        A 2D summed-area table where each cell contains the sum of all cells
        above and to the left of it (inclusive)
    """

    size = len(grid)
    # Create a table with an extra row and column for easier calculations
    sat = [[0] * (size + 1) for _ in range(size + 1)]

    # Fill the summed-area table using the recurrence relation:
    # SAT(x,y) = grid(x,y) + SAT(x-1,y) + SAT(x,y-1) - SAT(x-1,y-1)
    for x in range(1, size + 1):
        for y in range(1, size + 1):
            sat[x][y] = (
                grid[x-1][y-1] + sat[x-1][y] + sat[x][y-1] - sat[x-1][y-1]
            )
    return sat


def get_square_power(sat: list, x: int, y: int, size: int) -> int:
    """
    Calculate the total power in a square region using the summed-area table.

    Args:
        sat: The summed-area table
        x: The top-left x-coordinate of the square (1-indexed)
        y: The top-left y-coordinate of the square (1-indexed)
        size: The size of the square

    Returns:
        The total power in the square region
    """

    # Formula to calculate sum of a rectangular region using summed-area table:
    # sum = SAT(x+s-1,y+s-1) - SAT(x-1,y+s-1) - SAT(x+s-1,y-1) + SAT(x-1,y-1)
    return (
        sat[x+size-1][y+size-1] -
        sat[x-1][y+size-1] -
        sat[x+size-1][y-1] +
        sat[x-1][y-1]
    )


def find_best_square(grid: list,
                     sat: list,
                     min_size: int = 3,
                     max_size: int = 3
                     ) -> tuple:
    """
    Find the square with the highest total power level.

    Args:
        grid: The 2D power level grid
        sat: The summed-area table
        min_size: The minimum square size to consider (default: 3)
        max_size: The maximum square size to consider (default: 3)

    Returns:
        A tuple (x, y, size, power) where:
        - x, y: Top-left coordinates of the best square (1-indexed)
        - size: Size of the best square
        - power: Total power level of the best square
    """

    best_x, best_y, best_size, max_power = 0, 0, 0, float('-inf')
    grid_size = len(grid)

    # Optimization: Only check sizes that fit within the grid
    max_size = min(max_size, grid_size)

    for s in range(min_size, max_size + 1):
        # Only iterate through valid starting positions for this square size
        for x in range(1, grid_size - s + 2):
            for y in range(1, grid_size - s + 2):
                power = get_square_power(sat, x, y, s)
                if power > max_power:
                    best_x, best_y, best_size, max_power = x, y, s, power

    return best_x, best_y, best_size, max_power


def part_one(grid: list, sat: list) -> str:
    """
    Solve Part 1: Find the 3×3 square with the highest power level.

    Args:
        grid: The 2D power level grid
        sat: The summed-area table

    Returns:
        The result as a string in the format "x,y"
    """

    x, y, _, _ = find_best_square(grid, sat, min_size=3, max_size=3)
    return f"{x},{y}"


def part_two(grid: list, sat: list) -> str:
    """
    Solve Part 2: Find the square of any size with the highest power level.

    Args:
        grid: The 2D power level grid
        sat: The summed-area table

    Returns:
        The result as a string in the format "x,y,size"
    """

    x, y, size, _ = find_best_square(grid, sat, min_size=1, max_size=300)
    return f"{x},{y},{size}"


if __name__ == "__main__":
    # Grid serial number (puzzle input)
    serial_number = 8561

    # Build the power grid and its summed-area table
    grid = build_grid(serial_number)
    sat = build_summed_area_table(grid)

    # Solve both parts of the puzzle
    print("Part 1:", part_one(grid, sat))  # 21,37
    print("Part 2:", part_two(grid, sat))  # 236,146,12
