#!/usr/bin/env python
"""
Advent of Code - Day 1: The Tyranny of the Rocket Equation

This script calculates the total fuel required for a spacecraft's modules based
on their masses. The calculation is done in two parts:
1. Part One: Basic fuel calculation for each module.
2. Part Two: Fuel calculation accounting for the additional fuel required to
   transport the fuel itself.
"""


def read_puzzle_input() -> list[int]:
    """
    Reads the puzzle input from a file and returns a list of module masses.

    The input file is expected to contain one integer per line representing the
    mass of a module.

    Returns:
        List[int]: A list of module masses.
    """

    with open("01.in", "r") as file:
        return list(map(int, file.read().splitlines()))


def part_one(data: list[int]) -> int:
    """
    Calculates the total fuel required for all modules without accounting for
    the fuel's mass.

    The fuel required for each module is calculated as: floor(mass / 3) - 2.

    Args:
        data (List[int]): A list of module masses.

    Returns:
        int: The total fuel required for all modules.
    """

    return sum((x // 3) - 2 for x in data)


def part_two(data: list[int]) -> int:
    """
    Calculates the total fuel required for all modules, accounting for the
    fuel's mass.

    The calculation for each module includes the fuel required to transport
    the added fuel, recursively, until the fuel requirement becomes zero or
    negative.

    Args:
        data (List[int]): A list of module masses.

    Returns:
        int: The total fuel required for all modules, including fuel for the
        fuel.
    """

    fuel_required = 0
    for x in data:
        a = (x // 3) - 2
        while a > 0:
            fuel_required += a
            a = (a // 3) - 2

    return fuel_required


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3406342
    print("Part 2:", part_two(data))  # 5106629
