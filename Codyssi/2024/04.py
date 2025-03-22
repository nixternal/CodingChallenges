#!/usr/bin/env python

from collections import deque, defaultdict


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named "04.in" and returns a list of
    strings, each representing a connection between two locations.
    """

    with open("04.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Determines the number of unique locations in the given input data.

    Args:
        data (list): A list of strings representing location connections.

    Returns:
        int: The number of unique locations.
    """

    return len(set(loc for line in data for loc in line.split(' <-> ')))


def build_graph(data: list) -> dict:
    """
    Constructs an adjacency list representation of the graph from input data.

    Args:
        data (list): A list of strings representing location connections.

    Returns:
        dict: An adjacency list representation of the graph.
    """

    graph = defaultdict(list)
    for line in data:
        loc1, loc2 = line.split(' <-> ')
        graph[loc1].append(loc2)
        graph[loc2].append(loc1)
    return graph


def part_two(data: list) -> int:
    """
    Determines the number of reachable locations within a maximum of 3 hours.

    Args:
        data (list): A list of strings representing location connections.

    Returns:
        int: The count of reachable locations within 3 hours.
    """

    start = 'STT'
    max_hours = 3
    graph = build_graph(data)

    if start not in graph:
        return 0

    visited = {start: 0}  # Tracks shortest distance to each location
    queue = deque([(start, 0)])  # (location, distance)

    while queue:
        current, distance = queue.popleft()

        if distance >= max_hours:
            continue

        for neighbor in graph[current]:
            if neighbor not in visited or distance + 1 < visited[neighbor]:
                visited[neighbor] = distance + 1
                queue.append((neighbor, distance + 1))

    return len(visited)


def part_three(data: list) -> int:
    """
    Calculates the total travel time for all vehicles to reach their
    destinations.

    Args:
        data (list): A list of strings representing location connections.

    Returns:
        int: The total time spent traveling.
    """

    start = 'STT'
    graph = build_graph(data)

    total_time = 0
    queue = deque([(start, 0)])
    visited = set()

    while queue:
        node, time = queue.popleft()

        if node in visited:
            continue
        visited.add(node)
        total_time += time

        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, time + 1))

    return total_time


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 49
    print("Part 2:", part_two(data))    # 24
    print("Part 3:", part_three(data))  # 178
