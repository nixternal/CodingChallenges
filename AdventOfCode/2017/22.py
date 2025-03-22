#!/usr/bin/env python

from collections import defaultdict


def read_puzzle_input() -> list:
    with open("22.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Simulates the virus spreading across the grid for a given number of bursts.

    Args:
        grid (list of str): The initial grid representing infected (#) and
                            clean (.) nodes.
        bursts (int): The number of steps to simulate.

    Returns:
        int: The total number of infections caused by the virus.
    """

    grid = data.copy()
    bursts = 10000

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_index = 0  # Start facing up
    # Start at the center of the grid
    x, y = len(grid) // 2, len(grid[0]) // 2
    infections = 0  # Counter for infections caused

    # Convert the grid to a dictionary for easier manipulation
    # Keys are (x, y) coordinates, values are the state ('#' or '.')
    grid_dict = defaultdict(lambda: '.')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid_dict[(i, j)] = grid[i][j]

    for _ in range(bursts):
        # Check the current node's state
        current_node = (x, y)
        if grid_dict[current_node] == '#':
            # Infected: Turn right
            dir_index = (dir_index + 1) % 4
            # Clean the node
            grid_dict[current_node] = '.'
        else:
            # Clean: Turn left
            dir_index = (dir_index - 1) % 4
            # Infect the node
            grid_dict[current_node] = '#'
            infections += 1

        # Move forward in the new direction
        dx, dy = directions[dir_index]
        x += dx
        y += dy

    return infections


def part_two(data: list) -> int:
    """
    Simulates the virus spreading across the grid for a given number of bursts.

    Args:
        grid (list of str): The initial grid representing node states.
        bursts (int): The number of steps to simulate.

    Returns:
        int: The total number of infections caused by the virus.
    """

    grid = data.copy()
    bursts = 10000000

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dir_index = 0  # Start facing up
    x, y = len(grid) // 2, len(grid[0]) // 2  # Start at the center of the grid
    infections = 0  # Counter for infections caused

    # Convert the grid to a dictionary for easier manipulation
    # Keys are (x, y) coordinates, values are the state ('.', 'W', '#', or 'F')
    grid_dict = defaultdict(lambda: '.')
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid_dict[(i, j)] = grid[i][j]

    for _ in range(bursts):
        # Check the current node's state
        current_node = (x, y)
        state = grid_dict[current_node]

        if state == '.':
            # Clean: Turn left
            dir_index = (dir_index - 1) % 4
            # Change to weakened
            grid_dict[current_node] = 'W'
        elif state == 'W':
            # Weakened: Do not turn
            # Change to infected
            grid_dict[current_node] = '#'
            infections += 1
        elif state == '#':
            # Infected: Turn right
            dir_index = (dir_index + 1) % 4
            # Change to flagged
            grid_dict[current_node] = 'F'
        elif state == 'F':
            # Flagged: Reverse direction
            dir_index = (dir_index + 2) % 4
            # Change to clean
            grid_dict[current_node] = '.'

        # Move forward in the new direction
        dx, dy = directions[dir_index]
        x += dx
        y += dy

    return infections


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 5305
    print("Part 2:", part_two(data))  # 2511424
