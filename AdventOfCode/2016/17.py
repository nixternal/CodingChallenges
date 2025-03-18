#!/usr/bin/env python

import hashlib
from collections import deque


def get_moves(passcode, path, x, y):
    """
    Determines the possible moves from the current position based on the
    passcode and path.

    Args:
        passcode (str): The initial passcode provided in the puzzle.
        path (str): The sequence of moves taken so far (e.g., "UDLR").
        x (int): The current x-coordinate in the grid.
        y (int): The current y-coordinate in the grid.

    Returns:
        list: List of tuples representing possible moves. Each tuple contains:
              - The direction of the move ('U', 'D', 'L', 'R').
              - The new x-coordinate after the move.
              - The new y-coordinate after the move.
    """

    # Compute the MD5 hash of the passcode concatenated with the current path
    hash_input = passcode + path
    hash_result = hashlib.md5(hash_input.encode()).hexdigest()[:4]

    moves = []
    # Check each of the first four characters of hash to determine valid moves
    # Up (U)
    if y > 0 and hash_result[0] in 'bcdef':
        moves.append(('U', x, y - 1))
    # Down (D)
    if y < 3 and hash_result[1] in 'bcdef':
        moves.append(('D', x, y + 1))
    # Left (L)
    if x > 0 and hash_result[2] in 'bcdef':
        moves.append(('L', x - 1, y))
    # Right (R)
    if x < 3 and hash_result[3] in 'bcdef':
        moves.append(('R', x + 1, y))
    return moves


def find_paths(passcode):
    """
    Finds the shortest and longest paths from the top-left corner (0, 0) to
    the bottom-right corner (3, 3) of a 4x4 grid, using a Breadth-First
    Search (BFS) approach.

    Args:
        passcode (str): The initial passcode provided in the puzzle.

    Returns:
        tuple: A tuple containing:
               - The shortest path as a string (e.g., "DDRR").
               - The length of the longest path as an integer.
    """

    # Initialize a queue for BFS, starting at position (0, 0) w/ an empty path
    queue = deque()
    queue.append(('', 0, 0))  # (path, x, y)

    shortest_path = None     # Stores the shortest path to the target
    longest_path_length = 0  # Stores the length of longest path to the target

    while queue:
        # Dequeue the next path and position to explore
        path, x, y = queue.popleft()

        # Check if the current position is the target (3, 3)
        if x == 3 and y == 3:
            # If this is the first time reaching the target, store it as the
            # shortest path
            if not shortest_path:
                shortest_path = path
            # Update the longest path length if this path is longer
            longest_path_length = max(longest_path_length, len(path))
            continue  # Skip further exploration from this position

        # Explore all valid moves from the current position
        for move, new_x, new_y in get_moves(passcode, path, x, y):
            # Enqueue the new path and position
            queue.append((path + move, new_x, new_y))

    return shortest_path, longest_path_length


def part_one(passcode: str):
    return find_paths(passcode)[0]


def part_two(passcode: str) -> int:
    return find_paths(passcode)[1]


if __name__ == "__main__":
    print("Part 1:", part_one('dmypynyp'))  # RDRDUDLRDR
    print("Part 2:", part_two('dmypynyp'))  # 386
