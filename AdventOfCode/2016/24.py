#!/usr/bin/env python

"""
Advent of Code 2016, Day 24: Air Duct Spelunking

This script solves the Day 24 puzzle of Advent of Code 2016. The problem
involves navigating through a grid to collect numbered points in the shortest
number of steps. The solution uses Breadth-First Search (BFS) to compute
distances and permutations to find the optimal path.
"""

from collections import deque
from itertools import permutations


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file.

    Returns:
        list: A list of strings, where each string represents a row in the grid
    """

    with open("24.in", "r") as file:
        return file.read().splitlines()


def parse_grid(grid: list) -> dict:
    """
    Parses the grid to find the positions of all numbered points.

    Args:
        grid (list): A list of strings representing the grid.

    Returns:
        dict: A dictionary mapping point numbers (int) to their
              coordinates (x, y).
    """

    points = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isdigit():
                # Store the coordinates of the numbered point
                points[int(cell)] = (x, y)
    return points


def bfs_distance(grid: list, start: tuple, end: tuple) -> int:
    """
    Computes the shortest distance between two points using Breadth-First
    Search (BFS).

    Args:
        grid (list): A list of strings representing the grid.
        start (tuple): The starting coordinates (x, y).
        end (tuple): The target coordinates (x, y).

    Returns:
        int: The shortest distance between the two points, or -1 if no path
             exists.
    """

    queue = deque([(start, 0)])  # Stores (position, distance)
    visited = set()  # Tracks visited positions to avoid reprocessing

    while queue:
        (x, y), dist = queue.popleft()

        # If the target position is reached, return the distance
        if (x, y) == end:
            return dist

        # Skip if the position has already been visited
        if (x, y) in visited:
            continue

        # Mark the current position as visited
        visited.add((x, y))

        # Explore all 4 possible directions (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds and not a wall
            if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and
                    grid[ny][nx] != '#'):
                # Add the new position to the queue with an incremented
                # distance
                queue.append(((nx, ny), dist + 1))
    # If no path is found, return -1 (should not happen for valid inputs)
    return -1


def compute_pairwise_distances(grid: list, points: dict) -> dict:
    """
    Computes the shortest distances between all pairs of numbered points.

    Args:
        grid (list): A list of strings representing the grid.
        points (dict): A dictionary mapping point numbers to their coordinates.

    Returns:
        dict: A dictionary mapping pairs of points (a, b) to their shortest
              distance.
    """

    distances = {}
    for a in points:
        for b in points:
            if a != b:
                # Compute the shortest distance between points a & b using BFS
                distances[(a, b)] = bfs_distance(grid, points[a], points[b])
    return distances


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle: Finds the shortest path to visit all points
    starting from 0.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: The shortest distance to visit all points.
    """

    # Parse the grid to find the positions of all numbered points
    points = parse_grid(data)
    num_points = len(points)

    # Compute the shortest distances between all pairs of points
    distances = compute_pairwise_distances(data, points)

    # Generate all permutations of the points (excluding the starting point 0)
    points_to_visit = list(range(1, num_points))
    min_distance = float('inf')

    # Try all possible orders of visiting the points
    for perm in permutations(points_to_visit):
        # Start with the distance from point 0 to the first point in the
        # permutation
        current_distance = distances[(0, perm[0])]

        # Add the distances between consecutive points in the permutation
        for i in range(len(perm) - 1):
            current_distance += distances[(perm[i], perm[i + 1])]

        # Update the minimum distance if the current path is shorter
        if current_distance < min_distance:
            min_distance = current_distance

    return int(min_distance)


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle: Finds the shortest path to visit all points
    and return to 0.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: The shortest distance to visit all points and return to the start.
    """

    # Parse the grid to find the positions of all numbered points
    points = parse_grid(data)
    num_points = len(points)

    # Compute the shortest distances between all pairs of points
    distances = compute_pairwise_distances(data, points)

    # Generate all permutations of the points (excluding the starting point 0)
    points = list(range(1, num_points))
    min_distance = float('inf')

    # Try all possible orders of visiting the points
    for perm in permutations(points):
        # Start with the distance from point 0 to the first point in the
        # permutation
        current_distance = distances[(0, perm[0])]

        # Add the distances between consecutive points in the permutation
        for i in range(len(perm) - 1):
            current_distance += distances[(perm[i], perm[i + 1])]

            # Add the distance to return to point 0 from the last point in the
            # permutation
        current_distance += distances[(perm[-1], 0)]  # Return to 0

        # Update the minimum distance if the current path is shorter
        if current_distance < min_distance:
            min_distance = current_distance

    return int(min_distance)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 456
    print("Part 2:", part_two(data))  # 704
