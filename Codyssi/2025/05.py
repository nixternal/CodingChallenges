#!/usr/bin/env python

"""
Island Navigation Solver

This module solves three island navigation problems:
1. Find the difference between the furthest and closest islands from the origin
2. Find the shortest distance from the closest island to any other island
3. Calculate the total distance of a path visiting all islands using a greedy
   algorithm

Each problem uses Manhattan distance (|x1-x2| + |y1-y2|) for calculations.
"""

from typing import List, Tuple, Set, Optional


def read_puzzle_input() -> List[str]:
    """
    Read the puzzle input from a file.

    Args:
        filename (str): The name of the input file. Defaults to "05.in".

    Returns:
        list: A list of strings, each representing coordinates in the
              format "(x,y)".
    """

    with open("05.in", "r") as file:
        return file.read().splitlines()


def convert_data_to_coordinates(data: List[str]) -> List[Tuple[int, int]]:
    """
    Convert string coordinates "(x,y)" to a list of integer tuples (x, y).

    Args:
        data (list): A list of strings in the format "(x,y)".

    Returns:
        list: A list of tuples, each containing (x, y) coordinates as integers.
    """

    coordinates = []
    for coords in data:
        # Remove parentheses and split by comma
        nums = coords.strip('()').split(',')
        x, y = map(int, nums)
        coordinates.append((x, y))

    return coordinates


def part_one(data: List[str]) -> int:
    """
    Find the difference between the furthest and closest islands from the
    origin (0, 0).

    Args:
        data (list): A list of coordinate strings.

    Returns:
        int: The difference between the furthest & closest Manhattan distances.
    """

    coordinates = convert_data_to_coordinates(data)

    # Initialize with extreme values
    closest = float('inf')
    furthest = 0

    # Calculate Manhattan distance for each coordinate
    for x, y in coordinates:
        dist = abs(x) + abs(y)  # Manhattan distance from origin
        closest = min(closest, dist)
        furthest = max(furthest, dist)

    return int(furthest - closest)


def part_two(data: List[str]) -> int:
    """
    Find the shortest Manhattan distance from the closest island (to origin)
    to any other island.

    Tiebreakers for the closest island to origin:
    1. Smallest x-coordinate
    2. Smallest y-coordinate

    Args:
        data (list): A list of coordinate strings.

    Returns:
        int: The shortest Manhattan distance from the closest island to any
             other island.
    """

    coordinates = convert_data_to_coordinates(data)

    # Step 1: Find the closest island to the origin (0, 0)
    closest_to_origin = []
    min_distance_to_origin = float('inf')

    for coord in coordinates:
        x, y = coord
        manhattan_distance = abs(x) + abs(y)

        # Check if this island is closer to origin,
        # or if we need to apply tiebreakers
        if manhattan_distance < min_distance_to_origin:
            min_distance_to_origin = manhattan_distance
            closest_to_origin = coord
        elif manhattan_distance == min_distance_to_origin:
            # Tiebreaker 1: smaller x-coordinate
            if x < closest_to_origin[0]:
                closest_to_origin = coord
            elif x == closest_to_origin[0]:
                # Tiebreaker 2: smaller y-coordinate
                if y < closest_to_origin[1]:
                    closest_to_origin = coord

    # Step 2: Find the closest island to our chosen island
    min_distance_to_other_islands = float('inf')

    for coord in coordinates:
        if coord == closest_to_origin:
            continue  # Skip the island we're measuring from

        x1, y1 = closest_to_origin
        x2, y2 = coord
        manhattan_distance = abs(x1 - x2) + abs(y1 - y2)

        min_distance_to_other_islands = min(
            min_distance_to_other_islands, manhattan_distance
        )

    return int(min_distance_to_other_islands)


def part_three(data: List[str]) -> int:
    """
    Calculate the total distance of a path visiting all islands using a
    greedy algorithm. Starting at (0, 0), always move to the closest
    unvisited island. Tiebreakers for the closest island:
        1. Smallest x-coordinate
        2. Smallest y-coordinate

    Args:
        data (list): A list of coordinate strings.

    Returns:
        int: The total Manhattan distance traveled in the path.
    """

    coordinates = convert_data_to_coordinates(data)

    # Handle empty input case
    if not coordinates:
        return 0

    # Convert to a set for O(1) membership test and removal
    unvisited_islands: Set[Tuple[int, int]] = set(coordinates)

    # Initialize
    current_position: Tuple[int, int] = (0, 0)  # Start at origin
    total_distance = 0
    visited_order: List[Tuple[int, int]] = []  # For debugging/verification

    # Visit each island using the greedy algorithm
    while unvisited_islands:
        # Initialize closest_island and min_distance
        closest_island = None
        min_distance = float('inf')

        # Find the closest unvisited island
        closest_island: Optional[Tuple[int, int]] = None
        min_distance = float('inf')

        for island in unvisited_islands:
            x1, y1 = current_position
            x2, y2 = island
            manhattan_distance = abs(x1 - x2) + abs(y1 - y2)

            # First island in iteration: just assign it
            if closest_island is None:
                closest_island = island
                min_distance = manhattan_distance
            # Otherwise compare with current closest
            elif manhattan_distance < min_distance:
                min_distance = manhattan_distance
                closest_island = island
            elif manhattan_distance == min_distance:
                # Tiebreaker 1: smaller x-coordinate
                if x2 < closest_island[0]:
                    closest_island = island
                elif x2 == closest_island[0]:
                    # Tiebreaker 2: smaller y-coordinate
                    if y2 < closest_island[1]:
                        closest_island = island

        # Safety check - shouldn't happen with valid data
        if closest_island is None:
            break

        # Move to the closest island
        total_distance += min_distance
        current_position = closest_island
        visited_order.append(closest_island)
        unvisited_islands.remove(closest_island)

    return int(total_distance)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 643
    print("Part 2:", part_two(data))    # 57
    print("Part 3:", part_three(data))  # 6822
