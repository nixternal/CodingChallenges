#!/usr/bin/env python

"""
Advent of Code 2017 - Day 14: Disk Defragmentation
------------------------------------------------

This solution implements a disk defragmentation system that uses the Knot
Hash algorithm to generate a representation of disk usage and analyze
contiguous regions.

Key Algorithms Used:
1. Knot Hash (from Day 10)
   - A complex string hashing algorithm that produces a dense 32-character
     hexadecimal output
   - Involves list manipulation, bit operations (XOR), and hex conversion

2. Flood Fill (used in Part 2)
   - Also known as Seed Fill or Boundary Fill
   - A graph traversal algorithm that determines and labels connected regions
   - Uses Depth-First Search (DFS) for region exploration
   - Time Complexity: O(n), where n is the number of cells
   - Space Complexity: O(n) for the recursion stack

3. Connected Components (conceptual basis for Part 2)
   - Graph theory concept for finding connected subgraphs
   - In this case, used to identify contiguous regions of used disk space
"""


def knot_hash(input_string):
    """
    Implements the Knot Hash algorithm from Day 10.

    Args:
        input_string (str): The input string to hash

    Returns:
        str: A 32-character hexadecimal hash

    Algorithm Steps:
    1. Convert input to ASCII and add standard suffix
    2. Perform 64 rounds of list manipulation
    3. Compute dense hash through XOR operations
    4. Convert to hexadecimal
    """

    # Convert input to ASCII and add standard suffix
    lengths = [ord(c) for c in input_string] + [17, 31, 73, 47, 23]

    # Initialize circular list of numbers 0-255
    numbers = list(range(256))
    current_pos = 0
    skip_size = 0

    # Perform 64 rounds of the knot tying process
    for _ in range(64):
        for length in lengths:
            # Handle list reversal, including wrap-around cases
            if length <= len(numbers):
                end_pos = (current_pos + length) % len(numbers)
                if end_pos > current_pos:
                    numbers[current_pos:end_pos] = reversed(
                                                numbers[current_pos:end_pos])
                else:
                    to_reverse = numbers[current_pos:] + numbers[:end_pos]
                    reversed_portion = list(reversed(to_reverse))
                    numbers[current_pos:] = reversed_portion[:len(
                                                        numbers)-current_pos]
                    numbers[:end_pos] = reversed_portion[len(
                                                        numbers)-current_pos:]

            # Update position and skip size
            current_pos = (current_pos + length + skip_size) % len(numbers)
            skip_size += 1

    # Compute dense hash through XOR operations
    dense_hash = []
    for i in range(0, 256, 16):
        xor_result = 0
        for j in range(16):
            xor_result ^= numbers[i + j]
        dense_hash.append(xor_result)

    # Convert to hexadecimal
    return ''.join([format(x, '02x') for x in dense_hash])


def create_disk_grid(puzzle_input):
    """
    Creates a 128x128 grid representing disk usage.

    Args:
        puzzle_input (str): The puzzle input string

    Returns:
        list: 2D list representing disk grid where '1' represents used squares

    Process:
    1. Generate 128 different knot hashes
    2. Convert each hash to binary
    3. Create grid rows from binary strings
    """

    grid = []
    for row in range(128):
        # Create input string for this row
        row_input = f"{puzzle_input}-{row}"

        # Get knot hash and convert to binary
        hash_result = knot_hash(row_input)
        binary = bin(int(hash_result, 16))[2:].zfill(128)

        # Add row to grid
        grid.append(list(binary))
    return grid


def flood_fill(grid, row, col, visited):
    """
    Implements flood fill algorithm using recursive DFS to mark connected
    regions.

    Args:
        grid (list): 2D list representing the disk grid
        row (int): Current row position
        col (int): Current column position
        visited (set): Set of visited coordinates

    Algorithm:
    - Uses Depth-First Search to explore connected '1' cells
    - Marks visited cells to avoid cycles
    - Checks only orthogonal connections (up, down, left, right)
    """

    # Check bounds and validity of cell
    if (row < 0 or row >= 128 or
        col < 0 or col >= 128 or
        grid[row][col] == '0' or
            (row, col) in visited):
        return

    # Mark current cell as visited
    visited.add((row, col))

    # Recursively check all four adjacent cells
    # This creates a flood fill effect, marking all connected cells
    flood_fill(grid, row + 1, col, visited)  # down
    flood_fill(grid, row - 1, col, visited)  # up
    flood_fill(grid, row, col + 1, visited)  # right
    flood_fill(grid, row, col - 1, visited)  # left


def part_one(data: list) -> int:
    """
    Counts total number of used squares (Part 1).

    Args:
        grid (list): 2D list representing the disk grid

    Returns:
        int: Total number of used squares
    """

    return sum(row.count('1') for row in data)


def part_two(data: list) -> int:
    """
    Counts number of distinct regions (Part 2).

    Args:
        data (list): 2D list representing the disk grid

    Returns:
        int: Number of distinct regions

    Algorithm:
    - Uses flood fill to identify and count connected regions
    - Each unvisited '1' cell represents the start of a new region
    """

    visited = set()
    region_count = 0

    # Iterate through each cell in the grid
    for row in range(128):
        for col in range(128):
            # If we find an unvisited used square, it's a new region
            if data[row][col] == '1' and (row, col) not in visited:
                flood_fill(data, row, col, visited)
                region_count += 1

    return region_count


if __name__ == "__main__":
    data = create_disk_grid("uugsqrei")
    print("Part 1:", part_one(data))  # 8194
    print("Part 2:", part_two(data))  # 1141
