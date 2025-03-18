#!/usr/bin/env python
"""
Advent of Code 2016 - Day 20: Firewall Rules

This script processes a list of blocked IP ranges and determines:
1. The first available (non-blocked) IP.
2. The total count of available (non-blocked) IPs within the given range.

The input file "20.in" should contain IP ranges in the format:
    start-end
For example:
    5-8
    0-2
    4-7
"""

from typing import List, Tuple


def read_puzzle_input() -> List[Tuple[int, int]]:
    """
    Reads the input file and parses it into a list of blocked IP ranges.

    Each line in the file contains a range in the format 'start-end'.
    This function converts them into a list of (start, end) integer tuples.

    Returns:
        List[Tuple[int, int]]: A list of blocked IP ranges.
    """

    with open("20.in", "r") as file:
        return [tuple(map(int, line.strip().split('-'))) for line in file]


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merges overlapping or adjacent IP ranges into a consolidated list.

    Given a list of (start, end) tuples, this function:
    - Sorts them by the starting value.
    - Merges overlapping or contiguous ranges.

    Args:
        ranges (List[Tuple[int, int]]): List of blocked IP ranges.

    Returns:
        List[Tuple[int, int]]: A new list of merged IP ranges.
    """

    merged = []  # Stores merged IP ranges
    for start, end in sorted(ranges):  # Sort the ranges by start value
        if not merged or merged[-1][1] < start - 1:
            # If there's no overlap, add a new range
            merged.append((start, end))
        else:
            # Merge overlapping or adjacent ranges
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged


def part_one(data: List[Tuple[int, int]]) -> int:
    """
    Finds the first available (non-blocked) IP.

    - Merges the input ranges.
    - Looks for the first gap in the blocked ranges.
    - If the first blocked range does not start at 0, return 0.
    - Otherwise, find the first IP that is not covered.

    Args:
        data (List[Tuple[int, int]]): List of blocked IP ranges.

    Returns:
        int: The first non-blocked IP address.
    """

    merged_ranges = merge_ranges(data)

    # If the first blocked range starts after 0, return 0
    if merged_ranges[0][0] > 0:
        return 0

    # Look for the first gap in the blocked ranges
    for i in range(len(merged_ranges) - 1):
        if merged_ranges[i][1] + 1 < merged_ranges[i + 1][0]:
            return merged_ranges[i][1] + 1  # First available IP found

    return -1  # Should not happen with valid input


def part_two(data: List[Tuple[int, int]]) -> int:
    """
    Counts the number of non-blocked IPs in the given range (0 to 4294967295).

    - Merges the input ranges.
    - Counts all unblocked IPs by finding gaps between merged ranges.

    Args:
        data (List[Tuple[int, int]]): List of blocked IP ranges.

    Returns:
        int: The total count of non-blocked IPs.
    """

    merged_ranges = merge_ranges(data)
    max_ip = 4294967295  # Maximum possible IP in the range
    allowed_count = 0    # Tracks count of non-blocked IPs
    prev_end = -1        # Tracks the end of the last processed range

    for start, end in merged_ranges:
        if start > prev_end + 1:
            # Count all IPs in the gap between the last blocked range and the
            # current one
            allowed_count += start - (prev_end + 1)
        prev_end = end  # Update the last processed end

    # Count remaining IPs beyond the last blocked range
    if prev_end < max_ip:
        allowed_count += max_ip - prev_end

    return allowed_count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 19449262
    print("Part 2:", part_two(data))  # 119
