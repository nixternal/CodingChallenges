#!/usr/bin/env python

from collections import deque


def read_puzzle_input() -> list:
    with open("12.in", "r") as file:
        return file.read().splitlines()


def get_regions(data: list) -> list:
    """
    Identifies and groups connected regions of the same "crop" in a 2D grid.

    Args:
        data (list): A 2D list of characters representing the grid.

    Returns:
        list: A list of sets, where each set contains the coordinates of cells
        that belong to the same region.
    """

    rows, cols = len(data), len(data[0])
    regions = []  # List to store all identified regions
    seen = set()  # Set to keep track of visited cells/plots

    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue

            crop = data[r][c]
            region = set()  # Set to store the current region's cells/plots
            Q = deque([(r, c)])  # Queue for Breadth-first search (aka BFS)

            while Q:
                cr, cc = Q.popleft()
                if (cr, cc) in seen:
                    continue

                seen.add((cr, cc))
                region.add((cr, cc))

                # Check all neighbors (up, down, left, right)
                for nr, nc in [(cr - 1, cc), (cr + 1, cc),
                               (cr, cc - 1), (cr, cc + 1)]:
                    if (0 <= nr < rows and 0 <= nc < cols and
                            (nr, nc) not in seen and data[nr][nc] == crop):
                        Q.append((nr, nc))

            regions.append(region)

    return regions


def calculate_perimeter(region) -> int:
    """
    Calculates the perimeter of a region based on its boundary cells.

    Args:
        region (set): A set of tuples representing the coordinates of the
                      cells in the region.

    Returns:
        int: The total perimeter of the region.
    """

    perimeter = 0
    # Relative positions of neighbors
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for r, c in region:
        for dr, dc in neighbors:
            # If a neighboring cell is outside the region, it contributes to
            # the perimeter
            if (r + dr, c + dc) not in region:
                # Count edges that are not shared w/ another cell in the region
                perimeter += 1
    return perimeter


def calculate_sides(region) -> int:
    """
    Calculates the number of unique connected edges (sides) that form the
    boundary of a region.

    Args:
        region (set): A set of tuples representing the coordinates of the
                      cells in the region.

    Returns:
        int: The number of unique sides in the region's boundary.
    """

    edges = {}  # Dictionary to store edges w/ their directions
    for r, c in region:
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (nr, nc) in region:
                continue
            # Midpoint and direction of the edge
            er = (r + nr) / 2
            ec = (c + nc) / 2
            edges[(er, ec)] = (er - r, ec - c)  # Edge midpoint and direction

    # Track visited edges
    seen = set()  # Set to keep track of visited edges
    sides = 0

    # Traverse and count unique edges
    for edge, direction in edges.items():
        if edge in seen:
            continue
        sides += 1
        queue = [edge]

        # Use Breadth-first search (BFS) to traverse connected edges in the
        # same direction
        while queue:
            er, ec = queue.pop()
            if (er, ec) in seen:
                continue
            seen.add((er, ec))

            # Check neighboring edges based on orientation
            if er % 1 == 0:  # Vertical edge
                for dr in [-1, 1]:
                    neighbor = (er + dr, ec)
                    if (edges.get(neighbor) == direction and
                            neighbor not in seen):
                        queue.append(neighbor)
            else:  # Horizontal edge
                for dc in [-1, 1]:
                    neighbor = (er, ec + dc)
                    if (edges.get(neighbor) == direction and
                            neighbor not in seen):
                        queue.append(neighbor)

    return sides


def part_one(data: list) -> int:
    regions = get_regions(data)
    return sum(len(region) * calculate_perimeter(region) for region in regions)


def part_two(data: list) -> int:
    regions = get_regions(data)
    return sum(len(region) * calculate_sides(region) for region in regions)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1431440
    print("Part 2:", part_two(data))  # 869070
