#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return [int(char) for char in file.read().strip()]


def part_one(data: list) -> int:
    """
    Computes the sum of all digits in the list that match the next digit in
    the sequence. The list is treated as circular, meaning the last element
    is compared to the first.

    Args:
        data (list): A list of integers representing the sequence.

    Returns:
        int: The sum of all matching digits.
    """

    return sum(
        data[i] for i in range(len(data))
        if data[i] == data[(i + 1) % len(data)]
    )


def part_two(data: list) -> int:
    """
    Computes the sum of all digits in the list that match the digit halfway
    around the list. The list is assumed to have an even length, and each
    element at index `i` is compared to the element at `i + half`
    (where `half = len(data) // 2`).

    Args:
        data (list): A list of integers representing the sequence.

    Returns:
        int: The sum of all matching digits, multiplied by 2 to account for
             both halves.
    """

    half = len(data) // 2
    return 2 * sum(data[i] for i in range(half) if data[i] == data[i + half])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1049
    print("Part 2:", part_two(data))  # 1508
