#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("03.in", "r") as file:
        return file.read().splitlines()


def parse_digits(line: str) -> list[int]:
    """Convert a string of digits into a list of integers."""
    return [int(char) for char in line.strip()]


def find_max_two_digit_number(digits: list[int]) -> int:
    """
    Find the maximum two-digit number that can be formed from any two digits.

    Args:
        digits: List of single-digit integers

    Returns:
        Maximum value formed by combining any two digits (first * 10 + second)
    """
    if len(digits) < 2:
        return 0

    # Find the two largest distinct positions
    # We need to maintain order: first digit must come before second
    max_value = 0
    for i in range(len(digits) - 1):
        for j in range(i + 1, len(digits)):
            value = digits[i] * 10 + digits[j]
            max_value = max(max_value, value)

    return max_value


def extract_largest_subsequence(digits: list[int], length: int = 12) -> int:
    """
    Extract the largest subsequence of given length maintaining original order.

    Uses a greedy algorithm with a monotonic stack approach:
    - Keep digits in decreasing order when possible
    - Only pop smaller digits if we have enough remaining digits

    Args:
        digits: List of single-digit integers
        length: Target length of subsequence

    Returns:
        Integer formed by concatenating the selected digits
    """
    selected = []

    for idx, digit in enumerate(digits):
        remaining_digits = len(digits) - idx

        # Pop smaller digits from the end if:
        # 1. Current digit is larger than the last selected digit
        # 2. We still have enough remaining digits to reach target length
        while (
            selected
            and selected[-1] < digit
            and len(selected) - 1 + remaining_digits >= length
        ):
            selected.pop()

        # Add current digit if we haven't reached target length
        if len(selected) < length:
            selected.append(digit)

    return int("".join(map(str, selected)))


def part_one(data: list) -> int:
    return sum(find_max_two_digit_number(parse_digits(line)) for line in data)


def part_two(data: list) -> int:
    return sum(extract_largest_subsequence(parse_digits(line)) for line in data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 16993
    print("Part 2:", part_two(data))  # 168617068915447
