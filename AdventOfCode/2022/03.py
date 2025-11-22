#!/usr/bin/env python
"""
Advent of Code - Day 3: Rucksack Reorganization

This script calculates priority scores for items found in rucksacks.
- Part 1: Finds common items between two compartments of each rucksack
- Part 2: Finds common items (badges) across groups of three rucksacks

Priority scoring:
- Lowercase a-z: 1-26
- Uppercase A-Z: 27-52
"""


def read_puzzle_input() -> list[str]:
    """Read rucksack data from input file."""
    with open("03.in", "r") as file:
        return file.read().splitlines()


def get_priority(item: str) -> int:
    """
    Calculate priority value for a given item character.

    Args:
        item: Single character representing an item (a-z or A-Z)

    Returns:
        Priority score (1-52)
    """
    if item.isupper():
        return ord(item) - ord("A") + 27
    return ord(item) - ord("a") + 1


def part_one(data: list[str]) -> int:
    """
    Find the sum of priorities for items that appear in both compartments
    of each rucksack.

    Each rucksack is divided into two equal compartments (first half and second half).

    Args:
        data: List of rucksack contents (strings)

    Returns:
        Sum of all common item priorities
    """
    total_priority = 0

    for rucksack in data:
        # Split rucksack into two equal compartments
        mid = len(rucksack) // 2
        comp1 = set(rucksack[:mid])
        comp2 = set(rucksack[mid:])

        # Find common item(s) and add their priorities
        common_items = comp1 & comp2  # set.intersection()
        total_priority += sum(get_priority(item) for item in common_items)

    return total_priority


def part_two(data: list[str]) -> int:
    """
    Find the sum of priorities for badge items that appear in groups
    of three consecutive rucksacks.

    Args:
        data: List of rucksack contents (strings)

    Returns:
        Sum of all badge item priorities
    """
    total_priority = 0

    # Process rucksacks in groups of three
    for i in range(0, len(data), 3):
        sack1 = set(data[i])
        sack2 = set(data[i + 1])
        sack3 = set(data[i + 2])

        # Find common item(s) across all three rucksacks
        common_items = sack1 & sack2 & sack3  # set.intersection()
        total_priority += sum(get_priority(item) for item in common_items)

    return total_priority


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 7817
    print("Part 2:", part_two(data))  # 2444
