#!/usr/bin/env python
"""
Advent of Code - Day 17: Reservoir Research
-----------------------------------------

This program simulates water flowing through a slice of underground soil formation
consisting of clay and sand. Water flows from a spring at position (500, 0) and follows
these rules:
1. Water flows downward when possible
2. If blocked, water tries to flow left and right
3. If contained on both sides, water settles
4. Otherwise, water continues to flow over edges

The simulation uses a modified Depth-First Search (DFS) algorithm with a stack to track
the flow of water through the system.

Part 1: Count tiles that can be reached by water (both flowing and settled)
Part 2: Count tiles where water settles permanently
"""

import re
from collections import defaultdict


def read_puzzle_input() -> set:
    """
    Parses the input file containing clay positions.

    Format examples:
    - "x=495, y=2..7" means clay at x=495 for y values 2 through 7
    - "y=7, x=495..501" means clay at y=7 for x values 495 through 501

    Returns:
        set: A set of (x, y) coordinates where clay is present
    """

    clay = set()
    with open("17.in", "r") as file:
        for line in file:
            # Extract all numbers from the line
            nums = list(map(int, re.findall(r"\d+", line)))
            if line.startswith("x"):
                # x is fixed, y varies
                x, y1, y2 = nums
                for y in range(y1, y2 + 1):
                    clay.add((x, y))
            else:
                # y is fixed, x varies
                y, x1, x2 = nums
                for x in range(x1, x2 + 1):
                    clay.add((x, y))
    return clay


def simulate(clay: set):
    """
    Simulates water flowing through the soil formation.

    This function uses a modified Depth-First Search (DFS) algorithm implemented with
    an explicit stack. Water flows downward when possible, and spreads horizontally
    when blocked from below. If water is contained on both sides at a level, it settles
    and becomes stationary.

    Algorithm steps:
    1. Water flows down until hitting clay or settled water
    2. Water spreads horizontally in both directions
    3. If bounded on both sides, water settles
    4. Otherwise, water continues flowing over edges
    5. The process repeats from newly reached positions

    Args:
        clay: A set of (x, y) coordinates where clay is present

    Returns:
        tuple: (grid, min_y, max_y) where grid is a defaultdict mapping positions to
               their contents ('#' for clay, '~' for settled water, '|' for flowing
               water), and min_y/max_y define the vertical bounds of the clay formation
    """

    # Find the vertical bounds of the clay formation
    min_y = min(y for _, y in clay)
    max_y = max(y for _, y in clay)

    # Initialize the grid: '.' for sand, '#' for clay, '|' for flowing water, '~' for
    # settled water
    grid = defaultdict(lambda: ".")
    for x, y in clay:
        grid[(x, y)] = "#"

    # Start DFS from the spring at (500, 0)
    stack = [(500, 0)]
    visited = set()  # Track positions we've already processed

    while stack:
        x, y = stack.pop()

        # Skip already processed positions unless they need to be rechecked
        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Flow downward as far as possible
        while y <= max_y and grid[(x, y + 1)] not in "#~" and grid[(x, y)] != "~":
            grid[(x, y)] = "|"  # Mark as flowing water
            y += 1

        # If water reached the maximum depth, continue to next position
        if y > max_y:
            grid[(x, y)] = "|"
            continue

        # Mark the current position as flowing water if it's not already settled
        if grid[(x, y)] != "~":
            grid[(x, y)] = "|"

        # Try to spread water horizontally at this level
        while True:
            # Check if water can settle at this level (bounded on both sides)
            bounded_left = False
            bounded_right = False

            # Find left boundary - either clay or a point where water can fall
            left_x = x
            while True:
                # Check if blocked by clay on the left
                if grid[(left_x - 1, y)] == "#":
                    bounded_left = True
                    break
                # Check if water can fall through a gap
                if grid[(left_x - 1, y + 1)] not in "#~":
                    # Add this position to the stack to process the falling water
                    if (left_x - 1, y) not in visited:
                        stack.append((left_x - 1, y))
                        grid[(left_x - 1, y)] = "|"
                    break
                # Continue expanding left
                left_x -= 1
                grid[(left_x, y)] = "|"

            # Find right boundary - either clay or a point where water can fall
            right_x = x
            while True:
                # Check if blocked by clay on the right
                if grid[(right_x + 1, y)] == "#":
                    bounded_right = True
                    break
                # Check if water can fall through a gap
                if grid[(right_x + 1, y + 1)] not in "#~":
                    # Add this position to the stack to process the falling water
                    if (right_x + 1, y) not in visited:
                        stack.append((right_x + 1, y))
                        grid[(right_x + 1, y)] = "|"
                    break
                # Continue expanding right
                right_x += 1
                grid[(right_x, y)] = "|"

            # If bounded on both sides, convert flowing water to settled water
            if bounded_left and bounded_right:
                for fill_x in range(left_x, right_x + 1):
                    grid[(fill_x, y)] = "~"
                # Move up one level to check if water can settle there too
                y -= 1
                # Skip if at the very top or above the clay formation
                if y < min_y:
                    break
                # Reset this position as unvisited so we can check it again
                visited.discard((x, y))
                stack.append((x, y))
                break
            else:
                # Not bounded on both sides, continue to next position in stack
                break

    return grid, min_y, max_y


def part_one(data: set) -> int:
    """
    Count tiles that can be reached by water (both flowing and settled)
    within the vertical bounds of the clay formation.

    Args:
        data: A set of (x, y) coordinates where clay is present

    Returns:
        int: Number of tiles that can be reached by water
    """

    grid, min_y, max_y = simulate(data)
    return sum(
        1 for (_, y), val in grid.items() if val in ("|", "~") and min_y <= y <= max_y
    )


def part_two(data: set) -> int:
    """
    Count tiles where water settles permanently within the vertical bounds
    of the clay formation.

    Args:
        data: A set of (x, y) coordinates where clay is present

    Returns:
        int: Number of tiles where water settles permanently
    """

    grid, min_y, max_y = simulate(data)
    return sum(1 for (_, y), val in grid.items() if val == "~" and min_y <= y <= max_y)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 26910
    print("Part 2:", part_two(data))  # 22182
