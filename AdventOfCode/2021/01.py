#!/usr/bin/env python

from typing import List


def read_puzzle_input(filename: str = "01.in") -> List[int]:
    """
    Read the puzzle input file and return a list of integers.

    Args:
        filename: Name of the input file (default: "01.in")

    Returns:
        List of depth measurements as integers

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file contains non-integer values
    """

    try:
        with open(filename, "r") as file:
            return [int(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except ValueError as e:
        raise ValueError(f"Invalid integer in input file: {e}")


def part_one(data: list) -> int:
    """
    Count how many depth measurements are larger than the previous measurement.

    This is the solution for Part 1 of the puzzle.

    Args:
        measurements: List of depth measurements

    Returns:
        Number of measurements that are larger than the previous measurement

    Example:
        >>> count_depth_increases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
        7
    """

    if len(data) < 2:
        return 0

    # Count increases by comparing each measurement with the previous one
    # We start from index 1 since we need to compare with the previous element
    increases = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            increases += 1

    return increases


def part_two(data: list) -> int:
    """
    Count how many 3-measurement sliding window sums are larger than the previous window sum.

    This is the solution for Part 2 of the puzzle.

    OPTIMIZATION EXPLANATION:
    Instead of calculating actual window sums, we use a mathematical optimization:

    Window A: measurements[i-3] + measurements[i-2] + measurements[i-1]
    Window B: measurements[i-2] + measurements[i-1] + measurements[i]

    To check if Window B > Window A:
    (measurements[i-2] + measurements[i-1] + measurements[i]) > (measurements[i-3] + measurements[i-2] + measurements[i-1])

    The middle terms cancel out, leaving:
    measurements[i] > measurements[i-3]

    So we only need to compare the element entering the window with the element leaving it!

    Args:
        measurements: List of depth measurements

    Returns:
        Number of sliding window sums that are larger than the previous window sum

    Example:
        >>> count_sliding_window_increases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
        5
    """

    if len(data) < 4:
        return 0

    # We need at least 4 elements to compare two 3-element windows
    # Start from index 3 (4th element) since we're comparing with index 0 (1st element)
    increases = 0
    for i in range(3, len(data)):
        # Compare the element entering the new window with the element leaving the old window
        if data[i] > data[i - 3]:
            increases += 1

    return increases


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1233
    print("Part 2:", part_two(data))  # 1275
