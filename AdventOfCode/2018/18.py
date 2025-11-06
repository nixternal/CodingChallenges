#!/usr/bin/env python
"""
Advent of Code 2018 - Day 18: Settlers of The North Pole
Simulates a cellular automaton representing lumber collection area changes.

Rules:
- Open ground (.) becomes trees (|) if 3+ adjacent acres contain trees
- Trees (|) become lumberyard (#) if 3+ adjacent acres are lumberyards
- Lumberyard (#) becomes open (.) unless adjacent to both lumberyard and trees
"""


def read_puzzle_input() -> list[list[str]]:
    """Read the grid from input file."""

    with open("18.in", "r") as file:
        return [list(line.strip()) for line in file]


def neighbors(x: int, y: int, grid: list[list[str]]) -> dict[str, int]:
    """Count the number of each terrain type in the 8 adjacent cells."""

    h, w = len(grid), len(grid[0])
    counts = {".": 0, "|": 0, "#": 0}

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                counts[grid[ny][nx]] += 1

    return counts


def step(grid: list[list[str]]) -> list[list[str]]:
    """Perform one minute of simulation according to the transformation rules."""

    h, w = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]

    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            n = neighbors(x, y, grid)

            if cell == "." and n["|"] >= 3:
                new_grid[y][x] = "|"
            elif cell == "|" and n["#"] >= 3:
                new_grid[y][x] = "#"
            elif cell == "#" and (n["#"] == 0 or n["|"] == 0):
                new_grid[y][x] = "."

    return new_grid


def grid_to_key(grid: list[list[str]]) -> tuple:
    """Convert grid to hashable tuple for cycle detection."""

    return tuple(tuple(row) for row in grid)


def resource_value(grid: list[list[str]]) -> int:
    """Calculate resource value: (# of trees) * (# of lumberyards)."""

    trees = sum(row.count("|") for row in grid)
    yards = sum(row.count("#") for row in grid)
    return trees * yards


def part_one(data: list[list[str]]) -> int:
    """Run simulation for 10 minutes and return resource value."""

    grid = [row[:] for row in data]  # Copy to avoid mutating input
    for _ in range(10):
        grid = step(grid)
    return resource_value(grid)


def part_two(data: list[list[str]]) -> int:
    """
    Alternative implementation that stores values during cycle detection.
    Slightly faster as it avoids re-simulation.
    """

    grid = [row[:] for row in data]
    seen = {}
    values = []
    minute = 0

    while True:
        key = grid_to_key(grid)

        if key in seen:
            cycle_start = seen[key]
            cycle_length = minute - cycle_start
            # Calculate position in cycle at target minute
            target_offset = (1_000_000_000 - cycle_start) % cycle_length
            return values[cycle_start + target_offset]

        seen[key] = minute
        values.append(resource_value(grid))
        grid = step(grid)
        minute += 1


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 653184
    print("Part 2:", part_two(data))  # 169106
