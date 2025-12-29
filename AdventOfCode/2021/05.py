#!/usr/bin/env python
"""
Advent of Code Day 5: Hydrothermal Venture
Counts overlapping points in lines (horizontal, vertical, and diagonal).
"""

from collections import defaultdict


def read_puzzle_input() -> list[str]:
    """Read the puzzle input file and return lines as a list."""
    with open("05.in", "r") as file:
        return file.read().splitlines()


def parse_line(line: str) -> tuple[int, int, int, int]:
    """
    Parse a line coordinate string into start and end points.

    Args:
        line: String in format "x1,y1 -> x2,y2"

    Returns:
        Tuple of (x1, y1, x2, y2) coordinates
    """
    left, right = line.split(" -> ")
    x1, y1 = map(int, left.split(","))
    x2, y2 = map(int, right.split(","))
    return x1, y1, x2, y2


def sign(n: int) -> int:
    """Return the sign of a number (-1, 0, or 1)."""
    return (n > 0) - (n < 0)


def count_overlaps(data: list[str], include_diagonals: bool = False) -> int:
    """
    Count points where at least two lines overlap.

    Args:
        data: List of line coordinate strings
        include_diagonals: Whether to include 45-degree diagonal lines

    Returns:
        Number of points with 2+ overlapping lines
    """
    grid = defaultdict(int)

    for line in data:
        x1, y1, x2, y2 = parse_line(line)

        # Check if line should be processed
        is_horizontal_or_vertical = x1 == x2 or y1 == y2
        is_diagonal = abs(x1 - x2) == abs(y1 - y2)

        if is_horizontal_or_vertical or (include_diagonals and is_diagonal):
            dx = sign(x2 - x1)
            dy = sign(y2 - y1)

            # Walk along the line, marking each point
            x, y = x1, y1
            while True:
                grid[(x, y)] += 1

                if x == x2 and y == y2:
                    break

                x += dx
                y += dy

    # Count points with at least 2 overlaps
    return sum(1 for count in grid.values() if count >= 2)


def part_one(data: list[str]) -> int:
    """Solve part 1: Count overlaps for horizontal and vertical lines only."""
    return count_overlaps(data, include_diagonals=False)


def part_two(data: list[str]) -> int:
    """Solve part 2: Count overlaps including 45-degree diagonal lines."""
    return count_overlaps(data, include_diagonals=True)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 8111
    print("Part 2:", part_two(data))  # 22088
