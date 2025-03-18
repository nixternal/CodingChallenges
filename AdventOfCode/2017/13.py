#!/usr/bin/env python

"""
Advent of Code 2017 - Day 13: Packet Scanners
https://adventofcode.com/2017/day/13

Problem Summary:
- You need to traverse a firewall with multiple layers
- Each layer has a scanner that moves up and down with a specific range
- Part 1: Calculate severity if you start immediately
- Part 2: Find the minimum delay needed to pass through without getting caught

The firewall is represented as a dictionary where:
- Keys are layer depths (0, 1, 2, etc.)
- Values are the range of that scanner (how far it moves up and down)

Example input:
0: 3
1: 2
4: 4
6: 4

This means:
- Layer 0 has a scanner with range 3
- Layer 1 has a scanner with range 2
- Layer 4 has a scanner with range 4
- Layer 6 has a scanner with range 4
"""


def read_puzzle_input() -> dict:
    with open("13.in", "r") as file:
        data = file.read().splitlines()

    firewall = {}
    for line in data:
        depth, range_str = line.split(': ')
        firewall[int(depth)] = int(range_str)
    return firewall


def scanner_position(time, range_size):
    """
    Calculate the position of a scanner at a given time.

    The scanner moves up and down in a cycle. For example, with range 4:
    Time 0: position 0
    Time 1: position 1
    Time 2: position 2
    Time 3: position 3
    Time 4: position 2
    Time 5: position 1
    Time 6: position 0
    Time 7: position 1
    ... and so on

    Args:
        time (int): The current time step
        range_size (int): The range of the scanner's movement

    Returns:
        int: The position of the scanner (0 to range_size - 1)
    """

    # Calculate cycle length (going up and down)
    cycle = 2 * (range_size - 1)
    if cycle == 0:
        return 0

    # Get position within the cycle
    time = time % cycle

    # If in first half of cycle, scanner is moving down
    if time < range_size:
        return time
    # If in second half, scanner is moving up
    return cycle - time


def calculate_severity(firewall, delay=0):
    """
    Calculate the severity of the trip through the firewall.

    Severity is calculated as the product of depth and range for each layer
    where you get caught.

    Args:
        firewall (dict): Dictionary mapping depths to ranges
        delay (int): Number of picoseconds to wait before starting

    Returns:
        int: Total severity of the trip
    """

    severity = 0

    # Check each layer
    for depth, range_size in firewall.items():
        # Time when we reach this layer = depth + delay
        time = depth + delay
        # If scanner is at position 0, we're caught
        if scanner_position(time, range_size) == 0:
            severity += depth * range_size

    return severity


def find_safe_delay(firewall):
    """
    Find the minimum delay needed to pass through the firewall without
    getting caught.

    A packet is caught if it arrives at a layer at the same time the scanner
    is at position 0 in that layer.

    Args:
        firewall (dict): Dictionary mapping depths to ranges

    Returns:
        int: Minimum delay needed to pass safely
    """

    delay = 0
    while True:
        # Check if we can pass safely with this delay
        caught = False
        for depth, range_size in firewall.items():
            time = depth + delay
            if scanner_position(time, range_size) == 0:
                caught = True
                break

        if not caught:
            return delay
        delay += 1


def part_one(data: dict) -> int:
    """
    Solve Part 1: Calculate the severity if starting immediately.

    Args:
        input_text (str): Raw input text

    Returns:
        int: Total severity of the trip
    """

    return calculate_severity(data)


def part_two(data: dict):
    """
    Solve Part 2: Find minimum delay needed to pass safely.

    Args:
        input_text (str): Raw input text

    Returns:
        int: Minimum delay needed
    """

    return find_safe_delay(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1504
    print("Part 2:", part_two(data))  # 3823370
