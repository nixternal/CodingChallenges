#!/usr/bin/env python


def read_puzzle_input() -> list:
    """Read the puzzle input and return a list of lines."""
    with open("02.in", "r") as file:
        return file.read().splitlines()


def is_invalid_id(product_id: int, allow_repeated_patterns: bool) -> bool:
    """
    Determine whether a product ID is invalid based on repeated digit patterns.

    Parameters
    ----------
    product_id : int
        The product ID number to evaluate.
    allow_repeated_patterns : bool
        - False (Part 1 rules): ID is invalid only if it is composed of ONE sequence
          repeated EXACTLY twice (e.g., 1212, 5050).
        - True (Part 2 rules): ID is invalid if it is composed of ANY sequence repeated
          TWO OR MORE times (e.g., 11, 12121212, 123123123).

    Returns
    -------
    bool
        True if the ID is invalid, False otherwise.
    """
    digits = str(product_id)
    length = len(digits)

    # IDs must have enough digits to repeat at least once (minimum "AA")
    if length < 2:
        return False

    if not allow_repeated_patterns:
        # Part 1: only detect pattern A + A (two equal halves)
        if length % 2 != 0:
            return False  # odd-length IDs cannot split evenly
        half = length // 2
        return digits[:half] == digits[half:]

    # Part 2: detect ANY repeated pattern (A x N, where N >= 2)
    # We test every possible chunk size that evenly divides the length
    # If repeating the chunk reconstructs the full ID, it's invalid
    for chunk_size in range(1, length // 2 + 1):
        if length % chunk_size == 0:
            chunk = digits[:chunk_size]
            repetitions = length // chunk_size
            if chunk * repetitions == digits:
                return True

    return False


def part_one(data: list) -> int:
    total = 0
    id_ranges = data[0].strip().split(",")

    for id_range in id_ranges:
        if not id_range:
            continue
        start, end = map(int, id_range.split("-"))

        for product_id in range(start, end + 1):
            if is_invalid_id(product_id, allow_repeated_patterns=False):
                total += product_id

    return total


def part_two(data: list) -> int:
    total = 0
    id_ranges = data[0].strip().split(",")

    for id_range in id_ranges:
        if not id_range:
            continue
        start, end = map(int, id_range.split("-"))

        for product_id in range(start, end + 1):
            if is_invalid_id(product_id, allow_repeated_patterns=True):
                total += product_id

    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 40055209690
    print("Part 2:", part_two(data))  # 50857215650
