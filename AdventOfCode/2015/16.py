#!/usr/bin/env python

import re

# Define the TICKERTAPE as a dictionary directly instead of parsing it later
TICKERTAPE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def read_puzzle_input(file_path: str = "16.in") -> tuple[dict, list]:
    """
    Reads the puzzle input and parses it into two parts:
    1. `TICKERTAPE` - A predefined dictionary of properties and values.
    2. `data` - A list of lines from the specified input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: A tuple containing `TICKERTAPE` (dict) and `data`
               (list of strings).
    """
    with open(file_path, "r") as file:
        data = file.read().splitlines()
    return TICKERTAPE, data


def parse_aunt_sues(data: list) -> list[dict]:
    """
    Parses the input data to build a list of Aunt Sue profiles.
    Each profile is represented as a dictionary of properties and their values.

    Args:
        data (list): A list of strings describing Aunt Sue profiles.

    Returns:
        list: A list of dictionaries, each representing an Aunt Sue's
              properties.
    """
    pattern = re.compile(
            r'Sue \d+: ([a-z]+): (\d+), ([a-z]+): (\d+), ([a-z]+): (\d+)'
    )
    return [
        {
            match.group(1): int(match.group(2)),
            match.group(3): int(match.group(4)),
            match.group(5): int(match.group(6)),
        }
        for line in data if (match := pattern.match(line))
    ]


def find_matching_aunt(tickertape: dict, data: list, rules: dict = None) -> int:
    """
    Finds the Aunt Sue that matches the given criteria.

    Args:
        tickertape (dict): The target properties to match.
        data (list): The list of Aunt Sue profiles.
        rules (dict, optional): Custom rules for matching certain properties.

    Returns:
        int: The number of the matching Aunt Sue.
    """

    rules = rules or {}

    def could_match(aunt):
        """
        Checks if a given Aunt Sue could match the target properties under
        the given rules.

        Args:
            aunt (dict): A dictionary of properties for an Aunt Sue.

        Returns:
            bool: True if all properties match under the rules,
                  False otherwise.
        """
        for k, v in aunt.items():
            if k in rules:
                if not rules[k](tickertape[k], v):
                    return False
            elif tickertape[k] != v:
                return False
        return True

    # Build Aunt Sue profiles from the input data
    aunts = parse_aunt_sues(data)
    # Find Aunt Sue(s) that match the criteria
    matching_aunts = [
            i + 1 for i, aunt in enumerate(aunts) if could_match(aunt)
    ]
    # Ensure there is exactly one matching Aunt Sue
    assert len(matching_aunts) == 1
    return matching_aunts[0]


def part_one(tickertape: dict, data: list) -> int:
    """
    Solves Part One of the puzzle by finding the Aunt Sue that matches
    the properties in the TICKERTAPE exactly.

    Args:
        tickertape (dict): The target properties to match.
        data (list): The list of Aunt Sue profiles.

    Returns:
        int: The number of the matching Aunt Sue.
    """
    # No special rules for Part One
    return find_matching_aunt(tickertape, data)


def part_two(tickertape: dict, data: list) -> int:
    """
    Solves Part Two of the puzzle with custom matching rules for specific
    properties:
        - "cats" & "trees" values must be > than TICKERTAPE value.
        - "pomeranians" & "goldfish" values must be < than TICKERTAPE value.
        - Other properties must match exactly.

    Args:
        tickertape (dict): The target properties to match.
        data (list): The list of Aunt Sue profiles.

    Returns:
        int: The number of the matching Aunt Sue.
    """
    # Define custom matching rules for specific properties
    rules = {
        "cats": lambda t, v: t < v,
        "trees": lambda t, v: t < v,
        "pomeranians": lambda t, v: t > v,
        "goldfish": lambda t, v: t > v,
    }
    return find_matching_aunt(tickertape, data, rules)


if __name__ == "__main__":
    tickertape, data = read_puzzle_input()
    print("Part One:", part_one(tickertape, data))  # 373
    print("Part Two:", part_two(tickertape, data))  # 260
