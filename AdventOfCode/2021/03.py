#!/usr/bin/env python
"""
Advent of Code 2021 - Day 3: Binary Diagnostic

This solution analyzes binary diagnostic data from a submarine to calculate
power consumption and life support ratings.

Part 1: Power Consumption
- Gamma rate: most common bit in each position across all binary numbers
- Epsilon rate: least common bit in each position across all binary numbers
- Power consumption = gamma rate × epsilon rate

Part 2: Life Support Rating
- Oxygen generator rating: progressively filter numbers by most common bit per position
- CO2 scrubber rating: progressively filter numbers by least common bit per position
- Life support rating = oxygen generator rating × CO2 scrubber rating
"""


def read_puzzle_input() -> list:
    """Read binary diagnostic data from input file.

    Returns:
        list: List of binary number strings (e.g., ['10110', '10111', ...])
    """

    with open("03.in", "r") as file:
        return file.read().splitlines()


def calculate_gamma_rate(data: list) -> int:
    """Calculate gamma rate - most common bit in each position.

    For each bit position, count occurrences of '1' across all numbers.
    If '1' appears more than half the time, that position gets '1' in gamma rate.

    Args:
        data: List of binary number strings

    Returns:
        int: Gamma rate as decimal integer
    """

    gamma_rate = []
    for i in range(0, len(data[0])):
        sum = 0
        for j in range(0, len(data)):
            sum += int(data[j][i])
        if sum > len(data) // 2:
            gamma_rate.append("1")
        else:
            gamma_rate.append("0")
    return int("".join(gamma_rate), 2)


def calculate_epsilon_rate(data: list) -> int:
    """Calculate epsilon rate - least common bit in each position.

    For each bit position, count occurrences of '1' across all numbers.
    If '1' appears less than or equal to half the time, that position gets '1' in epsilon rate.
    (This is the inverse of the gamma rate)

    Args:
        data: List of binary number strings

    Returns:
        int: Epsilon rate as decimal integer
    """

    epsilon_rate = []
    for i in range(0, len(data[0])):
        sum = 0
        for j in range(0, len(data)):
            sum += int(data[j][i])
        if sum > len(data) // 2:
            epsilon_rate.append("0")
        else:
            epsilon_rate.append("1")
    return int("".join(epsilon_rate), 2)


def find_oxygen_generator_rating(data: list) -> int:
    """Find oxygen generator rating using bit criteria filtering.

    Algorithm:
    1. Start with all binary numbers as candidates
    2. For each bit position (left to right):
       - Count '1' and '0' bits at that position among remaining candidates
       - Keep only numbers with the MOST COMMON bit at that position
       - If tied, keep numbers with '1'
    3. Continue until only one number remains

    Args:
        data: List of binary number strings

    Returns:
        int: Oxygen generator rating as decimal integer
    """

    candidates = data[:]
    bit_position = 0

    while len(candidates) > 1:
        # Count 1s and 0s at current bit position
        ones = sum(1 for num in candidates if num[bit_position] == "1")
        zeros = len(candidates) - ones

        # Keep numbers with most common bit (1 wins ties)
        if ones >= zeros:
            keep_bit = "1"
        else:
            keep_bit = "0"

        candidates = [num for num in candidates if num[bit_position] == keep_bit]
        bit_position += 1

    return int(candidates[0], 2)


def find_co2_scrubber_rating(data: list) -> int:
    """Find CO2 scrubber rating using bit criteria filtering.

    Algorithm:
    1. Start with all binary numbers as candidates
    2. For each bit position (left to right):
       - Count '1' and '0' bits at that position among remaining candidates
       - Keep only numbers with the LEAST COMMON bit at that position
       - If tied, keep numbers with '0'
    3. Continue until only one number remains

    Args:
        data: List of binary number strings

    Returns:
        int: CO2 scrubber rating as decimal integer
    """

    candidates = data[:]
    bit_position = 0

    while len(candidates) > 1:
        # Count 1s and 0s at current bit position
        ones = sum(1 for num in candidates if num[bit_position] == "1")
        zeros = len(candidates) - ones

        # Keep numbers with least common bit (0 wins ties)
        if zeros <= ones:
            keep_bit = "0"
        else:
            keep_bit = "1"

        candidates = [num for num in candidates if num[bit_position] == keep_bit]
        bit_position += 1

    return int(candidates[0], 2)


def part_one(data: list) -> int:
    """Solve part 1: Calculate power consumption.

    Power consumption = gamma rate × epsilon rate

    Args:
        data: List of binary number strings

    Returns:
        int: Power consumption value
    """

    return calculate_epsilon_rate(data) * calculate_gamma_rate(data)


def part_two(data: list) -> int:
    """Solve part 2: Calculate life support rating.

    Life support rating = oxygen generator rating × CO2 scrubber rating

    Args:
        data: List of binary number strings

    Returns:
        int: Life support rating value
    """

    oxygen_rating = find_oxygen_generator_rating(data)
    co2_rating = find_co2_scrubber_rating(data)
    return oxygen_rating * co2_rating


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3901196
    print("Part 2:", part_two(data))  # 4412188
