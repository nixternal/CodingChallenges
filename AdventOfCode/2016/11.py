#!/usr/bin/env python

import re
from collections import deque, Counter
from itertools import chain, combinations


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named "11.in" and returns it as a list
    of strings.

    Returns:
        list: A list of strings, each representing a line in the input file.
    """

    with open("11.in", "r") as file:
        return file.read().splitlines()


def parse_floors(input: list) -> list:
    """
    Parses the input to extract the items (microchips and generators) on each
    floor.

    Args:
        input (list): The raw input data as a list of strings.

    Returns:
        list: A list of sets, each representing the items on a floor. Each
              item is a tuple (name, type).
    """

    return [
        set(
            re.findall(r'(\w+)(?:-compatible)? (microchip|generator)', line)
        ) for line in input
    ]


def is_valid_transition(floor: list) -> bool:
    """
    Checks if a floor configuration is valid.

    A floor is valid if either:
    1. It contains only one type of object (microchips or generators).
    2. Every microchip is protected by its corresponding generator.

    Args:
        floor (list): A list of tuples representing items on the floor.

    Returns:
        bool: True if the floor configuration is valid, False otherwise.
    """

    return len(set(type for _, type in floor)) < 2 or all(
        (obj, 'generator') in floor for (
            obj, type) in floor if type == 'microchip')


def next_states(state: tuple):
    """
    Generates all valid next states from the current state.

    Args:
        state (tuple): The current state as a tuple (moves, elevator, floors).
        - moves: Number of moves taken so far.
        - elevator: Current elevator position (0-indexed).
        - floors: List of sets representing items on each floor.

    Yields:
        tuple: The next state as (moves + 1, next_elevator, next_floors).
    """

    moves, elevator, floors = state

    # Generate all possible combinations of 1 or 2 items to move
    possible_moves = chain(combinations(floors[elevator], 2),
                           combinations(floors[elevator], 1))

    for move in possible_moves:
        for direction in [-1, 1]:  # Elevator can move up (+1) or down (-1)
            next_elevator = elevator + direction

            # Check if the next elevator position is valid
            if not 0 <= next_elevator < len(floors):
                continue

            # Compute the next floor configurations
            next_floors = floors.copy()
            next_floors[elevator] = next_floors[elevator].difference(move)
            next_floors[next_elevator] = next_floors[next_elevator].union(move)

            # Validate the current and next floors
            if (is_valid_transition(next_floors[elevator]) and
                    is_valid_transition(next_floors[next_elevator])):
                yield (moves + 1, next_elevator, next_floors)


def count_floor_objects(state: tuple) -> tuple:
    """
    Counts and encodes the types of objects on each floor and the elevator
    position.

    Args:
        state (tuple): The current state as (moves, elevator, floors).

    Returns:
        tuple: A tuple representing the elevator position and the object
               counts for each floor.
    """

    _, elevator, floors = state
    return elevator, tuple(tuple(
        Counter(type for _, type in floor).most_common()) for floor in floors
    )


def is_all_top_level(floors: list) -> bool:
    """
    Checks if all objects are on the top floor.

    Args:
        floors (list): List of sets representing items on each floor.

    Returns:
        bool: True if all objects are on the top floor, False otherwise.
    """

    return all(
        not floor for number, floor in enumerate(
            floors) if number < len(floors) - 1
    )


def min_moves_to_top_level(floors: list) -> int:
    """
    Uses a breadth-first search (BFS) to determine the minimum moves needed
    to bring all items to the top floor.

    Args:
        floors (list): List of sets representing items on each floor.

    Returns:
        int: The minimum number of moves required.
    """

    seen = set()  # To track visited states
    # Initialize the BFS queue with (moves, elevator, floors)
    queue = deque([(0, 0, floors)])

    while queue:
        state = queue.popleft()
        moves, _, floors = state

        # Check if all items are on the top floor
        if is_all_top_level(floors):
            return moves

        # Explore all valid next states
        for next_state in next_states(state):
            if (key := count_floor_objects(next_state)) not in seen:
                seen.add(key)
                queue.append(next_state)

    return 0


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle.

    Args:
        data (list): The puzzle input as a list of strings.

    Returns:
        int: The minimum number of moves required for Part 1.
    """

    return min_moves_to_top_level(parse_floors(data))


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle, adding four additional items to the first
    floor.

    Args:
        data (list): The puzzle input as a list of strings.

    Returns:
        int: The minimum number of moves required for Part 2.
    """

    floors = parse_floors(data)
    floors[0] = floors[0].union(
        [
            ('elerium', 'generator'),
            ('elerium', 'microchip'),
            ('dilithium', 'generator'),
            ('dilithium', 'microchip')
        ]
    )
    return min_moves_to_top_level(floors)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # Expected output: 33
    print("Part 2:", part_two(data))  # Expected output: 57
