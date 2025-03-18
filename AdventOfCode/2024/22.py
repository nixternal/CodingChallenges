#!/usr/bin/env python

"""
Puzzle Solution Script

This script provides solutions for two parts of a puzzle.
It processes numeric data from an input file, applies a transformation
function, and computes results based on specific patterns.

Functions:
    read_puzzle_input(): Reads the puzzle input from a file.
    step(num): Transforms a number using bitwise operations.
    part_one(data): Computes the total value after applying the transformation
                    function multiple times.
    part_two(data): Identifies unique sequences of differences in digit
                    transformations and returns the maximum value.
"""


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named "22.in" and returns it as a list
    of strings.

    Returns:
        list: A list of strings representing the input data.
    """

    with open("22.in", "r") as file:
        return file.read().splitlines()


def step(num: int):
    """
    Applies a series of bitwise operations to transform the input number.

    Args:
        num (int): The input number to transform.

    Returns:
        int: The transformed number.
    """

    num = num ^ ((num * 64)) % 16777216
    num = num ^ ((num // 32)) % 16777216
    num = num ^ ((num * 2048)) % 16777216
    return num


def part_one(data: list) -> int:
    """
    Solves part one of the puzzle by repeatedly transforming numbers
    and summing their final values.

    Args:
        data (list): A list of strings, each representing a number.

    Returns:
        int: The sum of the transformed numbers.
    """

    total = 0
    for line in data:
        num = int(line)
        for _ in range(2000):  # Apply step function 2000x to each number
            num = step(num)
        total += num  # Add the final value to the total
    return total


def part_two(data: list) -> int:
    """
    Solves part two of the puzzle by finding unique sequences of differences
    in digit transformations and calculating the maximum aggregated value.

    Args:
        data (list): A list of strings, each representing a number.

    Returns:
        int: The maximum aggregated value of unique sequences.
    """

    sequences = {}

    for line in data:
        num = int(line)
        buyer = [num % 10]  # Start sequence w/ last digit of the number
        for _ in range(2000):  # Generate 2000 additional digits using step()
            num = step(num)
            buyer.append(num % 10)

        seen = set()  # Track sequences seen

        # Iterate through the buyer list to find 5-digit patterns
        for i in range(len(buyer) - 4):
            a, b, c, d, e = buyer[i:i + 5]
            seq = (b - a, c - b, d - c, e - d)  # Calculate sequence of diffs
            if seq in seen:
                continue  # Skip if sequence already processed
            seen.add(seq)  # Mark the sequence as seen.
            if seq not in sequences:
                sequences[seq] = 0
            sequences[seq] += e  # Aggregate the value of the last digit in seq

    return max(sequences.values())  # Return the maximum aggregated value


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 20071921341
    print("Part 2:", part_two(data))  # 2242
