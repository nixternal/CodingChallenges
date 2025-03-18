#!/usr/bin/env python

"""
Advent of Code 2016, Day 19: An Elephant Named Joseph

This script solves the Day 19 puzzle from Advent of Code 2016. The puzzle
involves a group of elves sitting in a circle and playing a game of stealing
presents from each other. The problem is divided into two parts:

1. Part One: Elves steal presents from the immediate next elf in the circle.
2. Part Two: Elves steal presents from the elf directly across the circle.

The solutions use mathematical insights and efficient algorithms to determine
the winning elf's number for each part.
"""


def part_one(num_elves: int) -> int:
    """
    Solves Part One of the puzzle using the Josephus problem algorithm.

    Problem Description:
    - There are `num_elves` elves sitting in a circle.
    - Each elf steals presents from the immediate next elf in the circle.
    - The process continues until only one elf remains with all the presents.
    - The goal is to determine the winning elf's number.

    Algorithm:
    - This problem is a classic example of the Josephus problem with step
      size `k = 2`.
    - The winning position for `n` people and `k = 2` is given by:
        J(n) = 2 ⋅ (n - 2^[log^2(n)]) + 1
    - The algorithm works as follows:
      1. Find the largest power of 2 less than or equal to `num_elves`.
      2. Subtract this value from `num_elves` to get the offset.
      3. Multiply the offset by 2 and add 1 to get the winning position.

    Args:
        num_elves (int): The number of elves in the circle.

    Returns:
        int: The winning elf's number.
    """

    i = 1

    # Find the largest power of 2 less than or equal to num_elves
    while i * 2 <= num_elves:
        i *= 2

    # Calculate the winning position using the Josephus formula
    return 2 * (num_elves - i) + 1


def part_two(num_elves: int) -> int:
    """
    Solves Part Two of the puzzle using a mathematical approach.

    Problem Description:
    - There are `num_elves` elves sitting in a circle.
    - Each elf steals presents from the elf directly across the circle.
    - The process continues until only one elf remains with all the presents.
    - The goal is to determine the winning elf's number.

    Algorithm:
    - This problem is more complex than Part One and does not directly follow
      the Josephus problem.
    - The solution involves finding the largest power of 3 less than or equal
      to `num_elves` and using the offset to determine the winner.
    - The algorithm works as follows:
      1. Find the largest power of 3 less than or equal to `num_elves`.
      2. If `num_elves` is equal to this power of 3, the winner is `num_elves`.
      3. Otherwise, calculate the offset (`num_elves - largest_power_of_3`).
         - If the offset is less than or equal to the largest power of 3, the
           winner is the offset.
         - Otherwise, the winner is `2 * offset`.

    Args:
        num_elves (int): The number of elves in the circle.

    Returns:
        int: The winning elf's number.
    """

    # Find the largest power of 3 less than or equal to num_elves
    i = 1
    while i * 3 <= num_elves:
        i *= 3

    # Determine the winner based on the offset
    if num_elves == i:
        # If num_elves is a power of 3, the winner is num_elves
        return num_elves
    elif num_elves - i <= i:
        # If the offset is less than or equal to the largest power of 3,
        # the winner is the offset
        return num_elves - i
    else:
        # Otherwise, the winner is twice the offset
        return 2 * (num_elves - i)


if __name__ == '__main__':
    num_elves = 3005290
    print("Part 1:", part_one(num_elves))  # 1816277
    print("Part 2:", part_two(num_elves))  # 1410967
