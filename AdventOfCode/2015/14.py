#!/usr/bin/env python

"""
This script solves a puzzle involving racing reindeer, calculating the maximum distance
covered by a reindeer in a given time (Part 1) and determining the most points
scored by a reindeer in the same time period (Part 2).
"""

import re


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '14.in' and returns a list of
    strings, where each string represents one line from the input file.

    Returns:
        list: A list of strings, each containing a reindeer's description.
    """

    with open("14.in", "r") as file:
        return file.read().splitlines()


def create_reindeer_list(data: list) -> list:
    """
    Parses the input data to extract reindeer properties and returns a list of
    tuples, where each tuple represents a reindeer and its attributes.

    Args:
        data (list): List of strings, each containing a reindeer's description.

    Returns:
        list: List of tuples formatted (name, speed, travel_time, rest_time).
              - name (str): Reindeer's name.
              - speed (int): Distance covered per second during active travel.
              - travel_time (int): Time (in seconds) the reindeer can travel
                                   before resting.
              - rest_time (int): Time (in seconds) the reindeer needs to rest.
    """

    regex = r"(\w+).+?(\d+).+?(\d+).+?(\d+)"
    reindeer = []
    for line in data:
        # Extract name, speed, travel time, and rest time from the input using
        # regex
        name, dist, t1, t2 = re.findall(regex, line)[0]
        # Convert numeric values to integers and append to the list
        reindeer.append((name, int(dist), int(t1), int(t2)))
    return reindeer


def part_one(data: list) -> int:
    """
    Calculates the maximum distance covered by any reindeer in 2503 seconds.

    Args:
        data (list): A list of strings, each containing a reindeer's
                     description.

    Returns:
        int: The maximum distance traveled by a single reindeer.
    """

    reindeer = create_reindeer_list(data)
    total_time = 2503  # Race duration in seconds
    max_distance = 0   # Tracks the maximum distance covered by any reindeer
    for deer in reindeer:
        _, speed, travel_time, rest_time = deer
        # Calculate the number of complete cycles (travel + rest) and the
        # remaining time
        q, r = divmod(total_time, travel_time + rest_time)
        # Total distance is distance in complete cycles + distance in the
        # remaining time
        distance = (q * travel_time + min(r, travel_time)) * speed
        # Update maximum distance if the current reindeer covers more distance
        if distance > max_distance:
            max_distance = distance
    return max_distance


def part_two(data: list) -> int:
    """
    Determines the highest points scored by a reindeer in a 2503-second race.
    Points are awarded to the leading reindeer at each second.

    Args:
        data (list): List of strings, each containing a reindeer's description.

    Returns:
        int: The maximum points scored by any single reindeer.
    """

    reindeer = create_reindeer_list(data)

    # Tracks distances covered by each reindeer
    total_distances = [0 for _ in range(len(reindeer))]
    # Tracks points scored by each reindeer
    points = [0 for _ in range(len(reindeer))]
    total_time = 2503  # The race duration in seconds

    # Simulate the race second-by-second
    for sec in range(total_time):
        for i in range(len(reindeer)):
            # Determine if the reindeer is actively traveling at the current
            # second
            if ((sec % (reindeer[i][2] + reindeer[i][3])) < reindeer[i][2]):
                total_distances[i] += reindeer[i][1]

        # Award points to the reindeer(s) with the maximum distance at the
        # current second
        max_distance = max(total_distances)
        for i, distance in enumerate(total_distances):
            if distance == max_distance:
                points[i] += 1

    return max(points)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2655
    print("Part 2:", part_two(data))  # 1059
