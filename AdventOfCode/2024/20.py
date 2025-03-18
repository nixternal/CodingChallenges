#!/usr/bin/env python

"""
Breadth First Search - BFS

This script provides solutions for both parts of the puzzle by reading input
data from a file and performing grid-based calculations to solve the
respective problems.
"""


def read_puzzle_input() -> list[str]:
    """
    Reads the puzzle input from a file named '20.in' and returns it as a list
    of strings.

    Returns:
        List[str]: A list of strings representing the puzzle input lines.
    """

    with open("20.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list[str]) -> int:
    """
    Solves Part 1 of the puzzle.

    It calculates the number of grid cells satisfying specific conditions based
    on distances from the start ('S') to the end ('E') while avoiding obstacles
    ('#').

    Args:
        data (list[str]): The puzzle input as a grid of characters.

    Returns:
        int: The count of cells meeting the condition.
    """

    rows = len(data)
    cols = len(data[0])
    r = c = 0

    # Locate the starting point 'S'
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == 'S':
                break
        else:
            continue
        break

    # Initialize distance map
    dists = [[-1] * cols for _ in range(rows)]
    dists[r][c] = 0

    # Breadth-First Search (BFS) like traversal to calculate distances
    while data[r][c] != 'E':
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:  # Out-of-bounds
                continue
            if data[nr][nc] == '#':  # Obstacle
                continue
            if dists[nr][nc] != -1:  # Already visited
                continue
            dists[nr][nc] = dists[r][c] + 1
            r = nr
            c = nc

    count = 0

    # Evaluate conditions for each cell
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == '#':  # Skip obstacles
                continue
            for nr, nc in [
                    (r + 2, c), (r + 1, c + 1), (r, c + 2), (r - 1, c + 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols:  # O-o-b
                    continue
                if data[nr][nc] == '#':  # Obstacle
                    continue
                # Check distance between difference condition. 100 picosecond
                # total time + a 2 picosecond cheat time
                if abs(dists[r][c] - dists[nr][nc]) >= 102:
                    count += 1
    return count


def part_two(data: list[str]) -> int:
    """
    Solves Part 2 of the puzzle.

    It calculates the number of grid cells satisfying more complex conditions
    based on distances from the start ('S') to the end ('E') while avoiding
    obstacles ('#').

    Args:
        data (list[str]): The puzzle input as a grid of characters.

    Returns:
        int: The count of cells meeting the condition.
    """

    rows = len(data)
    cols = len(data[0])
    r = c = 0

    # Locate starting point 'S'
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == 'S':
                break
        else:
            continue
        break

    # Initialize distance map
    dists = [[-1] * cols for _ in range(rows)]
    dists[r][c] = 0

    # BFS-like traversal to calculate distances
    while data[r][c] != 'E':
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:  # Out-of-bounds
                continue
            if data[nr][nc] == '#':  # Obstacle
                continue
            if dists[nr][nc] != -1:  # Already visited
                continue
            dists[nr][nc] = dists[r][c] + 1
            r = nr
            c = nc

    count = 0

    # Evaluate conditions for each cell and radius
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == '#':  # Skip obstacles
                continue
            for radius in range(2, 21):
                for dr in range(radius + 1):
                    dc = radius - dr
                    for nr, nc in {
                            (r + dr, c + dc), (r + dr, c - dc),
                            (r - dr, c + dc), (r - dr, c - dc)}:
                        if nr < 0 or nc < 0 or nr >= rows or nc >= cols:  # OOB
                            continue
                        if data[nr][nc] == '#':  # Obstacle
                            continue
                        # Check distance difference. 100 picosecond total time
                        # + the extra picoseconds of cheat time
                        if dists[r][c] - dists[nr][nc] >= 100 + radius:
                            count += 1
    return count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1263
    print("Part 2:", part_two(data))  # 957831
