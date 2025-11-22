#!/usr/bin/env python

import heapq
import re
from bisect import bisect_left, bisect_right


def read_puzzle_input() -> list:
    with open("15.in", "r") as file:
        return file.read().split("\n\n")


# Direction constants as (x, y) tuples
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ORIGIN = (0, 0)


def clockwise(direction: tuple) -> tuple:
    """Rotate a direction 90 degrees clockwise."""
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    else:  # LEFT
        return UP


def counter_clockwise(direction: tuple) -> tuple:
    """Rotate a direction 90 degrees counter-clockwise."""
    if direction == UP:
        return LEFT
    elif direction == LEFT:
        return DOWN
    elif direction == DOWN:
        return RIGHT
    else:  # RIGHT
        return UP


def manhattan(p1: tuple, p2: tuple) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def minmax(a: int, b: int) -> tuple[int, int]:
    """Return (minimum, maximum) of two values."""
    return (min(a, b), max(a, b))


def can_move(walls: list, from_point: tuple, to_point: tuple) -> bool:
    """
    Check if movement between two points is valid (doesn't intersect walls).

    Creates a bounding box for the movement and checks if it overlaps with
    any wall rectangles using rectangle intersection logic.
    """
    x1, x2 = minmax(from_point[0], to_point[0])
    y1, y2 = minmax(from_point[1], to_point[1])

    for x3, x4, y3, y4 in walls:
        # Check if rectangles overlap - if any condition is true, they don't overlap
        if not (x1 > x4 or x2 < x3 or y1 > y4 or y2 < y3):
            return False
    return True


def solve(notes: str) -> int:
    """
    Solve the pathfinding problem by building walls from turn instructions,
    then finding the shortest path from origin to final position.

    The algorithm:
    1. Parse turn instructions (R/L) and movement amounts from the input
    2. Build walls by following the path and tracking wall segments
    3. Create a coordinate compression grid (xs, ys sets) for efficient pathfinding
    4. Use Dijkstra's algorithm with Manhattan distance to find shortest path
    """
    # Extract turns (uppercase letters) and amounts (signed integers)
    turns = [char for char in notes if char.isupper()]
    amounts = [int(x) for x in re.findall(r"-?\d+", notes)]

    direction = UP
    position = ORIGIN

    # Track all unique x and y coordinates for coordinate compression
    xs = set()
    ys = set()
    # Each wall is [x_min, x_max, y_min, y_max]
    walls = []

    # Build the walls by following the path
    for turn, amount in zip(turns, amounts):
        # Update direction based on turn instruction
        direction = (
            clockwise(direction) if turn == "R" else counter_clockwise(direction)
        )
        from_pos = position
        # Move in the current direction by the amount
        position = (
            position[0] + direction[0] * amount,
            position[1] + direction[1] * amount,
        )

        x1, x2 = minmax(from_pos[0], position[0])
        y1, y2 = minmax(from_pos[1], position[1])

        # Add boundary coordinates for pathfinding grid (±1 from wall edges)
        xs.add(x1 - 1)
        xs.add(x2 + 1)
        ys.add(y1 - 1)
        ys.add(y2 + 1)

        # Add wall segment based on direction of movement
        if direction == LEFT or direction == RIGHT:
            # Horizontal wall - shrink by 1 on x-axis
            walls.append([x1 + 1, x2 - 1, y1, y2])
        else:
            # Vertical wall - shrink by 1 on y-axis
            walls.append([x1, x2, y1 + 1, y2 - 1])

    # Add final position to coordinate sets
    xs.add(position[0])
    ys.add(position[1])

    # Convert to sorted lists for efficient binary search
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)

    # Dijkstra's algorithm using min heap
    # Heap contains tuples of (cost, point)
    todo = [(0, ORIGIN)]
    seen = {ORIGIN}

    while todo:
        cost, from_point = heapq.heappop(todo)

        # Check if we've reached the destination
        if from_point == position:
            return cost

        # Find next valid grid points in each direction using binary search
        next_points = []

        # Left - find next x coordinate to the left
        idx = bisect_left(xs_sorted, from_point[0])
        if idx > 0:
            next_points.append((xs_sorted[idx - 1], from_point[1]))

        # Right - find next x coordinate to the right
        idx = bisect_right(xs_sorted, from_point[0])
        if idx < len(xs_sorted):
            next_points.append((xs_sorted[idx], from_point[1]))

        # Up - find next y coordinate above
        idx = bisect_left(ys_sorted, from_point[1])
        if idx > 0:
            next_points.append((from_point[0], ys_sorted[idx - 1]))

        # Down - find next y coordinate below
        idx = bisect_right(ys_sorted, from_point[1])
        if idx < len(ys_sorted):
            next_points.append((from_point[0], ys_sorted[idx]))

        # Try to move to each candidate point
        for to_point in next_points:
            if can_move(walls, from_point, to_point) and to_point not in seen:
                seen.add(to_point)
                heapq.heappush(todo, (cost + manhattan(from_point, to_point), to_point))

    raise Exception("No path found")


def part_one(data: list) -> int:
    return solve(data[0])


def part_two(data: list) -> int:
    return solve(data[1])


def part_three(data: list) -> int:
    return solve(data[2])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 110
    print("Part 2:", part_two(data))  # 4331
    print("Part 3:", part_three(data))  # 511692980
