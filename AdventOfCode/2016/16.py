#!/usr/bin/env python

"""
Dragon Curve Checksum Generator

This module implements a modified Dragon Curve algorithm to generate a checksum
for binary data. It uses a special data expansion technique followed by a
checksum computation that ensures data integrity.

The algorithm works by repeatedly expanding the input data using a modified
dragon curve pattern and then computing a checksum on the expanded data.
This is commonly used in scenarios where data needs to be expanded in a
deterministic way while maintaining certain mathematical properties.
"""


def expand_data(initial_state: str, length: int) -> str:
    """
    Expands a binary string using a modified dragon curve algorithm until it
    reaches or exceeds the specified length, then truncates to exact length.

    The expansion process follows these steps for each iteration:
    1. Take the current data
    2. Create a reversed and bit-flipped version of it (0→1, 1→0)
    3. Join original + '0' + modified version
    4. Repeat until desired length is reached or exceeded

    Args:
        initial_state (str): Starting string (containing only '0' and '1')
        length (int): The desired length of the final expanded string

    Returns:
        str: Expanded binary string truncated to exactly 'length' characters

    Examples:
        >>> expand_data('1', 3)
        '100'
        >>> expand_data('111', 6)
        '111000'

    Note:
        - The input string must contain only '0' and '1' characters
        - The function will always return a string of exactly 'length'
          characters
        - Each expansion step produces a string slightly more than double the
          original length
    """

    data = initial_state
    while len(data) < length:
        # Create a reversed and flipped version of the current data
        # Example: '111' becomes '000' (reverse and flip bits)
        reversed_flipped = ''.join(
            ['1' if bit == '0' else '0' for bit in data[::-1]]
        )
        # Combine original data + '0' + modified version
        # Example: '111' + '0' + '000' becomes '1110000'
        data = data + '0' + reversed_flipped

    # Return only the requested length, truncating any excess
    return data[:length]


def compute_checksum(data: str) -> str:
    """
    Computes a checksum for the given binary string using a pair-matching
    algorithm.

    The checksum is computed by repeatedly:
    1. Taking pairs of characters
    2. Replacing each pair with '1' if they match, '0' if they don't
    3. Continuing until the resulting string has odd length

    Args:
        data (str): The binary string to compute checksum for (containing only
                    '0' and '1')

    Returns:
        str: The computed checksum string

    Examples:
        >>> compute_checksum('110010')
        '110'
        >>> compute_checksum('1111')
        '1'

    Note:
        - Input string must contain only '0' and '1' characters
        - The process continues until the resulting string has an odd length
        - Each iteration reduces the string length by approximately half
    """

    checksum = data
    while len(checksum) % 2 == 0:
        new_checksum = []
        # Process pairs of characters
        for i in range(0, len(checksum), 2):
            # If pair matches (00 or 11), append '1'; otherwise append '0'
            if checksum[i] == checksum[i+1]:
                new_checksum.append('1')
            else:
                new_checksum.append('0')
        checksum = ''.join(new_checksum)
    return checksum


def part_one() -> str:
    """
    Solves part one of the dragon curve challenge by expanding the initial
    state to length 272 and computing its checksum.

    Returns:
        str: The computed checksum for the expanded data

    Note:
        The initial state '10111100110001111' is expanded to length 272
        before computing the checksum.
    """

    return compute_checksum(expand_data('10111100110001111', 272))


def part_two() -> str:
    """
    Solves part two of the dragon curve challenge by expanding the initial
    state to length 35651584 and computing its checksum.

    Returns:
        str: The computed checksum for the expanded data

    Note:
        The initial state '10111100110001111' is expanded to length 35651584
        before computing the checksum. This is a significantly larger expansion
        than part one and may take longer to compute.
    """

    return compute_checksum(expand_data('10111100110001111', 35651584))


if __name__ == "__main__":
    # Execute both parts of the challenge and print results
    print("Part 1:", part_one())  # 11100110111101110
    print("Part 2:", part_two())  # 10001101010000101
