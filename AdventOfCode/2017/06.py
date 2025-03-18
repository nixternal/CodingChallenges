#!/usr/bin/env python

"""
Advent of Code 2017 - Day 6: Memory Reallocation

This script solves both parts of the puzzle by redistributing blocks across
memory banks until a repeated configuration is found (Part 1) and then
determining the cycle length of that repeated configuration (Part 2).

Part 1:
- Count how many redistribution cycles occur before a configuration repeats.

Part 2:
- Determine the size of the infinite loop that starts when a configuration is
  seen again.
"""


def part_one(data: list) -> int:
    """
    Finds the number of redistribution cycles before a memory bank
    configuration repeats.

    Parameters:
    data (list): A list of integers representing memory banks.

    Returns:
    int: The number of redistribution cycles before a configuration repeats.
    """

    seen_configs = set()                    # Set to store seen configurations
    banks = data[:]                         # Copy to avoid modifying original
    steps = 0                               # Count redistribution cycles

    while tuple(banks) not in seen_configs:
        seen_configs.add(tuple(banks))      # Store the current configuration
        steps += 1                          # Increment cycle counter

        # Find the index of the first max value
        max_blocks = max(banks)
        idx = banks.index(max_blocks)       # Get first occurrence of max

        banks[idx] = 0                      # Clear the max bank

        # Redistribute blocks cyclically
        for _ in range(max_blocks):
            idx = (idx + 1) % len(banks)    # Move to next index circularly
            banks[idx] += 1
    return steps                            # Return redistribution cycles


def part_two(data: list) -> int:
    """
    Finds the cycle length of the infinite loop in memory bank redistribution.

    Parameters:
    data (list): A list of integers representing memory banks.

    Returns:
    int: The length of the loop that forms when a configuration repeats.
    """

    seen_configs = {}                       # Dictionary to store seen configs
    banks = data[:]                         # Copy to avoid modifying original
    steps = 0                               # Count total redistribution cycles

    while tuple(banks) not in seen_configs:
        seen_configs[tuple(banks)] = steps  # Store config w/ its step count
        steps += 1                          # Increment step count

        # Find the index of the first max value
        max_blocks = max(banks)
        idx = banks.index(max_blocks)       # Get first occurrence of max

        banks[idx] = 0                      # Clear the max bank

        # Redistribute blocks cyclically
        for _ in range(max_blocks):
            idx = (idx + 1) % len(banks)    # Move to next index circularly
            banks[idx] += 1

    # Loop Size = Current Step Count - First Occurrence Step Count
    return steps - seen_configs[tuple(banks)]


if __name__ == "__main__":
    data = [2, 8, 8, 5, 4, 2, 3, 1, 5, 5, 1, 2, 15, 13, 5, 14]
    print("Part 1:", part_one(data))  # 3156
    print("Part 2:", part_two(data))  # 1610
