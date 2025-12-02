#!/usr/bin/env python3
"""Advent of Code 2018 - Day 22: Mode Maze"""

import heapq
from collections import defaultdict
from typing import Tuple

# Terrain types
ROCKY, WET, NARROW = 0, 1, 2

# Tools: neither, torch, climbing gear
NEITHER, TORCH, CLIMBING_GEAR = 0, 1, 2

# Tool compatibility for each terrain type
ALLOWED_TOOLS = {
    ROCKY: {TORCH, CLIMBING_GEAR},
    WET: {NEITHER, CLIMBING_GEAR},
    NARROW: {NEITHER, TORCH},
}


def read_puzzle_input() -> list:
    """Read puzzle input from file."""
    with open("22.in") as f:
        return f.read().splitlines()


def compute_erosion_level(
    x: int, y: int, depth: int, target: Tuple[int, int], cache: dict
) -> int:
    """Compute erosion level for coordinate (x, y) with memoization."""
    if (x, y) in cache:
        return cache[(x, y)]

    # Determine geologic index based on special cases
    if (x, y) == (0, 0) or (x, y) == target:
        geo_index = 0
    elif y == 0:
        geo_index = x * 16807
    elif x == 0:
        geo_index = y * 48271
    else:
        erosion_left = compute_erosion_level(x - 1, y, depth, target, cache)
        erosion_up = compute_erosion_level(x, y - 1, depth, target, cache)
        geo_index = erosion_left * erosion_up

    erosion = (geo_index + depth) % 20183
    cache[(x, y)] = erosion
    return erosion


def get_terrain_type(
    x: int, y: int, depth: int, target: Tuple[int, int], cache: dict
) -> int:
    """Get terrain type (0=rocky, 1=wet, 2=narrow) for coordinate."""
    return compute_erosion_level(x, y, depth, target, cache) % 3


def part_one(data: list) -> int:
    """Calculate total risk level for the rectangular region to target."""
    depth = int(data[0].split(": ")[1])
    tx, ty = map(int, data[1].split(": ")[1].split(","))
    target = (tx, ty)

    erosion_cache = {}
    total_risk = 0

    for y in range(ty + 1):
        for x in range(tx + 1):
            terrain = get_terrain_type(x, y, depth, target, erosion_cache)
            total_risk += terrain

    return total_risk


def part_two(data: list) -> int:
    """Find shortest time to reach target with torch equipped using Dijkstra."""
    depth = int(data[0].split(": ")[1])
    tx, ty = map(int, data[1].split(": ")[1].split(","))
    target = (tx, ty)
    erosion_cache = {}

    # State: (time, x, y, current_tool)
    heap = [(0, 0, 0, TORCH)]
    distances = defaultdict(lambda: float("inf"))
    distances[(0, 0, TORCH)] = 0

    # Search boundary - allow exploring beyond target
    max_coord = max(tx, ty) + 100

    while heap:
        time, x, y, tool = heapq.heappop(heap)

        # Already found a better path to this state
        if time > distances[(x, y, tool)]:
            continue

        # Reached target with torch equipped
        if (x, y) == target and tool == TORCH:
            return time

        current_terrain = get_terrain_type(x, y, depth, target, erosion_cache)

        # Option 1: Switch to a different allowed tool (costs 7 minutes)
        for new_tool in ALLOWED_TOOLS[current_terrain]:
            if new_tool != tool:
                new_time = time + 7
                if new_time < distances[(x, y, new_tool)]:
                    distances[(x, y, new_tool)] = new_time
                    heapq.heappush(heap, (new_time, x, y, new_tool))

        # Option 2: Move to adjacent region (costs 1 minute)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            # Stay within valid bounds
            if nx < 0 or ny < 0 or nx > max_coord or ny > max_coord:
                continue

            neighbor_terrain = get_terrain_type(nx, ny, depth, target, erosion_cache)

            # Can only move if current tool is valid in neighbor terrain
            if tool in ALLOWED_TOOLS[neighbor_terrain]:
                new_time = time + 1
                if new_time < distances[(nx, ny, tool)]:
                    distances[(nx, ny, tool)] = new_time
                    heapq.heappush(heap, (new_time, nx, ny, tool))

    return -1  # Should never reach here


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10603
    print("Part 2:", part_two(data))  # 952
