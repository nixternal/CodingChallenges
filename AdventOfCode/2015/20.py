#!/usr/bin/env python
"""
Advent of Code Solution: Infinite Houses Problem

This script solves the Infinite Houses problem where each house receives
packages delivered by elves. Each elf delivers packages to houses according
to specific rules.

The solutions are split into two parts:
1. Each elf delivers packages to all houses that are multiples of their number.
2. Each elf delivers packages to at most 50 houses.

The algorithms used are variations of the "Sum of Divisors" problem, optimized
using a sieve-like approach for efficient computation.
"""


def part_one() -> int:
    """
    Solves Part 1 of the problem:
    - Each elf delivers 10 times their number of packages.
    - Elves deliver to all houses that are multiples of their number.

    Algorithm:
    - Sieve of Divisors: A sieve-like approach is used to calculate the sum of
      divisors for all houses up to a given limit. The sum of divisors
      represents the houses that each elf delivers to.

    Returns:
        int: The lowest house number where the total packages delivered meet
             or exceed the target.
    """

    target = 33100000  # Target number of packages
    limit = 1000000  # Upper limit for house numbers to check (brute-force)
    packages = [0] * (limit + 1)  # Array to store package count for each house

    # Sieve of Divisors: calculate the sum of divisors for each house
    for p in range(1, limit + 1):
        for k in range(p, limit + 1, p):
            packages[k] += p  # Add elf's number to all houses they deliver to

    # Find the first house where the total packages meet or exceed the target
    for n in range(1, limit + 1):
        # Multiply by 10 to account for package rules
        if 10 * packages[n] >= target:
            return n

    # If no house meets the target within the limit return -1. If this happens
    # increase the limit until it doesn't
    return -1


def part_two() -> int:
    """
    Solves Part 2 of the problem:
    - Each elf delivers 11 times their number of packages.
    - Each elf delivers to at most 50 houses.

    Algorithm:
    - Modified Sieve of Divisors: A variation of the sieve is used where each elf only
      delivers to the first 50 houses they are responsible for. This imposes a
      delivery limit.

    Returns:
        int: The lowest house number where the total packages delivered meet
             or exceed the target.
    """

    target = 33100000  # Target number of packages
    limit = 1000000  # Upper limit for house numbers to check (brute-force)
    packages = [0] * (limit + 1)  # Array to store package count for each house

    # Modified Sieve of Divisors: limit each elf to 50 deliveries
    for p in range(1, limit + 1):
        for k in range(1, 51):  # Elves deliver to at most 50 houses
            house = p * k
            if house > limit:
                break  # Stop if the house number exceeds the limit
            packages[house] += 11 * p  # Add packages to the house

    # Find the first house where the total packages meet or exceed the target
    for n in range(1, limit + 1):
        if packages[n] >= target:
            return n

    # If no house meets the target within the limit return -1. If this happens
    # increase the limit until it doesn't
    return -1


if __name__ == "__main__":
    print("Part 1:", part_one())  # 776160
    print("Part 2:", part_two())  # 786240
