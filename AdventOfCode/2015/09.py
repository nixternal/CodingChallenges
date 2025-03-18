#!/usr/bin/env python
"""
Traveling Salesman/Salesperson Problem
https://en.wikipedia.org/wiki/Travelling_salesman_problem
"""

import itertools


def read_puzzle_input() -> list:
    """
    Reads the input data from a file and parses it into a list of tuples
    representing the distances between city pairs.

    Each line of the input file is expected to have the format:
    'City1 to City2 = distance'.

    Returns:
        list: A list of tuples, where each tuple contains two cities and the
              distance between them.
    """

    with open("09.in", "r") as file:
        return [
            (cities[0], cities[1], int(distance))
            for line in file
            if (parts := line.strip().split(" = ")) and len(parts) == 2
            if (cities := parts[0].split(" to ")) and len(cities) == 2
            for distance in [parts[1]]
        ]


def generate_distance_matrix(locations: list[tuple]) -> list[list[int]]:
    """
    Generates a distance matrix from a list of city pair distances.

    The matrix is a 2D list where each element at [i][j] represents the
    distance between the i-th and j-th city in the list of unique cities.

    Args:
        locations (list): A list of tuples where each tuple contains two
                          cities and the distance between them.

    Returns:
        list: A 2D list (matrix) representing the distances between all cities.
    """

    # Extract unique cities and sort them
    cities = sorted({city for c1, c2, _ in locations for city in (c1, c2)})
    city_indices = {city: i for i, city in enumerate(cities)}
    n = len(cities)

    # Initialize the distance matrix with 0s
    dist_matrix = [[0] * n for _ in range(n)]

    # Populate the matrix with distances
    for c1, c2, distance in locations:
        i, j = city_indices[c1], city_indices[c2]
        dist_matrix[i][j] = dist_matrix[j][i] = distance

    return dist_matrix


def part_one(data: list) -> float | int:
    """
    Solves the first part of the puzzle by calculating the minimum possible
    travel distance that visits each city exactly once, using brute force
    (all permutations).

    Args:
        data (list): A list of city pair distances.

    Returns:
        int: The minimum travel distance that visits each city exactly once.
    """

    distances = generate_distance_matrix(data)

    n = len(distances)
    cities = range(n)

    min_dist = float("inf")  # Start with a very large number

    # Generate all permutations of cities
    for perm in itertools.permutations(cities):
        dist = 0
        for i in range(n - 1):
            # Sum the distances for the current permutation
            dist += distances[perm[i]][perm[i + 1]]
        if dist < min_dist:  # Update minimum distance if shorter one is found
            min_dist = dist
    return min_dist


def part_two(data: list) -> float | int:
    """
    Solves the second part of the puzzle by calculating the maximum possible
    travel distance that visits each city exactly once, using brute force
    (all permutations).

    Args:
        data (list): A list of city pair distances.

    Returns:
        int: The maximum travel distance that visits each city exactly once.
    """

    distances = generate_distance_matrix(data)

    n = len(distances)
    cities = range(n)

    max_dist = 0  # Start with a very small number

    # Generate all permutations of cities
    for perm in itertools.permutations(cities):
        dist = 0
        for i in range(n - 1):
            # Sum the distances for the current permutation
            dist += distances[perm[i]][perm[i + 1]]
        if dist > max_dist:  # Update maximum distance if longer one is found
            max_dist = dist
    return max_dist


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 141
    print("Part 2:", part_two(data))  # 736
