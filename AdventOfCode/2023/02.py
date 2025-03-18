#!/usr/bin/env python

import os


def parse_input() -> list:
    """
    Reads the input file and splits the contents into a list of lines.

    Returns:
        list: A list of strings, where each string is line from the input file.
    """

    with open(
            os.path.splitext(os.path.basename(__file__))[0] + '.in',
            'r') as file:
        return file.read().splitlines()


def part_one(data: list, red: int, green: int, blue: int) -> int:
    """
    Computes the sum of game numbers where the largest red, green, and blue
    cube values in each game are within the specified limits.

    Args:
        data (list): A list of game descriptions passed from parse_input()
        red (int): The maximum allowed value for red cubes.
        green (int): The maximum allowed value for green cubes.
        blue (int): The maximum allowed value for blue cubes.

    Returns:
        int: The sum of the game numbers that satisfy the conditions.
    """

    # The following commented out code is my original
    # sum = 0
    # for game in data:
    #     num = int(game.split(':')[0].replace('Game ', ''))
    #     r, g, b = [], [], []
    #     for cubes in game.split(':')[1].replace(';', ',').split(','):
    #         if 'red' in cubes:
    #             r.append(int(cubes.split()[0]))
    #         if 'green' in cubes:
    #             g.append(int(cubes.split()[0]))
    #         if 'blue' in cubes:
    #             b.append(int(cubes.split()[0]))
    #     r = sorted(r).pop()
    #     g = sorted(g).pop()
    #     b = sorted(b).pop()
    #     if r <= red and g <= green and b <= blue:
    #         sum += num

    # The following code is what ChatGPT said was the optimized version of what
    # I did above.
    sum = 0
    for game in data:
        num, cubes_desc = game.split(':')
        num = int(num.replace('Game ', ''))

        # Initialize  maximum values for each color
        max_r, max_g, max_b = 0, 0, 0

        # Process each cube count
        for cubes in cubes_desc.replace(';', ',').split(','):
            value, color = int(cubes.split()[0]), cubes.split()[1]

            if 'red' in color:
                max_r = max(max_r, value)
            if 'green' in color:
                max_g = max(max_g, value)
            if 'blue' in color:
                max_b = max(max_b, value)

        if max_r <= red and max_g <= green and max_b <= blue:
            sum += num

    return sum


def part_two(data: list) -> int:
    """
    Computes the sum of the products of the largest red, green, and blue cube
    values for each game.

    Args:
        data (list): A list of game descriptions passed from parse_input()

    Returns:
        int: The total sum of the products of the largest red, green and blue
             cube values.
    """

    # The following commented out code is my original
    # sum = 0
    # for game in data:
    #     r = []
    #     g = []
    #     b = []
    #     for cubes in game.split(':')[1].replace(';', ',').split(','):
    #         if 'red' in cubes:
    #             r.append(int(cubes.split()[0]))
    #         if 'green' in cubes:
    #             g.append(int(cubes.split()[0]))
    #         if 'blue' in cubes:
    #             b.append(int(cubes.split()[0]))
    #     r = sorted(r).pop()
    #     g = sorted(g).pop()
    #     b = sorted(b).pop()
    #     sum += r * g * b

    # This is borrowing off the optimized code from part_one():
    sum = 0
    for game in data:
        num, cubes_desc = game.split(':')
        num = int(num.replace('Game ', ''))

        # Initialize  maximum values for each color
        max_r, max_g, max_b = 0, 0, 0

        # Process each cube count
        for cubes in cubes_desc.replace(';', ',').split(','):
            value, color = int(cubes.split()[0]), cubes.split()[1]

            if 'red' in color:
                max_r = max(max_r, value)
            if 'green' in color:
                max_g = max(max_g, value)
            if 'blue' in color:
                max_b = max(max_b, value)

        sum += max_r * max_g * max_b
    return sum


if __name__ == "__main__":
    data = parse_input()
    # print("Part 1:", test_one(data))
    print("Part 1:", part_one(data, 12, 13, 14))  # 2776
    print("Part 2:", part_two(data))              # 68638
