#!/usr/bin/env python

import re
from collections import defaultdict
from math import prod


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns it as a list of strings.

    Returns:
        list: A list of strings, where each string represents a line from the
              input file.
    """

    with open("10.in", "r") as file:
        return file.read().splitlines()


def simulate_bots(instructions: list, tgt1: int = 0, tgt2: int = 0):
    """
    Simulates the behavior of bots and outputs based on the given instructions.

    Args:
        instructions (list): A list of strings representing the instructions
                             for bots and values.
        tgt1 (int, optional): The first target microchip value to identify
                              the bot. Defaults to 0.
        tgt2 (int, optional): The second target microchip value to identify
                              the bot. Defaults to 0.

    Returns:
        int: If tgt1 and tgt2 are provided, returns the ID of the bot that
             compares these values. Otherwise, returns the product of the
             first microchips in outputs 0, 1, and 2.
    """

    # Initialize the data structures
    bot = defaultdict(list)  # Stores microchips held by each bot
    output = defaultdict(list)  # Stores microchips in output bins
    pipeline = {}  # Stores the rules for how bots pass microchips

    # Parse instructions
    for line in instructions:
        if line.startswith('value'):
            # Extract value and bot ID from "value X goes to bot Y"
            # instructions
            value, bot_id = map(int, re.findall(r'-?\d+', line))
            bot[bot_id].append(value)  # Assign the value to the bot

        if line.startswith('bot'):
            # Extract bot ID, destination types, and destination IDs from "bot
            # X gives low to Y and high to Z" instructions
            bot_id, val1, val2 = map(int, re.findall(r'-?\d+', line))
            type1, type2 = re.findall(r' (bot|output)', line)
            # Store the rules for how the bot passes microchips
            pipeline[bot_id] = (type1, val1), (type2, val2)

    # Simulate the bots
    while bot:
        for key, val in dict(bot).items():
            if len(val) == 2:  # Check if the bot has 2 microchips
                # Sort & remove the microchips from the bot
                val1, val2 = sorted(bot.pop(key))

                # Check if the bot is comparing the target values
                if val1 == tgt1 and val2 == tgt2:
                    return key  # Return the bot ID if it matches the targets

                # Pass the microchips to their destinations based on pipeline
                # rules
                (type1, _val1), (type2, _val2) = pipeline[key]
                eval(type1)[_val1].append(val1)  # Pass the low val to dest
                eval(type2)[_val2].append(val2)  # Pass the high val to dest

    # No targets come from Part Two of the puzzle, so return the product of the
    # first microchips in outputs 0, 1, and 2
    return prod(output[key][0] for key in [0, 1, 2])


def part_one(data: list) -> int:
    return simulate_bots(data, 17, 61)


def part_two(data: list) -> int:
    return simulate_bots(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 141
    print("Part 2:", part_two(data))  # 1209
