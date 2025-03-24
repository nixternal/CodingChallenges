#!/usr/bin/env python

from typing import List, Tuple


def read_puzzle_input(filename: str = "24.in") -> List[Tuple[int, int]]:
    """
    Reads the puzzle input file and parses it into a list of component tuples.

    :param filename: Name of the input file.
    :return: List of (portA, portB) tuples representing bridge components.
    """

    with open(filename, "r") as file:
        return [
            (int(a), int(b)) for
            line in file for
            a, b in [line.strip().split('/')]
        ]


def calc_strongest_bridge(components: List[Tuple[int, int]],
                          open_port: int = 0,
                          used: frozenset = frozenset()) -> int:
    """
    Recursively finds the strongest possible bridge.

    :param components: List of available components.
    :param open_port: The port value to which the next piece must connect.
    :param used: A frozenset of used component indices to prevent reuse.
    :return: Strength of the strongest possible bridge.
    """

    max_strength = 0

    for i, (a, b) in enumerate(components):
        if i in used:
            continue  # Skip components that are already used

        if a == open_port or b == open_port:
            next_port = b if a == open_port else a  # Determine new open port
            bridge_strength = (a + b) + calc_strongest_bridge(
                components, next_port, used | frozenset({i})
            )
            max_strength = max(max_strength, bridge_strength)

    return max_strength


def find_longest_bridge(components: List[Tuple[int, int]],
                        open_port: int = 0,
                        used: frozenset = frozenset()) -> Tuple[int, int]:
    """
    Recursively finds the longest possible bridge. If multiple bridges have
    the same length, the strongest one is chosen.

    :param components: List of available components.
    :param open_port: The port value to which the next piece must connect.
    :param used: A frozenset of used component indices to prevent reuse.
    :return: (length, strength) of the longest valid bridge.
    """

    max_length = 0
    max_strength = 0

    for i, (a, b) in enumerate(components):
        if i in used:
            continue  # Skip already used components

        if a == open_port or b == open_port:
            next_port = b if a == open_port else a  # Determine new open port
            length, strength = find_longest_bridge(
                components, next_port, used | frozenset({i})
            )

            # Update with current component
            length += 1
            strength += (a + b)

            # Prioritize longer bridges,
            # then stronger ones if lengths are equal
            if (length > max_length or
                    (length == max_length and strength > max_strength)):
                max_length = length
                max_strength = strength

    return max_length, max_strength


def part_one(data: List[Tuple[int, int]]) -> int:
    """Solves Part 1: Finds the strength of the strongest bridge."""
    return calc_strongest_bridge(data)


def part_two(data: List[Tuple[int, int]]) -> int:
    """Solves Part 2: Finds the strength of the longest bridge."""
    return find_longest_bridge(data)[1]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1868
    print("Part 2:", part_two(data))  # 1841
