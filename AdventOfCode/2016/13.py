#!/usr/bin/env python

from collections import deque


def wall_or_open(coords: tuple, fav_num: int) -> bool:
    """
    Determines if a coordinate is a wall or an open space based on a formula.

    Args:
        coords (tuple): The (x, y) coordinates to check.
        fav_num (int): A favorite number used in the calculation.

    Returns:
        bool: True if the space is open, False if it is a wall.
    """

    x, y = coords

    # Calculate the value using the formula: x² + 3x + 2xy + y + y² + fav_num
    a = ((x * x) + (3 * x) + (2 * x * y) + y + (y * y)) + fav_num

    # Count the number of 1s in the binary representation of `a`
    # If the count is even, it's an open space; otherwise, it's a wall
    return bin(a).count('1') % 2 == 0


def initialize_grid(fav_num: int, size: int) -> list:
    """
    Initializes a grid of a given size, marking walls and open spaces.

    NOTE: 1 is the same as . and 0 is the same as # with AoC grids & Mazes.

    Args:
        fav_num (int): A favorite number used in the wall_or_open calculation.
        size (int): The size of the grid (size x size).

    Returns:
        list: A 2D list representing the grid, where '.' is open and '#' is a
              wall.
    """

    # Create a grid of size x size, filled with 1 (open spaces)
    grid = [[1 for _ in range(size)] for _ in range(size)]

    # Iterate through each cell in the grid
    for x in range(size):
        for y in range(size):
             # If the cell is a wall, mark it with 0
            if not wall_or_open((x, y), fav_num):
                grid[x][y] = 0
    return grid


def bfs(grid, start, finish, max_dist=None):
    """
    Performs a Breadth-First Search (BFS) on the grid to find the shortest path
    or count reachable locations within a maximum distance.

    Args:
        grid (list): The 2D grid representing the maze.
        start (tuple): The starting (x, y) coordinates.
        finish (tuple): The target (x, y) coordinates.
        max_dist (int, optional): The maximum distance to explore. If None,
                                  searches until the finish is found.

    Returns:
        int: The shortest distance to the finish, or the number of reachable
             locations if max_dist is specified.
    """

    rows, cols = len(grid), len(grid[0])  # Get grid dimensions
    # Initialize the BFS queue with the starting position and distance 0
    queue = deque([(start[0], start[1], 0)])
    # Track visited cells to avoid revisiting them
    visited = set()
    visited.add(start)

    # Define the four possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Continue searching while there are cells in the queue
    while queue:
        # Get the next cell from the queue
        x, y, dist = queue.popleft()

        # If we've reached the finish, return the distance
        if (x, y) == finish:
            return dist

        # If a maximum distance is specified and we've reached it, skip further
        # exploration in this branch
        if max_dist is not None and dist >= max_dist:
            continue

        # Explore all four directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # Calculate the new coordinates

            # Check if the new coordinates are within bounds, the cell is open,
            # and it hasn't been visited
            if (0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] and
                    (nx, ny) not in visited):
                # Mark the cell as visited and add it to the queue
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    # If max_dist is specified, return the number of reachable locations
    # Otherwise, return -1 if the finish is unreachable
    return len(visited) if max_dist is not None else -1


def part_one(grid, finish) -> int:
    """
    Solves Part One of the problem by finding the shortest path to the finish.

    Args:
        grid (list): The 2D grid representing the maze.
        finish (tuple): The target (x, y) coordinates.

    Returns:
        int: The shortest distance to the finish.
    """

    # Use BFS to find the shortest path from (1, 1) to the finish
    return bfs(grid, (1, 1), finish)


def part_two(grid, finish) -> int:
    """
    Solves Part Two of the problem by counting the number of locations reachable
    within 50 steps.

    Args:
        grid (list): The 2D grid representing the maze.
        finish (tuple): The target (x, y) coordinates.

    Returns:
        int: The number of reachable locations within 50 steps.
    """

    # Use BFS to count all reachable locations within 50 steps
    return bfs(grid, (1, 1), finish, max_dist=50)


if __name__ == "__main__":
    # Define the favorite number and grid size
    fav_num = 1350
    grid_size = 50
    # Initialize the grid using the favorite number
    grid = initialize_grid(fav_num, grid_size)
    # Define the finish coordinates
    finish = (31, 39)

    # Solve and print the results for Part One and Part Two
    print("Part 1:", part_one(grid, finish))  # 92
    print("Part 2:", part_two(grid, finish))  # 124
