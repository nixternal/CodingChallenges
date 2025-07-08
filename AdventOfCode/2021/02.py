#!/usr/bin/env python

"""
Advent of Code 2021 - Day 2: Dive!
https://adventofcode.com/2021/day/2

PROBLEM DESCRIPTION:
A submarine needs to navigate through the ocean following a series of commands.
Each command is in the format: "<direction> <value>" where direction is one of:
- "forward X": moves forward X units
- "down X": changes depth/aim by X units (interpretation depends on part)
- "up X": changes depth/aim by -X units (interpretation depends on part)

PART 1: Simple Navigation
- "forward X": increases horizontal position by X
- "down X": increases depth by X
- "up X": decreases depth by X
Goal: Calculate horizontal position × final depth

PART 2: Navigation with Aim
- "forward X": increases horizontal position by X AND increases depth by (aim × X)
- "down X": increases aim by X
- "up X": decreases aim by X
Goal: Calculate horizontal position × final depth

INPUT FORMAT:
Text file with one command per line, e.g.:
forward 5
down 5
forward 8
up 3
"""

from typing import List, Tuple


def read_puzzle_input(filename: str = "02.in") -> List[str]:
    """
    Read and parse the input file containing submarine navigation commands.

    Args:
        filename: Path to the input file containing navigation commands

    Returns:
        List of command strings, each in format "<direction> <value>"

    Raises:
        FileNotFoundError: If the specified input file doesn't exist
    """

    try:
        with open(filename, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")


def parse_command(command: str) -> Tuple[str, int]:
    """
    Parse a single navigation command into direction and value.

    Args:
        command: Command string in format "<direction> <value>"

    Returns:
        Tuple of (direction, value) where direction is str and value is int

    Example:
        >>> parse_command("forward 5")
        ('forward', 5)
    """

    direction, value_str = command.split()
    return direction, int(value_str)


def part_one(data: list) -> int:
    """
    Solve Part 1: Simple submarine navigation.

    Navigation rules:
    - forward X: move horizontally forward by X units
    - down X: increase depth by X units
    - up X: decrease depth by X units

    Args:
        commands: List of navigation command strings

    Returns:
        Product of final horizontal position and final depth
    """

    horizontal_position = 0
    depth = 0

    for command in data:
        direction, value = parse_command(command)

        if direction == "forward":
            horizontal_position += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value

    return horizontal_position * depth


def part_two(data: list) -> int:
    """
    Solve Part 2: Submarine navigation with aim mechanics.

    Navigation rules:
    - forward X: move horizontally by X AND increase depth by (aim × X)
    - down X: increase aim by X
    - up X: decrease aim by X

    The key insight is that "down" and "up" don't directly change depth,
    but rather change the "aim" which affects future "forward" movements.

    Args:
        commands: List of navigation command strings

    Returns:
        Product of final horizontal position and final depth
    """

    horizontal_position = 0
    depth = 0
    aim = 0

    for command in data:
        direction, value = parse_command(command)

        if direction == "forward":
            horizontal_position += value
            depth += aim * value  # Depth changes based on current aim
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value

    return horizontal_position * depth


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1660158
    print("Part 2:", part_two(data))  # 1604592846
