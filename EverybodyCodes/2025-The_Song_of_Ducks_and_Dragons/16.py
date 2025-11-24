#!/usr/bin/env python
"""
Puzzle Solution: Block Placement and Spell Calculations

This solution handles three parts:
1. Count blocks placed in columns based on spell divisibility
2. Find optimal spell pattern and calculate product
3. Binary search for maximum length within block limit
"""


def read_puzzle_input() -> list:
    """Read puzzle input file and split into sections."""
    with open("16.in", "r") as file:
        return file.read().split("\n\n")


def find_optimal_spell(wall_heights):
    """
    Find the optimal spell pattern by greedily selecting intervals.

    The algorithm finds all divisors that can fully cover positions with
    remaining height, reducing height by 1 at each covered position.

    Args:
        wall_heights: List of integers representing wall heights

    Returns:
        List of divisors that form the optimal spell pattern
    """
    wall_heights = wall_heights[:]  # Work on a copy
    num_positions = len(wall_heights)
    spell_pattern = []

    # Try each possible divisor from 1 to num_positions
    for divisor in range(1, num_positions + 1):
        # Check if all positions at this interval have remaining height
        positions = range(divisor - 1, num_positions, divisor)

        if all(wall_heights[i] > 0 for i in positions):
            spell_pattern.append(divisor)
            # Reduce height at each position covered by this divisor
            for i in positions:
                wall_heights[i] -= 1

    return spell_pattern


def calculate_total_blocks(max_length, spell_pattern):
    """
    Calculate total blocks placed up to max_length using the spell pattern.

    For each divisor in the spell, blocks are placed at positions that are
    multiples of that divisor.

    Args:
        max_length: Maximum column/position to consider
        spell_pattern: List of divisors in the spell

    Returns:
        Total number of blocks placed
    """
    return sum(max_length // divisor for divisor in spell_pattern)


def part_one(data: list) -> int:
    """
    Part 1: Count total blocks in 90 columns using given spell pattern.

    For each column, count how many spell divisors evenly divide into
    that column number (i.e., blocks placed in that column).
    """
    spell_pattern = list(map(int, data[0].strip().split(",")))
    num_columns = 90
    total = 0

    for column in range(1, num_columns + 1):
        # Count divisors in spell that divide evenly into this column
        total += sum(column % divisor == 0 for divisor in spell_pattern)

    return total


def part_two(data: list) -> int:
    """
    Part 2: Find optimal spell pattern and return product of all divisors.

    Uses greedy algorithm to find spell pattern, then multiplies all
    divisors together.
    """
    wall_heights = list(map(int, data[1].strip().split(",")))
    spell_pattern = find_optimal_spell(wall_heights)

    # Calculate product of all divisors in the spell
    product = 1
    for divisor in spell_pattern:
        product *= divisor

    return product


def part_three(data: list) -> int:
    """
    Part 3: Binary search for maximum length with block limit.

    Find the largest column number where total blocks doesn't exceed
    202,520,252,025,000.
    """
    wall_heights = list(map(int, data[2].strip().split(",")))
    spell_pattern = find_optimal_spell(wall_heights)

    # Binary search bounds
    low = 1
    high = 10 ** 17
    block_limit = 202520252025000

    # Binary search for maximum length
    while low < high:
        mid = (low + high + 1) // 2

        if calculate_total_blocks(mid, spell_pattern) <= block_limit:
            low = mid  # Can go higher
        else:
            high = mid - 1  # Too many blocks, go lower

    return low


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  #  202
    print("Part 2:", part_two(data))  #  124480032768
    print("Part 3:", part_three(data))  # 95079364681119
