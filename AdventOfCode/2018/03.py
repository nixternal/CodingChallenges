#!/usr/bin/env python3

import re


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns a list of claims as strings.
    """

    with open("03.in", "r") as file:
        return file.read().splitlines()


def parse_claim(claim):
    """
    Parses a fabric claim string and extracts the relevant numbers.

    Example input: "#123 @ 3,2: 5x4"
    Returns: (123, 3, 2, 5, 4)
    """

    return tuple(map(int, re.findall(r'\d+', claim)))


def part_one(claims):
    """
    Determines the number of square inches of fabric that have overlapping
    claims.

    Args:
        claims (list): List of fabric claim strings.

    Returns:
        int: Count of overlapping square inches.
    """

    fabric = {}  # Dictionary to track fabric usage (x, y) -> count

    for claim in claims:
        _, x, y, w, h = parse_claim(claim)
        for dx in range(w):
            for dy in range(h):
                fabric[(x + dx, y + dy)] = fabric.get((x + dx, y + dy), 0) + 1

    return sum(1 for count in fabric.values() if count > 1)


def part_two(claims):
    """
    Identifies the claim ID that does not overlap with any other claims.

    Args:
        claims (list): List of fabric claim strings.

    Returns:
        int: The ID of the non-overlapping claim.
    """
    fabric = {}  # Dictionary tracking (x, y) -> set of claim IDs
    all_claims = set()

    # Track claim coverage
    for claim in claims:
        claim_id, x, y, w, h = parse_claim(claim)
        all_claims.add(claim_id)
        for dx in range(w):
            for dy in range(h):
                coord = (x + dx, y + dy)
                if coord not in fabric:
                    fabric[coord] = {claim_id}
                else:
                    fabric[coord].add(claim_id)

    # Remove overlapping claims
    for ids in fabric.values():
        if len(ids) > 1:
            all_claims.difference_update(ids)

    return all_claims.pop()  # The remaining claim is the non-overlapping one


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 119551
    print("Part 2:", part_two(data))  # 1124
