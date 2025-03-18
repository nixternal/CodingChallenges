#!/usr/bin/env python

import numpy as np
import re


def read_puzzle_input() -> list:
    with open("06.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Simulates a grid of lights and calculates the number of lights that are on
    after processing a series of commands.

    Each command specifies an action ("turn on", "turn off", or "toggle") to be
    applied to a rectangular region of the grid.

    ORIGINAL VERSION at the bottom of the file

    Parameters:
        data (list): A list of command strings. Each string contains an action
                     ("turn on", "turn off", or "toggle") and two coordinate
                     pairs specifying the corners of a rectangle.

    Returns:
        int: The number of lights that are on after all commands are processed.
    """

    # Initialize a 1000x1000 grid of False (all lights are off)
    lights = np.zeros((1000, 1000), dtype=bool)

    # Precompile regex for efficiency
    pattern = re.compile(r"(\d+),(\d+)")

    # Process each command in the input data
    for command in data:
        # Extract coordinates
        coords = pattern.findall(command)
        x1, y1 = map(int, coords[0])
        x2, y2 = map(int, coords[1])

        # Process commands
        if "on" in command:
            # Turn on the lights in the specified region
            lights[x1:x2+1, y1:y2+1] = True
        elif "off" in command:
            # Turn off the lights in the specified region
            lights[x1:x2+1, y1:y2+1] = False
        elif "toggle" in command:
            # Toggle the lights in the specified region (invert their state)
            lights[x1:x2+1, y1:y2+1] ^= True

    # Calculate & return the total number of lights that are on
    # (True values are treated as 1, and False values as 0)
    return np.sum(lights)


def part_two(data: list) -> int:
    """
    Simulates a grid of lights with brightness levels and calculates the total
    brightness after processing a series of commands.

    Each command specifies an action ("turn on", "turn off", or "toggle") to be
    applied to a rectangular region of the grid. Brightness levels change as
    follows:
        - "turn on" increases brightness by 1.
        - "turn off" decreases brightness by 1 (brightness cannot go below 0).
        - "toggle" increases brightness by 2.

    ORIGINAL VERSION at the bottom of the file

    Parameters:
        data (list): A list of command strings. Each string contains an action
                     ("turn on", "turn off", or "toggle") & 2 coordinate pairs
                     specifying the corners of a rectangle.

    Returns:
        int: Total brightness of all lights after all commands are processed.
    """

    # Initialize a 1000x1000 grid of integers representing brightness levels
    # (all start at 0)
    lights = np.zeros((1000, 1000), dtype=int)

    # Precompile the regex pattern to extract coordinates for efficiency
    pattern = re.compile(r"(\d+),(\d+)")

    # Process each command in the input data
    for command in data:
        # Extract the coordinates from the command
        coords = pattern.findall(command)
        x1, y1 = map(int, coords[0])
        x2, y2 = map(int, coords[1])

        if "on" in command:
            # Increase brightness by 1 in the specified region
            lights[x1:x2+1, y1:y2+1] += 1
        elif "off" in command:
            # Decrease brightness by 1 in the specified region, but ensure no
            # value goes below 0
            lights[x1:x2+1, y1:y2+1] = np.maximum(
                    lights[x1:x2+1, y1:y2+1] - 1, 0)
        elif "toggle" in command:
            # Increase brightness by 2 in the specified region
            lights[x1:x2+1, y1:y2+1] += 2

    # Calculate & return the total brightness (sum of all brightness levels)
    return np.sum(lights)

    # ORIGINAL - slow!
    # pattern = re.compile(r"(\d+),(\d+)")
    # lights = defaultdict(int)

    # for command in data:
    #     coords = pattern.findall(command)
    #     x1, y1 = map(int, coords[0])
    #     x2, y2 = map(int, coords[1])

    #     if "on" in command:
    #         action = "on"
    #     elif "toggle" in command:
    #         action = "toggle"
    #     else:
    #         action = "off"

    #     for x in range(x1, x2 + 1):
    #         for y in range(y1, y2 + 1):
    #             point = (x, y)

    #             if action == "on":
    #                 lights[point] += 1
    #             elif action == "toggle":
    #                 lights[point] += 2
    #             elif action == "off" and lights[point] > 0:
    #                 lights[point] -= 1

    # return sum(lights.values())


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 377891
    print("Part 2:", part_two(data))  # 14110788

    # part_one() : ORIGINAL - slow!
    # on = set()
    # for command in data:
    #     coords = re.findall(r"(\d+),(\d+)", command)
    #     x1, y1 = map(int, coords[0])
    #     x2, y2 = map(int, coords[1])
    #     action = None
    #     if "on" in command:
    #         action = "on"
    #     elif "toggle" in command:
    #         action = "toggle"
    #     else:
    #         action = "off"

    #     for x in range(x1, x2 + 1):
    #         for y in range(y1, y2 + 1):
    #             point = (x, y)
    #             if "on" in action and point not in on:
    #                 on.add(point)
    #                 continue

    #             if "off" in action and point in on:
    #                 on.discard(point)
    #                 continue

    #             if "toggle" in action:
    #                 if point not in on:
    #                     on.add(point)
    #                 else:
    #                     on.discard(point)

    # return len(on)

    # part_two() : ORIGINAL - slow!
    # pattern = re.compile(r"(\d+),(\d+)")
    # lights = defaultdict(int)

    # for command in data:
    #     coords = pattern.findall(command)
    #     x1, y1 = map(int, coords[0])
    #     x2, y2 = map(int, coords[1])

    #     if "on" in command:
    #         action = "on"
    #     elif "toggle" in command:
    #         action = "toggle"
    #     else:
    #         action = "off"

    #     for x in range(x1, x2 + 1):
    #         for y in range(y1, y2 + 1):
    #             point = (x, y)

    #             if action == "on":
    #                 lights[point] += 1
    #             elif action == "toggle":
    #                 lights[point] += 2
    #             elif action == "off" and lights[point] > 0:
    #                 lights[point] -= 1

    # return sum(lights.values())
