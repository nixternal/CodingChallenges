#!/usr/bin/env python

"""
Codyssi 2025 Siren Disruption Challenge Solution

This program solves a three-part puzzle involving frequency manipulation
to configure earplugs that will mute sirens. Each part implements a different
swapping mechanism to transform track frequencies according to specific rules.

The program reads input from "07.in" which contains:
1. A list of track frequencies
2. A list of swap instructions (in the form X-Y)
3. A test index to verify the solution
"""


def read_puzzle_input() -> str:
    """
    Read and return the puzzle input from the file.

    Returns:
        str: The content of the input file with whitespace stripped
    """

    with open("07.in", "r") as file:
        return file.read().strip()


def parse_input(data: str) -> tuple:
    """
    Parse the input data into its component parts.

    Args:
        data (str): Raw puzzle input

    Returns:
        tuple: Contains three elements:
            - frequencies (dict): Mapping of track numbers to their frequencies
            - swaps (list): List of tuples representing swap instructions
            - test_idx (int): Index used to verify the solution
    """

    # Split into three sections separated by double newlines
    frequencies, swaps, test_idx = data.split('\n\n')

    # Convert frequencies to a dictionary with 1-based indexing
    frequencies = dict(enumerate(frequencies.split('\n'), 1))

    # Convert swap instructions to tuples of integers
    swaps = [
        (int(x), int(y)) for
        swap in swaps.split('\n') for
        x, y in [swap.split('-')]
    ]

    return frequencies, swaps, int(test_idx)


def part_one(data: str) -> str:
    """
    Solve part one of the puzzle: Simple swaps of frequencies.

    For each swap instruction (X-Y), swap the frequencies at tracks X and Y.

    Args:
        data (str): Raw puzzle input

    Returns:
        str: The frequency at the test index after all swaps
    """

    freqs, swaps, test_idx = parse_input(data)

    # Perform simple one-to-one swaps
    for swap in swaps:
        x, y = swap
        freqs[x], freqs[y] = freqs[y], freqs[x]

    return freqs[test_idx]


def part_two(data: str) -> str:
    """
    Solve part two of the puzzle: Triple rotation swaps.

    For each swap instruction at position i:
    - Take the first two indices from the current swap (X, Y)
    - Take the first index from the next swap (Z)
      (For the last swap, Z is the first index of the first swap)
    - Rotate the frequencies: freqs[X], freqs[Y], freqs[Z] = freqs[Z],
      freqs[X], freqs[Y]

    Args:
        data (str): Raw puzzle input

    Returns:
        str: The frequency at the test index after all swaps
    """

    freqs, swaps, test_idx = parse_input(data)

    # Perform triple rotation swaps
    for i in range(len(swaps)):
        # For the last swap, wrap around to the first swap
        if i + 1 >= len(swaps):
            x, y, z = swaps[i][0], swaps[i][1], swaps[0][0]
        else:
            x, y, z = swaps[i][0], swaps[i][1], swaps[i+1][0]

        # Rotate the three frequencies
        freqs[x], freqs[y], freqs[z] = freqs[z], freqs[x], freqs[y]

    return freqs[test_idx]


def part_three(data: str) -> str:
    """
    Solve part three of the puzzle: Block swaps.

    For each swap instruction (X-Y):
    - Find the maximum length of non-overlapping blocks starting at positions
      X and Y
    - Swap corresponding frequencies between the two blocks

    A block is defined as consecutive tracks in ascending order.
    The maximum block length is limited by:
    1. The distance between X and Y (to prevent overlap)
    2. The number of tracks remaining after position Y

    Args:
        data (str): Raw puzzle input

    Returns:
        str: The frequency at the test index after all block swaps
    """

    freqs, swaps, test_idx = parse_input(data)

    # Convert to list for easier manipulation (1-indexed, so index 0 is None)
    trk_freqs = [None] + [freqs[i] for i in range(1, len(freqs) + 1)]

    for swap in swaps:
        x, y = swap

        # Ensure x < y for consistent logic
        if x > y:
            x, y = y, x

        # Calculate the maximum block length that:
        # 1. Doesn't cause blocks to overlap
        # 2. Doesn't extend beyond the end of the track list
        max_block_length = min(y - x, len(trk_freqs) - y)

        # Swap corresponding frequencies between the two blocks
        for i in range(max_block_length):
            trk_freqs[x+i], trk_freqs[y+i] = trk_freqs[y+i], trk_freqs[x+i]

    return trk_freqs[test_idx]


if __name__ == "__main__":
    # Read puzzle input
    data = read_puzzle_input()

    # Solve and print results for all three parts
    print("Part 1:", part_one(data))    # 8273
    print("Part 2:", part_two(data))    # 47354
    print("Part 3:", part_three(data))  # 30088
