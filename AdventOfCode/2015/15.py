#!/usr/bin/env python

import re
from itertools import product


def read_puzzle_input() -> list:
    """
    Brute Force

    Reads the input file and returns a list of strings, each representing a
    line of input.

    Returns:
        list: List of strings where each string is a line from the input file.
    """

    with open("15.in", "r") as file:
        return file.read().splitlines()


def generate_amounts():
    """
    Generates all valid combinations of teaspoon amounts to make sure all
    given ingredients when combined will equal 100 teaspoons. This is
    brute-forced in this example.

    Yields:
        list: A list of 4 integers representing amount of each ingredient in
              teaspoons.
    """
    # for a in range(1, 100):
    #     for b in range(1, 100):
    #         for c in range(1, 100):
    #             d = 100 - a - b - c
    #             if d > 0:
    #                 yield [a, b, c, d]

    for a, b, c in product(range(1, 100), repeat=3):
        d = 100 - a - b - c  # Calculate the remaining amount
        if d > 0:  # Ensure the last ingredient has a valid amount
            yield [a, b, c, d]


def part_one(data: list) -> int:
    """
    Calculates the maximum score of all ingredient combinations based on
    their properties.

    Args:
        data (list): A list of strings representing the ingredient properties.

    Returns:
        int: The maximum score achievable with the given properties.
    """

    # Regex pattern to extract property values (4 properties & 1 calorie count)
    # Calories are ignored for Part 1
    regex = r".+?(-?\d+).+?(-?\d+).+?(-?\d+).+?(-?\d+).+?(-?\d+)"

    # Initialize lists to hold property values for all ingredients
    properties = [[], [], [], []]

    # Parse the input data and populate the property lists
    for line in data:
        # Extract first 4 properties
        values = list(map(int, re.findall(regex, line)[0][:4]))
        for i, value in enumerate(values):
            properties[i].append(value)

    def calculate_score(amount):
        """
        Calculates the score for a given combination of ingredient amounts.

        Args:
            amount (list): A list of four integers representing the amounts
                           of each ingredient.

        Returns:
            int: The calculated score for the given combination.
        """

        # Compute scores for each property by summing the weighted
        # contributions of all ingredients
        scores = [
            max(
                0,
                sum(
                    properties[prop][i] * amount[i] for i in range(len(data))
                )
            )
            for prop in range(len(properties))
        ]
        # Return the product of all property scores
        return scores[0] * scores[1] * scores[2] * scores[3]

    # Return the maximum score across all valid combinations
    return max(calculate_score(amount) for amount in generate_amounts())


def part_two(data: list) -> int:
    """
    Calculates the maximum score of all ingredient combinations, ensuring the
    total calories are 500.

    Args:
        data (list): A list of strings representing the ingredient properties.

    Returns:
        int: The maximum score achievable with the given properties and
             calorie constraint.
    """

    # Regex pattern to extract property values (4 properties & 1 calorie count)
    regex = r".+?(-?\d+).+?(-?\d+).+?(-?\d+).+?(-?\d+).+?(-?\d+)"

    # Initialize lists to hold property values for all ingredients
    properties = [[], [], [], [], []]

    # Parse the input data and populate the property lists
    for line in data:
        # Extract all 5 properties
        values = list(map(int, re.findall(regex, line)[0]))
        for i, value in enumerate(values):
            properties[i].append(value)

    def calculate_score(amount):
        """
        Calculates the score for a given combination of ingredient amounts
        with a calorie constraint.

        Args:
            amount (list): A list of four integers representing the amounts
                           of each ingredient.

        Returns:
            int: The calculated score if the calorie constraint is met,
                 otherwise 0.
        """

        # Compute scores for each property by summing the weighted
        # contributions of all ingredients
        scores = [
            max(
                0,
                sum(
                    properties[prop][i] * amount[i] for i in range(len(data))
                )
            )
            for prop in range(len(properties))
        ]

        # Check if the calorie constraint is met
        if scores[4] == 500:  # Calories are the 5th property
            return scores[0] * scores[1] * scores[2] * scores[3]
        return 0

    # Return the maximum score across all valid combinations that meet the
    # calorie constraint
    return max(calculate_score(amount) for amount in generate_amounts())


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 222870
    print("Part 2:", part_two(data))  # 117936
