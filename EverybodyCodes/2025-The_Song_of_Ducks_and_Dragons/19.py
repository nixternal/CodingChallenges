#!/usr/bin/env python
"""
Dynamic programming solution for optimal flapping navigation through obstacles.

The problem models movement where:
- Position advances horizontally (x-axis) with each time step
- Height (y-axis) changes based on flapping: y_new = y_old + 2*flaps - delta_x
- Must pass through specified height ranges at certain x positions
- Goal: minimize total flaps needed
"""

from collections import defaultdict


def read_puzzle_input() -> list:
    """Read and split input file into sections."""
    with open("19.in", "r") as file:
        return file.read().split("\n\n")


def parse_obstacles(lines):
    """
    Parse obstacle specifications into (x, start_height, height_range) triplets.

    Args:
        lines: Input lines, each containing 3 space or comma-separated integers

    Returns:
        List of (x_position, start_height, height_range) tuples
    """
    obstacles = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle both comma and space-separated values
        parts = [p.strip() for p in line.replace(",", " ").split() if p.strip()]

        if len(parts) != 3:
            raise ValueError(f"Expected 3 values, got {len(parts)}: {line}")

        x, start, height = map(int, parts)
        obstacles.append((x, start, height))

    return obstacles


def calculate_min_flaps(obstacles):
    """
    Calculate minimum flaps needed to navigate through all obstacles.

    Uses dynamic programming where:
    - State: (height, cumulative_flap_cost) at each x position
    - Transition: For each valid target height, calculate required flaps
    - Constraint: flaps must be non-negative integer (derived from physics)

    Returns:
        Minimum flaps needed, or None if no valid path exists
    """
    if not obstacles:
        return 0

    # Group obstacles by x-coordinate (handles multiple openings at same x)
    walls = defaultdict(list)
    for x, start, height_range in obstacles:
        walls[x].append((start, start + height_range - 1))  # inclusive range

    # Process walls in order
    x_positions = sorted(walls.keys())

    # DP state: height -> minimum flaps to reach that height
    dp = {0: 0}  # Start at height 0 with 0 flaps
    prev_x = 0

    for x in x_positions:
        delta_x = x - prev_x
        new_dp = {}

        # For each current state and each valid target height
        for y_current, flaps_so_far in dp.items():
            for start, end in walls[x]:
                for y_target in range(start, end + 1):
                    # Physics constraint: y_target = y_current + 2*flaps - delta_x
                    # Solving for flaps: flaps = (delta_x + y_target - y_current) / 2
                    numerator = delta_x + y_target - y_current

                    # Must be even (integer number of flaps) and non-negative
                    if numerator % 2 != 0:
                        continue

                    flaps = numerator // 2
                    if not (0 <= flaps <= delta_x):
                        continue

                    total_flaps = flaps_so_far + flaps

                    # Update if this is better than previous best for this height
                    if y_target not in new_dp or total_flaps < new_dp[y_target]:
                        new_dp[y_target] = total_flaps

        dp = new_dp
        prev_x = x

        # No valid states means no solution exists
        if not dp:
            return None

    return min(dp.values())


def part_one(data: list) -> int:
    lines = data[0].strip().splitlines()
    obstacles = parse_obstacles(lines)
    result = calculate_min_flaps(obstacles)
    return result if result is not None else -1


def part_two(data: list) -> int:
    lines = data[1].strip().splitlines()
    obstacles = parse_obstacles(lines)
    result = calculate_min_flaps(obstacles)
    return result if result is not None else -1


def part_three(data: list) -> int:
    lines = data[2].strip().splitlines()
    obstacles = parse_obstacles(lines)
    result = calculate_min_flaps(obstacles)
    return result if result is not None else -1


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 52
    print("Part 2:", part_two(data))  # 790
    print("Part 3:", part_three(data))  # 4411137
