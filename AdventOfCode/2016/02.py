#!/usr/bin/env python

KEYPAD2 = [
    ['.', '.', '1', '.', '.'],
    ['.', '2', '3', '4', '.'],
    ['5', '6', '7', '8', '9'],
    ['.', 'A', 'B', 'C', '.'],
    ['.', '.', 'D', '.', '.']
]


def read_puzzle_input() -> list:
    with open("02.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> str:
    # Define the keypad layout
    keypad = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

    # Initialize the starting position
    x, y = 1, 1

    # Initialize an empty password
    password = ''

    #                   LEFT        RIGHT           UP          DOWN
    directions = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

    for commands in data:
        for cmd in commands:
            # Calculate the new position
            dx, dy = directions.get(cmd, (0, 0))
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within bounds
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                x, y = new_x, new_y

        # Append the corresponding keypad value to the password
        password += keypad[x][y]

    return password


def part_two(data: list) -> str:
    # Define the keypad layout
    keypad = [
        [0, 0, '1', 0, 0],
        [0, '2', '3', '4', 0],
        ['5', '6', '7', '8', '9'],
        [0, 'A', 'B', 'C', 0],
        [0, 0, 'D', 0, 0]
    ]

    # Initialize the starting position
    x, y = 2, 0

    # Initialize an empty passord
    password = ''

    #                   LEFT        RIGHT           UP          DOWN
    directions = {'L': (0, -1), 'R': (0, 1), 'U': (-1, 0), 'D': (1, 0)}

    for commands in data:
        for cmd in commands:
            # Calculate the new position
            dx, dy = directions.get(cmd, (0, 0))
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within bound and not 0
            if 0 <= new_x < 5 and 0 <= new_y < 5 and keypad[new_x][new_y]:
                x, y = new_x, new_y

        # Append the corresponding keypad value to the password
        password += keypad[x][y]

    return password


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 44558
    print("Part 2:", part_two(data))  # 6BBAD
