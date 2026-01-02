#!/usr/bin/env python

from collections import defaultdict
from math import atan2, gcd, pi


def read_puzzle_input() -> list:
    with open("10.in", "r") as file:
        return file.read().splitlines()


def parse_asteroids(data: list) -> list:
    """Parse the map and return list of asteroid coordinates."""
    asteroids = []
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                asteroids.append((x, y))
    return asteroids


def get_direction(from_pos: list, to_pos: list) -> tuple:
    """
    Get the reduced direction vector from from_pos to to_pos.
    This represents the unique line of sight direction.
    """
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]

    # Reduce the direction by the GCD to get the fundamental direction
    g = gcd(abs(dx), abs(dy))
    return (dx // g, dy // g)


def count_visible(station: list, asteroids: list) -> int:
    """
    Count how many asteroids are visible from the station.
    Asteroids are visible if no other asteroid blocks the line of sight.
    """
    # Use a set to track unique directions
    directions = set()

    for asteroid in asteroids:
        if asteroid == station:
            continue

        direction = get_direction(station, asteroid)
        directions.add(direction)

    return len(directions)


def part_one(data: list) -> int:
    asteroids = parse_asteroids(data)

    max_visible = 0

    for asteroid in asteroids:
        visible = count_visible(asteroid, asteroids)
        if visible > max_visible:
            max_visible = visible

    return max_visible


def part_two(data: list) -> int:
    asteroids = parse_asteroids(data)

    # Find the best station location from part 1
    max_visible = 0
    station = []

    for asteroid in asteroids:
        visible = count_visible(asteroid, asteroids)
        if visible > max_visible:
            max_visible = visible
            station = asteroid

    # Group asteroids by their angle from the station
    # and sort by distance within each angle
    angle_groups = defaultdict(list)

    for asteroid in asteroids:
        if asteroid == station:
            continue

        dx = asteroid[0] - station[0]
        dy = asteroid[1] - station[1]

        # Calculate angle starting from up (negative y) going clockwise
        # atan2 returns angle from positive x-axis, counter-clockwise
        # We want angle from negative y-axis, clockwise
        angle = atan2(dx, -dy)

        # Normalize to [0, 2π) range
        if angle < 0:
            angle += 2 * pi

        # Calculate distance
        distance = (
            dx * dx + dy * dy
        )  # No need for sqrt, we just need relative distances

        angle_groups[angle].append((distance, asteroid))

    # Sort each group by distance (closest first)
    for angle in angle_groups:
        angle_groups[angle].sort()

    # Get sorted list of angles (clockwise from up)
    sorted_angles = sorted(angle_groups.keys())

    # Vaporize asteroids
    vaporized = []
    angle_idx = 0

    while len(vaporized) < 200 and angle_groups:
        angle = sorted_angles[angle_idx % len(sorted_angles)]

        if angle in angle_groups and angle_groups[angle]:
            # Vaporize the closest asteroid at this angle
            distance, asteroid = angle_groups[angle].pop(0)
            vaporized.append(asteroid)

            # Remove this angle if no more asteroids in that direction
            if not angle_groups[angle]:
                del angle_groups[angle]
                sorted_angles.remove(angle)
                # Don't increment angle_idx since we removed an element
                continue

        angle_idx += 1

    if len(vaporized) >= 200:
        asteroid_200 = vaporized[199]  # 0-indexed
        return asteroid_200[0] * 100 + asteroid_200[1]

    return -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 299
    print("Part 2:", part_two(data))  # 1419
