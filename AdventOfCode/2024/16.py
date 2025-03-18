#!/usr/bin/env python
"""
Pathfinding Puzzle Solution

This script solves a pathfinding puzzle where a starting point ('S') and an
endpoint ('E') are connected through a grid. Each movement on the grid has
associated costs, and the script determines the minimal cost to reach the
endpoint and counts unique states reachable in part two.

Functions:
    - read_puzzle_input: Reads input data from a file.
    - part_one: Computes the minimal cost to reach the endpoint.
    - part_two: Calculates the number of unique grid positions reachable

Usage:
    Run the script directly to solve the puzzle for a given input file.

Requirements:
    - Python 3.x
    - Input file named "16.in" containing the grid layout.
"""

from collections import deque
import heapq


def read_puzzle_input() -> list:
    """
    Read the puzzle input from the file "16.in".

    Returns:
        list: List of strings, where each string represents a row in the grid.
    """

    with open("16.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Calculate minimal cost to reach the endpoint ('E') from the start ('S').

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: Minimal cost to reach the endpoint. Returns 0 if no path exists.
    """

    rows, cols = len(data), len(data[0])

    # Locate the start position ('S')
    sr, sc = next(
        (r, c) for r in range(rows) for c in range(cols) if data[r][c] == "S"
    )

    # Priority queue for BFS (cost, row, col, direction row, direction col)
    pq = [(0, sr, sc, 0, 1)]
    seen = set()

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)

        # Skip already visited states
        if (r, c, dr, dc) in seen:
            continue
        seen.add((r, c, dr, dc))

        # Check if we've reached the end ('E')
        if data[r][c] == "E":
            return cost

        # Generate neighbors
        for new_cost, nr, nc, ndr, ndc in [
            (cost + 1, r + dr, c + dc, dr, dc),    # Move forward
            (cost + 1000, r, c, dc, -dr),          # Turn clockwise
            (cost + 1000, r, c, -dc, dr)           # Turn counter-clockwise
        ]:
            # Ensure the new position is within bounds and not blocked
            if (0 <= nr < rows and 0 <= nc < cols and data[nr][nc] != "#" and
                    (nr, nc, ndr, ndc) not in seen):
                heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    return 0


def part_two(data: list) -> int:
    """
    Calculate the number of unique grid positions reachable in part two.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: Number of unique grid positions (ignoring direction) reachable.
    """

    rows, cols = len(data), len(data[0])

    # Locate the start position ('S')
    sr, sc = next(
        (r, c) for r in range(rows) for c in range(cols) if data[r][c] == "S"
    )

    # Priority queue for BFS (cost, row, col, direction row, direction col)
    pq = [(0, sr, sc, 0, 1)]
    lowest_cost = {(sr, sc, 0, 1): 0}
    backtrack = {}
    best_cost = float("inf")
    end_states = set()

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)

        # Skip if not the lowest cost for this state
        if cost > lowest_cost.get((r, c, dr, dc), float("inf")):
            continue

        # Check if we've reached the end ('E')
        if data[r][c] == "E":
            if cost > best_cost:
                break
            best_cost = cost
            end_states.add((r, c, dr, dc))

        # Explore neighbors
        for new_cost, nr, nc, ndr, ndc in [
            (cost + 1, r + dr, c + dc, dr, dc),    # Move forward
            (cost + 1000, r, c, dc, -dr),          # Turn clockwise
            (cost + 1000, r, c, -dc, dr)           # Turn counter-clockwise
        ]:
            # Check bounds and obstacles
            if not (0 <= nr < rows and 0 <= nc < cols) or data[nr][nc] == "#":
                continue

            # Update the lowest cost and backtrack map
            if new_cost < lowest_cost.get((nr, nc, ndr, ndc), float("inf")):
                lowest_cost[(nr, nc, ndr, ndc)] = new_cost
                backtrack[(nr, nc, ndr, ndc)] = {(r, c, dr, dc)}
                heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))
            elif new_cost == lowest_cost[(nr, nc, ndr, ndc)]:
                backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))

    # Backtrack to find all reachable states
    states = deque(end_states)
    seen = set(end_states)

    while states:
        key = states.popleft()
        for prev in backtrack.get(key, []):
            if prev not in seen:
                seen.add(prev)
                states.append(prev)

    # Count unique grid positions (ignoring direction)
    return len({(r, c) for r, c, _, _ in seen})


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 105496
    print("Part 2:", part_two(data))  # 524
