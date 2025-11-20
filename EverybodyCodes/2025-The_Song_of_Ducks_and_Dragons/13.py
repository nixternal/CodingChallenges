#!/usr/bin/env python
"""
Puzzle solver for circular dial navigation problems.

This module solves three related problems involving building circular dials
and finding values at specific positions after wrapping around the dial.
"""


def read_puzzle_input() -> list[str]:
    """Read and parse puzzle input from file.

    Returns:
        List of input sections split by blank lines.
    """
    with open("13.in", "r") as file:
        return file.read().split("\n\n")


def part_one(data: list[str]) -> int:
    """Build a dial by alternately appending and prepending numbers.

    Starting with [1], alternately append and prepend numbers from the input.
    Find the value at position (index_of_1 + 2025) % dial_length.

    Args:
        data: List where first element contains newline-separated numbers.

    Returns:
        The value at the calculated position in the dial.
    """
    numbers = [int(line) for line in data[0].splitlines()]
    dial = [1]

    for i, number in enumerate(numbers):
        if i % 2 == 0:  # Even indices: append right
            dial.append(number)
        else:  # Odd indices: prepend left
            dial.insert(0, number)

    target_index = (dial.index(1) + 2025) % len(dial)
    return dial[target_index]


def part_two(data: list[str]) -> int:
    """Build a dial using ranges, alternating append and prepend operations.

    Each line represents a range (x-y). Convert to a list of numbers and
    alternately append or prepend to the dial.

    Args:
        data: List where second element contains newline-separated ranges.

    Returns:
        The value at position (index_of_1 + 20252025) % dial_length.
    """
    ranges = [tuple(map(int, line.split("-"))) for line in data[1].splitlines()]
    dial = [1]

    for i, (x, y) in enumerate(ranges):
        # Create range, handling both ascending and descending
        if x <= y:
            numbers = list(range(x, y + 1))
        else:
            numbers = list(range(x, y - 1, -1))

        if i % 2 == 0:  # Even indices: append right
            dial.extend(numbers)
        else:  # Odd indices: prepend left (reverse order)
            dial = numbers[::-1] + dial

    target_index = (dial.index(1) + 20252025) % len(dial)
    return dial[target_index]


def part_three(data: list[str]) -> int:
    """Efficiently find position in a virtual dial without materializing it.

    Instead of building the full dial, work with range tuples and calculate
    the target value mathematically. This avoids memory issues with large dials.

    Args:
        data: List where third element contains newline-separated ranges.

    Returns:
        The value at position 202520252025 % dial_size.
    """
    ranges = [tuple(map(int, line.split("-"))) for line in data[2].splitlines()]
    dial = [(1, 1)]

    # Build dial structure with range tuples
    for i, (x, y) in enumerate(ranges):
        if i % 2 == 0:  # Even: append right
            dial.append((x, y))
        else:  # Odd: prepend left (swap x and y)
            dial.insert(0, (y, x))

    # Rotate dial so (1, 1) is at the start
    index_of_one = dial.index((1, 1))
    dial = dial[index_of_one:] + dial[:index_of_one]

    # Calculate total size and target position
    dial_size = sum(abs(x - y) + 1 for x, y in dial)
    target_position = 202520252025 % dial_size

    # Walk through ranges to find the value at target position
    current_position = 0
    for x, y in dial:
        range_size = abs(x - y) + 1

        if current_position + range_size > target_position:
            # Target is within this range
            offset = target_position - current_position
            return x + offset if x <= y else x - offset

        current_position += range_size

    # Should never reach here with valid input
    raise ValueError("Target position not found in dial")


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 869
    print("Part 2:", part_two(data))  # 2461
    print("Part 3:", part_three(data))  # 416364
