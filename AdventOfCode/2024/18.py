#!/usr/bin/env python
"""
Breadth-First Search - BFS
"""

from collections import deque


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from the file "18.in" located in the current
    directory.

    Returns:
        list: A list of strings, where each string represents a line in the
              input file.
    """

    with open("18.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Solves the first part of the puzzle by finding the shortest path from the
    top-left corner (0, 0) to the bottom-right corner (s, s) on a grid,
    avoiding obstacles.

    Args:
        data (list): A list of strings, each representing a coordinate pair in
                     the format "x,y".

    Returns:
        int: The shortest path distance from (0, 0) to (s, s), or 0 if no path
             exists.
    """

    s = 70    # Size of the grid (side length)
    n = 1024  # Number or coordinates (bytes) to consider for obstacles

    # Initialize a (s+1)x(s+1) grid with all cells set to 0 (empty)
    grid = [[0] * (s + 1) for _ in range(s + 1)]

    # Parse the first `n` coordinate pairs & mark them as obstacles on the grid
    coords = {tuple(map(int, line.split(','))) for line in data[:n]}
    for c, r in coords:
        grid[r][c] = 1

    # BFS initialization: start from (0, 0) with distance 0
    Q = deque([(0, 0, 0)])  # Each element in Q is a tuple (row, col, distance)
    seen = {(0, 0)}  # Set of visited cells to prevent revisiting

    # Perform BFS
    while Q:
        r, c, d = Q.popleft()  # Dequeue the current cell
        # Explore the 4 possible directions (up, down, left, right)
        for nr, nc in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
            # Skip out-of-bounds or already visited cells
            if 0 <= nr <= s and 0 <= nc <= s and (nr, nc) not in seen:
                if grid[nr][nc] == 0:  # Process only empty cells
                    if (nr, nc) == (s, s):  # Reached the bottom-right corner
                        return d + 1  # Return the path length
                    seen.add((nr, nc))  # Mark cell as visited
                    Q.append((nr, nc, d + 1))  # Enqueue cell incremented dist

    return 0  # Return 0 if no path exists


def part_two(data: list) -> str:
    """
    Solves the second part of the puzzle by finding the last obstacle
    coordinate such that removing it results in the grid being connected
    from (0, 0) to (s, s).

    Args:
        data (list): A list of strings, each representing a coordinate pair in
                     the format "x,y".

    Returns:
        str: The last coordinate in the format "x,y" that maintains
             connectivity.
    """

    s = 70  # Size of the grid (side length)

    # Parse all coordinates into a list of tuples
    coords = [tuple(map(int, line.split(','))) for line in data]

    def is_connected(n):
        """
        Checks if the grid is connected from (0, 0) to (s, s) with the first
        `n` coordinates considered as obstacles.

        Args:
            n (int): Number of coordinates to consider as obstacles.

        Returns:
            bool: True if the grid is connected, False otherwise.
        """

        # Initialize grid with obstacles marked
        grid = [[0] * (s + 1) for _ in range(s + 1)]
        for c, r in coords[:n]:
            grid[r][c] = 1

        # BFS to check connectivity
        Q = deque([(0, 0)])  # Start BFS from (0, 0)
        seen = {(0, 0)}  # Set of visited cells

        while Q:
            r, c = Q.popleft()  # Dequeue the current cell
        # Explore the 4 possible directions (up, down, left, right)
            for nr, nc in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
                # Skip out-of-bounds or already visited cells
                if 0 <= nr <= s and 0 <= nc <= s and (nr, nc) not in seen:
                    if grid[nr][nc] == 0:  # Process only empty cells
                        if (nr, nc) == (s, s):  # Reached bottom-right corner
                            return True
                        seen.add((nr, nc))  # Mark cell as visited
                        Q.append((nr, nc))  # Enqueue the cell

        return False  # Return False if (s, s) is unreachable

    # Binary search to find the last `n` where the grid is still connected
    low, high = 0, len(coords) - 1
    while low < high:
        mid = (low + high) // 2  # Compute the midpoint
        if is_connected(mid + 1):  # Check connectivity w/ `mid + 1` obstacles
            low = mid + 1  # If connected, search the upper half
        else:
            high = mid  # If not connected, search the lower half

    # Return the last coordinate as a string "x,y"
    return ','.join(map(str, coords[low]))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 296
    print("Part 2:", part_two(data))  # 28,44
