#!/usr/bin/env python
"""
Advent of Code Day 5: Binary Boarding
Decodes binary space partitioning boarding passes to find seat IDs.
"""


def read_puzzle_input() -> list[str]:
    """Read boarding passes from input file."""
    with open("05.in") as file:
        return file.read().splitlines()


def get_seat_id(boarding_pass: str) -> int:
    """
    Convert boarding pass to seat ID using binary encoding.

    F/L = 0, B/R = 1 in binary representation.
    First 7 chars encode row (0-127), last 3 encode column (0-7).
    Seat ID = row * 8 + col

    Args:
        boarding_pass: 10-character string like 'FBFBBFFRLR'

    Returns:
        Unique seat ID integer
    """
    # Translation table is more efficient than chained replace() calls
    translation = str.maketrans("FBLR", "0101")
    return int(boarding_pass.translate(translation), 2)


def part_one(data: list[str]) -> int:
    """Find the highest seat ID."""
    return max(get_seat_id(bp) for bp in data)


def part_two(data: list[str]) -> int:
    """
    Find your seat ID - the missing ID where seats ±1 exist.

    Returns the gap in the sorted seat ID sequence.
    """
    seat_ids = sorted(get_seat_id(bp) for bp in data)

    # Find the gap where current - previous = 2
    for prev, curr in zip(seat_ids, seat_ids[1:]):
        if curr - prev == 2:
            return prev + 1

    return -2  # Not found


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 987
    print("Part 2:", part_two(data))  # 603
