#!/usr/bin/env python

import math


def read_puzzle_input() -> list:
    with open("07.in", "r") as file:
        return [int(x) for x in file.read().split(',')]


def part_one(data: list) -> int:
    """Calculates fuel using the Median (Linear Cost)."""
    data.sort()
    # The middle element is our target
    median = data[len(data) // 2]
    # Sum of absolute differences
    return sum(abs(crab - median) for crab in data)


def part_two(data: list) -> int:
    """Calculates fuel using the Mean (Quadratic Cost)."""
    avg = sum(data) / len(data)

    # We check both rounding directions to be safe
    targets = [math.floor(avg), math.ceil(avg)]

    results = []
    for target in targets:
        fuel = 0
        for crab in data:
            n = abs(crab - target)
            # Triangular number formula: n(n+1)/2
            fuel += (n * (n + 1)) // 2
        results.append(fuel)

    return min(results)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 352254
    print("Part 2:", part_two(data))  # 99053143
