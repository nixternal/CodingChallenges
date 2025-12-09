#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("09.in", "r") as file:
        return file.read().splitlines()


def parse_tiles(data: list) -> list:
    """Parse input data into list of coordinate tuples."""
    return [tuple(map(int, line.split(","))) for line in data]


def get_polygon_edges(
    tiles: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    Convert list of vertices into a list of edges ((x1, y1), (x2, y2)).
    """
    edges = []
    n = len(tiles)
    for i in range(n):
        p1 = tiles[i]
        p2 = tiles[(i + 1) % n]
        edges.append((p1, p2))
    return edges


def is_rectangle_valid(x1: int, y1: int, x2: int, y2: int, edges: list) -> bool:
    """
    Geometric check to see if a rectangle formed by (x1, y1) and (x2, y2)
    is strictly inside or on the boundary of the polygon defined by 'edges'.
    """
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # 1. Intersection Check:
    # The rectangle is invalid if any polygon edge passes *strictly through* it.
    # Edges aligned with the rectangle boundary are allowed.
    for (ex1, ey1), (ex2, ey2) in edges:
        if ex1 == ex2:  # Vertical polygon edge
            # Check if this vertical edge is strictly between rect x-bounds
            if min_x < ex1 < max_x:
                # Check for y-overlap
                e_ymin, e_ymax = min(ey1, ey2), max(ey1, ey2)
                # Overlap if max(start1, start2) < min(end1, end2)
                if max(min_y, e_ymin) < min(max_y, e_ymax):
                    return False
        else:  # Horizontal polygon edge
            # Check if this horizontal edge is strictly between rect y-bounds
            if min_y < ey1 < max_y:
                # Check for x-overlap
                e_xmin, e_xmax = min(ex1, ex2), max(ex1, ex2)
                if max(min_x, e_xmin) < min(max_x, e_xmax):
                    return False

    # 2. Inclusion Check:
    # If no edges intersect, the rectangle is either fully inside or fully outside.
    # Check a test point in the center of the rectangle (min_x + 0.5, min_y + 0.5)
    # using Ray Casting.
    test_x = min_x + 0.5
    test_y = min_y + 0.5

    inside = False
    for (ex1, ey1), (ex2, ey2) in edges:
        # We only care about vertical edges for horizontal ray casting
        # (or horizontal edges for vertical ray casting).
        # Let's use vertical edges and a ray casting to the right (+x).

        if ex1 == ex2:  # Vertical edge
            e_ymin, e_ymax = min(ey1, ey2), max(ey1, ey2)
            # Does the edge span the test y?
            if e_ymin <= test_y <= e_ymax:
                # Is the edge to the right of the test point?
                if ex1 > test_x:
                    inside = not inside

    return inside


def part_one(data: list) -> int:
    """
    Find the largest rectangle that can be formed using red tiles
    as opposite corners.
    """
    tiles = parse_tiles(data)
    max_area = 0

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            if x1 != x2 and y1 != y2:
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)

    return max_area


def part_two(data: list) -> int:
    """
    Find the largest rectangle using only red and green tiles.
    Optimized to use Geometric checks instead of Grid Rasterization.
    """
    tiles = parse_tiles(data)
    edges = get_polygon_edges(tiles)

    max_area = 0

    # Try every pair of red tiles as opposite corners
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # Only form a rectangle if corners are different in both dimensions
            if x1 != x2 and y1 != y2:
                # Calculate area first
                current_area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

                # Optimization: Only check validity if this area is bigger than what we found
                if current_area > max_area:
                    if is_rectangle_valid(x1, y1, x2, y2, edges):
                        max_area = current_area

    return max_area


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 4763040296
    print("Part 2:", part_two(data))  # 1396494456
