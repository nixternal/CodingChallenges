#!/usr/bin/env python
"""
Advent of Code 2018 - Day 14: Chocolate Charts

This script solves both parts of the problem:
- Part 1: Simulates the chocolate recipe scoreboard and returns the next 10
          recipes after a given number of recipes.
- Part 2: Finds the first occurrence of a given sequence of digits in the
          scoreboard.

The solution follows the problem's rules for recipe generation and elf movement
"""


def part_one(target_recipes: int) -> str:
    """
    Simulates the chocolate recipe scoreboard and returns the next 10 recipes
    after the given number of recipes.

    Process:
    - Start with the initial recipes [3, 7].
    - Each iteration, sum the recipes where the two elves are positioned.
    - Append the resulting digits to the scoreboard.
    - Move the elves forward based on their current recipes.
    - Continue until the total number of recipes is at least target_recipes+10

    Args:
        target_recipes (int): The number of recipes to process before
                              extracting the next 10.

    Returns:
        str: String representation of the next 10 recipes after target_recipes
    """

    recipes = [3, 7]   # Initial recipes
    elf1, elf2 = 0, 1  # Initial elf positions

    while len(recipes) < target_recipes + 10:
        # Generate new recipes
        new_recipe = recipes[elf1] + recipes[elf2]
        if new_recipe >= 10:
            recipes.append(new_recipe // 10)  # Append 1st digit if 2-digit num
        recipes.append(new_recipe % 10)  # Append second digit

        # Move elves forward
        elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
        elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)

    return ''.join(map(str, recipes[target_recipes:target_recipes + 10]))


def part_two(target_sequence: int) -> int:
    """
    Finds the first occurrence of a given target sequence in the recipe
    scoreboard.

    Process:
    - Start with the initial recipes [3, 7].
    - Generate new recipes by summing the elves' current recipes.
    - Append the resulting digits to the scoreboard.
    - Continuously check if the last digits match the target sequence.
    - If a match is found, return the index where the sequence starts.

    Args:
        target_sequence (str): The sequence of digits to find in the scoreboard

    Returns:
        int: The index at which the target sequence first appears.
    """

    # Convert input sequence to list of digits
    target_list = list(map(int, str(target_sequence)))
    target_length = len(target_list)
    recipes = [3, 7]   # Initial recipes
    elf1, elf2 = 0, 1  # Initial elf positions

    while True:
        # Generate new recipes
        new_recipe = recipes[elf1] + recipes[elf2]
        if new_recipe >= 10:
            recipes.append(new_recipe // 10)  # Append 1st digit if 2-digit num
            if recipes[-target_length:] == target_list:
                return len(recipes) - target_length

        recipes.append(new_recipe % 10)  # Append second digit
        if recipes[-target_length:] == target_list:
            return len(recipes) - target_length

        # Move elves forward
        elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
        elf2 = (elf2 + 1 + recipes[elf2]) % len(recipes)


if __name__ == "__main__":
    data = 540391
    print("Part 1:", part_one(data))  # 1474315445
    print("Part 2:", part_two(data))  # 20278122
