#!/usr/bin/env python
"""
Advent of Code 2020 - Day 1: Report Repair

Problem Description:
- Part 1: Find two numbers in the expense report that sum to 2020, then multiply them together
- Part 2: Find three numbers in the expense report that sum to 2020, then multiply them together

The "expense report" is a list of numbers, one per line in the input file.

Example:
If the input contains [1721, 979, 366, 299, 675, 1456]:
- Part 1: 1721 + 299 = 2020, so answer is 1721 * 299 = 514579
- Part 2: 979 + 366 + 675 = 2020, so answer is 979 * 366 * 675 = 241861950

Time Complexity:
- Part 1: O(n) using hash set lookup
- Part 2: O(n²) using nested loops with hash set lookup

Space Complexity: O(n) for storing the number set
"""

from typing import List, Set


def read_puzzle_input() -> List[int]:
    with open("01.in", "r") as file:
        return list(map(int, file.read().splitlines()))


def part_one(data: List[int], target: int = 2020) -> int:
    """
    Find two numbers in the list that sum to the target value and return their product.

    Algorithm:
    1. Convert list to set for O(1) lookup
    2. For each number, calculate what its complement would need to be
    3. Check if the complement exists in the set
    4. Return the product of the two numbers

    Args:
        numbers: List of integers to search through
        target: Target sum value (default: 2020)

    Returns:
        Product of the two numbers that sum to target, or None if no such pair exists

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    number_set: Set[int] = set(data)

    for num in data:
        complement = target - num
        # Ensure we don't use the same number twice (unless it appears multiple times)
        if complement in number_set and (complement != num or data.count(num) > 1):
            return num * complement

    return -1


def part_two(data: List[int], target: int = 2020) -> int:
    """
    Find three numbers in the list that sum to the target value and return their product.

    Algorithm:
    1. Convert list to set for O(1) lookup
    2. For each pair of numbers (i, j), calculate what the third number would need to be
    3. Check if the third number exists in the set
    4. Ensure all three numbers are different instances
    5. Return the product of the three numbers

    Args:
        numbers: List of integers to search through
        target: Target sum value (default: 2020)

    Returns:
        Product of the three numbers that sum to target, or None if no such triplet exists

    Time Complexity: O(n²)
    Space Complexity: O(n)
    """

    number_set: Set[int] = set(data)

    for i, first_num in enumerate(data):
        for _, second_num in enumerate(data[i + 1 :], i + 1):  # Avoid duplicate pairs
            third_num = target - first_num - second_num

            # Check if third number exists and is different from the first two
            if (
                third_num in number_set
                and third_num != first_num
                and third_num != second_num
            ):
                return first_num * second_num * third_num

    return -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 928896
    print("Part 2:", part_two(data))  # 295668576
