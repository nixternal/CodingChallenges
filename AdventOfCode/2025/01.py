#!/usr/bin/env python
"""
Circular Track Movement Solver

Simulates movement on a circular track (positions 0-99) starting at position 50.
Tracks how many times position 0 is crossed during movement sequences.
"""

from typing import List


def read_puzzle_input() -> List[str]:
    """Read movement instructions from input file."""
    with open("01.in", "r") as file:
        return file.read().splitlines()


def parse_move(instruction: str) -> tuple[str, int]:
    """
    Parse a movement instruction into direction and distance.

    Args:
        instruction: String like "R25" or "L10"

    Returns:
        Tuple of (direction, distance)
    """
    return instruction[0], int(instruction[1:])


def part_one(instructions: List[str]) -> int:
    """
    Count zero crossings treating each instruction as a single jump.

    Moves the full distance specified in each instruction in one step,
    only checking if the final position equals zero.

    Args:
        instructions: List of movement commands (e.g., ["R25", "L10"])

    Returns:
        Number of times position 0 was landed on
    """
    TRACK_SIZE = 100
    START_POSITION = 50

    position = START_POSITION
    zero_count = 0

    for instruction in instructions:
        direction, distance = parse_move(instruction)

        if direction == "R":
            position = (position + distance) % TRACK_SIZE
        else:  # direction == "L"
            position = (position - distance) % TRACK_SIZE

        if position == 0:
            zero_count += 1

    return zero_count


def part_two(instructions: List[str]) -> int:
    """
    Count zero crossings for each individual step of movement.

    Breaks each instruction into individual steps and checks for zero
    crossing after each single position change.

    Args:
        instructions: List of movement commands (e.g., ["R25", "L10"])

    Returns:
        Number of times position 0 was crossed
    """
    TRACK_SIZE = 100
    START_POSITION = 50

    position = START_POSITION
    zero_count = 0

    for instruction in instructions:
        direction, distance = parse_move(instruction)
        step = 1 if direction == "R" else -1

        for _ in range(distance):
            position = (position + step) % TRACK_SIZE

            if position == 0:
                zero_count += 1

    return zero_count


if __name__ == "__main__":
    instructions = read_puzzle_input()
    print("Part 1:", part_one(instructions))  # 1021
    print("Part 2:", part_two(instructions))  # 5933
