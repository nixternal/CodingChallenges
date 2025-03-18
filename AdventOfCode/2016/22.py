#!/usr/bin/env python

"""
Solution for Advent of Code 2016 Day 22: Grid Computing.

This module solves a puzzle about data storage nodes in a grid. Each node has a
size, used space, and available space. The puzzle has two parts:
1. Count viable pairs of nodes where data from one could fit in the other
2. Calculate minimum steps to move target data from top-right to top-left

Each node in the grid is represented as a tuple:
    (x, y, size, used, avail, use_percent)

The grid contains special nodes:
    - Empty node (used = 0): Represented as '_' in visualization
    - Wall nodes (used > 100T): Represented as '#' in visualization
    - Goal data (top-right corner): Represented as 'G' in visualization
    - Origin (top-left corner): Represented as 'O' in visualization
"""

import re
from collections import deque


def read_puzzle_input() -> list:
    """
    Parse the input data into a list of node tuples.

    Args:
        input_data: Raw input string containing node information.
            Example line: "/dev/grid/node-x0-y0   10T    8T     2T   80%"

    Returns:
        List of tuples, each containing (x, y, size, used, avail, use_percent)

    Raises:
        ValueError: If a line cannot be parsed using the expected format
    """

    nodes = []
    pattern = r".*-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
    with open("22.in", "r") as file:
        for line in file.read().strip().split('\n'):
            if line.startswith('/dev/grid'):
                match = re.match(pattern, line)
                if match is None:
                    raise ValueError(f"Failed to parse line: {line}")
                x, y, size, used, avail, use_percent = map(int, match.groups())
                nodes.append((x, y, size, used, avail, use_percent))
    return nodes


def is_empty(node):
    """Check if a node is empty (has 0 used space)."""

    return node[3] == 0  # node[3] is the 'used' value


def find_viable_pairs(nodes):
    """
    Find all viable pairs of nodes where data from A could fit in node B.

    A pair is viable if:
    1. Node A is not empty
    2. Nodes A and B are different nodes
    3. Node A's used space would fit in Node B's available space

    Returns:
        List of tuples, each containing (node_a, node_b) representing viable
        pairs
    """

    pairs = []
    for a in nodes:
        if is_empty(a):
            continue
        for b in nodes:
            if a != b and a[3] <= b[4]:  # a.used <= b.avail
                pairs.append((a, b))
    return pairs


def visualize_grid(nodes):
    """
    Create a string visualization of the grid.

    The visualization uses these symbols:
        '_' : Empty node (used = 0)
        '#' : Wall node (used > 100)
        'G' : Goal data (top-right corner)
        'O' : Origin (top-left corner)
        '.' : Normal node

    Returns:
        String representation of the grid
    """

    max_x = max(n[0] for n in nodes)  # n[0] is x
    max_y = max(n[1] for n in nodes)  # n[1] is y
    grid = []

    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            node = next(n for n in nodes if n[0] == x and n[1] == y)
            if is_empty(node):
                row.append('_')
            elif node[3] > 100:  # used > 100
                row.append('#')
            elif x == max_x and y == 0:
                row.append('G')  # Goal data
            elif x == 0 and y == 0:
                row.append('O')  # Origin
            else:
                row.append('.')
        grid.append(''.join(row))

    return '\n'.join(grid)


def find_shortest_path(nodes):
    """
    Find minimum steps needed to move goal data to origin.

    The process happens in two phases:
    1. Move empty node next to goal data
    2. Move goal data to origin by repeatedly:
       - Moving empty node around goal data (4 steps)
       - Moving goal data one step left (1 step)

    Returns:
        Total number of steps required
    """

    max_x = max(n[0] for n in nodes)
    max_y = max(n[1] for n in nodes)

    # Find the empty node
    empty_node = next(n for n in nodes if is_empty(n))
    start_pos = (empty_node[0], empty_node[1])

    # We need to get the empty node next to the goal data at (max_x, 0)
    target_pos = (max_x - 1, 0)  # Position next to the goal data

    # Find wall nodes (nodes with usage > 100T)
    walls = {(n[0], n[1]) for n in nodes if n[3] > 100}

    def get_neighbors(pos):
        """Get valid neighboring positions (not walls, within grid)."""

        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x <= max_x and 0 <= new_y <= max_y and
                    (new_x, new_y) not in walls):
                neighbors.append((new_x, new_y))
        return neighbors

    def bfs(start, target):
        """Find shortest path between two positions using BFS."""

        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            pos, steps = queue.popleft()
            if pos == target:
                return steps

            for next_pos in get_neighbors(pos):
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, steps + 1))

        return float('inf')

    # Calculate total steps:
    # 1. Move empty node next to goal data
    empty_to_goal = bfs(start_pos, target_pos)

    # 2. Moving goal data to (0,0) takes 5 steps per position
    # For each position we need to:
    # - Move empty around goal data (4 steps)
    # - Move goal data one step left (1 step)
    goal_to_origin = 5 * (max_x - 1) + 1

    return empty_to_goal + goal_to_origin


def part_one(data: list) -> int:
    return len(find_viable_pairs(data))


def part_two(data: list) -> int:
    return find_shortest_path(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1043
    print("Part 2:", part_two(data))  # 185
