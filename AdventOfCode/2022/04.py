#!/usr/bin/env python
"""
Advent of Code - Day 4: Camp Cleanup

Analyzes pairs of section assignment ranges to find overlaps.
Part 1: Count pairs where one range fully contains the other.
Part 2: Count pairs where ranges overlap at all.
"""


def read_puzzle_input() -> list:
    """Read and parse the puzzle input file."""
    with open("04.in", "r") as file:
        return file.read().splitlines()


def parse_range(range_str: str) -> tuple[int, int]:
    """Parse a range string like '2-8' into a tuple of (start, end)."""
    start, end = map(int, range_str.split("-"))
    return start, end


def fully_contains(elf1: tuple[int, int], elf2: tuple[int, int]) -> bool:
    """Check if either range fully contains the other."""
    return (elf1[0] <= elf2[0] and elf1[1] >= elf2[1]) or (
        elf2[0] <= elf1[0] and elf2[1] >= elf1[1]
    )


def overlaps(elf1: tuple[int, int], elf2: tuple[int, int]) -> bool:
    """Check if two ranges overlap at all."""
    return elf1[0] <= elf2[1] and elf2[0] <= elf1[1]


def part_one(data: list) -> int:
    """Count pairs where one range fully contains the other."""
    count = 0
    for line in data:
        elf1, elf2 = map(parse_range, line.split(","))
        if fully_contains(elf1, elf2):
            count += 1
    return count


def part_two(data: list) -> int:
    """Count pairs where ranges overlap at all."""
    count = 0
    for line in data:
        elf1, elf2 = map(parse_range, line.split(","))
        if overlaps(elf1, elf2):
            count += 1
    return count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 534
    print("Part 2:", part_two(data))  # 841
