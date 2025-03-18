#!/usr/bin/env python

import re
from typing import List, Tuple


def read_puzzle_input() -> List[Tuple[int, int]]:
    """
    Reads the puzzle input from a file named '15.in' and extracts disc
    information.

    Each line in the input describes a rotating disc with:
      - A total number of positions.
      - A starting position.

    Example input line:
        "Disc #1 has 5 positions; at time=0, it is at position 4."

    This function extracts `(5, 4)` from the above line.

    Returns:
        List[Tuple[int, int]]: A list of tuples where:
            - The first value is the number of positions the disc has.
            - The second value is the starting position of the disc.
    """

    with open("15.in", "r") as file:
        discs = []
        for line in file:
            # Use regex to extract the number of positions & starting position
            match = re.search(r"(\d+) positions.*position (\d+)", line)
            if match:
                # Convert extracted values to integers
                discs.append((int(match.group(1)), int(match.group(2))))
        return discs


def solve_discs(discs: list) -> int:
    """
    Determines the earliest time 't' at which a capsule can be dropped
    and pass through all the discs without being blocked.

    Each disc moves by one position per second. The capsule takes (i+1) seconds
    to reach the ith disc, so at time 't', the condition for a successful pass
    is:

        (t + i + 1 + start_position) % num_positions == 0

    for every disc `i`.

    This function finds the smallest `t` that satisfies this condition for
    all discs.

    Args:
        discs (List[Tuple[int, int]]): A list of tuples, each containing:
            - The number of positions the disc has.
            - The starting position of the disc.

    Returns:
        int: The first valid time 't' when the capsule can successfully pass.
    """

    t = 0
    while True:
        # Check if all discs align correctly at time 't'
        if all((t + i + 1 + start) % positions == 0 for i,
                (positions, start) in enumerate(discs)):
            return t  # Return the first valid time
        t += 1  # Increment time and try again


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle using the given disc configuration.

    Args:
        data (List[Tuple[int, int]]): The list of discs from the input file.

    Returns:
        int: The first valid time 't' when the capsule can successfully pass
             through all discs.
    """

    return solve_discs(data)


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle by adding an extra disc to the configuration.

    The extra disc has:
      - 11 positions.
      - Starts at position 0.

    This function modifies the input data and then finds the first valid time.

    Args:
        data (List[Tuple[int, int]]): The list of discs from the input file.

    Returns:
        int: The first valid time 't' when the capsule can successfully pass
             through all discs, including the newly added disc.
    """

    data.append((11, 0))
    return solve_discs(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 203660
    print("Part 2:", part_two(data))  # 2408135
