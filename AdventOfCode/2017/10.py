#!/usr/bin/env python

"""
Advent of Code 2017 - Day 10: Knot Hash Algorithm

This script implements the Knot Hash algorithm, which consists of two parts:
1. Scrambling a circular list using a sequence of lengths.
2. Computing a hexadecimal hash from the scrambled list.

Usage:
    - Run the script to compute the results for a predefined input.
    - Modify `data` in the `__main__` block to test with different inputs.
"""

from typing import List


def knot_hash(numbers: List[int], lengths: List[int],
              rounds: int = 1) -> List[int]:
    """
    Performs the Knot Hash scrambling process on a circular list.

    Args:
        numbers (List[int]): The initial list of numbers to be scrambled.
        lengths (List[int]): The sequence of lengths used to modify the list.
        rounds (int, optional): Number of times to repeat the process.
                                Defaults to 1.

    Returns:
        List[int]: The modified list after processing all lengths.
    """

    pos = 0  # Current position in the list
    skip = 0  # Skip size increases after each operation
    n = len(numbers)  # Size of the circular list

    for _ in range(rounds):
        for length in lengths:
            # Extract and reverse the section of the list, handling wraparound
            rev_section = [numbers[(pos + i) % n] for i in range(length)]
            rev_section.reverse()

            # Write the reversed section back into the list
            for i in range(length):
                numbers[(pos + i) % n] = rev_section[i]

            # Move forward in the list, adjusting for wraparound
            pos = (pos + length + skip) % n
            skip += 1  # Increment skip size

    return numbers


def compute_dense_hash(scrambled: List[int]) -> List[int]:
    """
    Computes the dense hash from a scrambled list.

    The dense hash is computed by taking 16-byte blocks and XOR-ing all
    elements within each block.

    Args:
        scrambled (List[int]): The list of 256 numbers after 64 rounds of
                               scrambling.

    Returns:
        List[int]: A list of 16 numbers (each rep a block's XOR result).
    """

    dense_hash = []
    for i in range(0, 256, 16):  # Process in blocks of 16
        xor_result = scrambled[i]
        for j in range(1, 16):
            xor_result ^= scrambled[i + j]  # XOR each value in the block
        dense_hash.append(xor_result)

    return dense_hash


def part_one(data: str) -> int:
    """
    Computes the result for Part 1 of the Knot Hash algorithm.

    The first two numbers of the scrambled list are multiplied to produce the
    result.

    Args:
        data (str): A comma-separated string of lengths.

    Returns:
        int: The product of the first two numbers in the scrambled list.
    """

    # Initialize the list with values from 0 to 255
    numbers = list(range(256))

    # Convert input string to a list of integers
    lengths = list(map(int, data.split(',')))

    # Apply the Knot Hash algorithm
    scrambled = knot_hash(numbers, lengths)

    # Multiply the first 2 numbers and return the product
    return scrambled[0] * scrambled[1]


def part_two(data: str) -> str:
    """
    Computes the full Knot Hash (hexadecimal representation).

    This follows the full process:
      1. Convert input string to ASCII values.
      2. Append the fixed suffix `[17, 31, 73, 47, 23]` to the lengths.
      3. Perform 64 rounds of the Knot Hash algorithm.
      4. Compute the dense hash (XOR reduction in blocks of 16).
      5. Convert the dense hash to a hexadecimal string.

    Args:
        data (str): The input string to be hashed.

    Returns:
        str: The final Knot Hash as a 32-character hexadecimal string.
    """

    # Initialize the list with values from 0 to 255
    numbers = list(range(256))

    # Convert input to ASCII + suffix
    lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]

    # Perform 64 rounds
    scrambled = knot_hash(numbers, lengths, rounds=64)

    # Compute dense hash
    dense_hash = compute_dense_hash(scrambled)

    # Convert to a hex string and return
    return ''.join(f'{x:02x}' for x in dense_hash)


if __name__ == "__main__":

    # Input data for the problem (modify if needed)
    data = "199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192"

    # Compute and print results for both parts
    print("Part 1:", part_one(data))  # 3770
    print("Part 2:", part_two(data))  # a9d0e68649d0174c8756a59ba21d4dc6
