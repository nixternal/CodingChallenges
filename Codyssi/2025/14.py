#!/usr/bin/env python3
"""
Item Selection Optimization Problem

This program solves an optimization problem where items have three attributes:
1. Quality - how good the item is
2. Cost - how expensive the item is
3. Unique Materials - how many unique materials the item contains

The program has three parts:
1. Part 1: Select the top 5 items by quality (then by cost if there's a tie)
   and calculate the total unique materials.
2. Part 2: Find the combination of items that maximizes (quality ×
   unique_materials) while keeping the total cost under 30.
3. Part 3: Same as part 2, but with a cost limit of 300.
"""


def read_puzzle_input() -> list[tuple[int, int, int]]:
    """
    Read the puzzle input from the file and parse the input data into a list
    of items.

    Args:
        data: List of strings from the input file

    Returns:
        List of tuples (quality, cost, unique_materials)
    """

    items = []
    with open("14.in", "r") as file:
        for line in file.readlines():
            parts = line.split('|')
            # Extract the attributes from the parts
            attributes = parts[1].split(':')
            quality = int(attributes[1].strip().split(',')[0])
            cost = int(attributes[2].strip().split(',')[0])
            unique_materials = int(attributes[3].strip())
            items.append((quality, cost, unique_materials))
    return items


def calculate_total_unique_materials(items: list[tuple[int, int, int]]) -> int:
    """
    Calculate the total unique materials for the top 5 items.

    Args:
        items: List of (quality, cost, unique_materials) tuples

    Returns:
        Total unique materials of the top 5 items
    """

    # Sort items by quality (descending), then by cost (descending)
    top_5 = sorted(items, key=lambda x: (-x[0], -x[1]))[:5]

    # Sum the unique materials of the top 5 items
    return sum(item[2] for item in top_5)


def find_optimal_combination(
        items: list[tuple[int, int, int]],
        max_cost: int
        ) -> int:
    """
    Find the combination of items that maximizes (quality × unique_materials)
    while keeping the total cost under max_cost.

    Uses dynamic programming where:
    - dp[c] represents the best (quality, unique_materials) pair achievable
      with a cost of exactly c.

    Args:
        items: List of (quality, cost, unique_materials) tuples
        max_cost: Maximum cost allowed

    Returns:
        The product of total quality and total unique materials
    """

    # Initialize dp array: (quality, unique_materials)
    dp = [(0, 0)] * (max_cost + 1)

    for quality, cost, unique_materials in items:
        # Iterate backwards to prevent using an item multiple times
        for c in range(max_cost, cost - 1, -1):
            # Calculate new quality and materials if we include this item
            prev_quality, prev_materials = dp[c - cost]
            new_quality = prev_quality + quality
            new_materials = prev_materials + unique_materials

            # Update if better (either higher quality, or same quality but
            # fewer materials)
            current_quality, current_materials = dp[c]
            if (new_quality > current_quality or
                (new_quality == current_quality and
                    new_materials < current_materials)):
                dp[c] = (new_quality, new_materials)

    # Find the combination with the highest product of quality and materials
    best_product = 0
    for quality, materials in dp:
        product = quality * materials
        if product > best_product:
            best_product = product

    return best_product


def part_one(data: list) -> int:
    return calculate_total_unique_materials(data)


def part_two(data: list) -> int:
    return find_optimal_combination(data, 30)


def part_three(data: list) -> int:
    return find_optimal_combination(data, 300)


if __name__ == "__main__":
    """Main function to run all parts of the puzzle."""
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 55
    print("Part 2:", part_two(data))    # 25650
    print("Part 3:", part_three(data))  # 425459
