#!/usr/bin/env python

import re
from typing import Tuple, List, Optional
import numpy as np
from numpy.typing import NDArray


def read_puzzle_input(
        filename="10.in"
        ) -> Tuple[NDArray[np.int_], NDArray[np.int_]]:
    """
    Parse the input text into numpy arrays of positions and velocities.

    Args:
        input_text: The raw puzzle input

    Returns:
        Tuple containing positions and velocities as numpy arrays
    """

    pattern = (
        r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>'
    )
    positions: List[List[int]] = []
    velocities: List[List[int]] = []

    with open(filename, "r") as file:
        for line in file.readlines():
            match = re.match(pattern, line)
            if match:
                x, y, vx, vy = map(int, match.groups())
                positions.append([x, y])
                velocities.append([vx, vy])

    return np.array(positions), np.array(velocities)


def get_grid_size(positions: NDArray[np.int_]) -> Tuple[int, int, int, int]:
    """
    Calculate the dimensions of the grid containing all points.

    Args:
        positions: Array of point positions

    Returns:
        Tuple of (width, height, min_x, min_y)
    """

    min_x, min_y = positions.min(axis=0)
    max_x, max_y = positions.max(axis=0)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return width, height, min_x, min_y


def print_message(positions: NDArray[np.int_]) -> Optional[str]:
    """
    Create a string representation of the points.

    Args:
        positions: Array of point positions

    Returns:
        String representation of message or None if dimensions are too large
    """

    width, height, min_x, min_y = get_grid_size(positions)

    # Skip if the message is unreasonably large (likely not the right time)
    if width > 100 or height > 20:
        return None

    # Create empty grid
    grid: List[List[str]] = [
        [' ' for _ in range(width)] for _ in range(height)
    ]

    # Fill in the points
    for x, y in positions:
        # Adjust coordinates to be relative to grid
        grid[y - min_y][x - min_x] = '#'

    # Convert grid to string
    return '\n'.join(''.join(row) for row in grid)


def solve(data) -> Tuple[Optional[str], int]:
    """
    Solve the puzzle by finding when the points align to form a message.

    Args:
        input_text: The raw puzzle input

    Returns:
        Tuple of (message, seconds elapsed)
    """

    positions, velocities = data

    # The message appears when the points are closest together
    min_area = float('inf')
    message: Optional[str] = None
    time_elapsed: int = 0

    # Binary search to find when points are closest together
    left, right = 0, 100000

    while left <= right:
        mid = (left + right) // 2

        # Calculate area at mid-1, mid, and mid+1
        pos_prev = positions + velocities * (mid - 1)
        pos_mid = positions + velocities * mid
        pos_next = positions + velocities * (mid + 1)

        width_prev, height_prev, _, _ = get_grid_size(pos_prev)
        width_mid, height_mid, _, _ = get_grid_size(pos_mid)
        width_next, height_next, _, _ = get_grid_size(pos_next)

        area_prev = width_prev * height_prev
        area_mid = width_mid * height_mid
        area_next = width_next * height_next

        # Check if we're at a minimum
        if area_mid < area_prev and area_mid < area_next:
            time_elapsed = mid
            break

        # Move left or right based on derivative
        if area_next < area_mid:
            left = mid + 1
        else:
            right = mid - 1

    # Now that we've found the approximate time, check a small range around it
    min_time = max(0, time_elapsed - 5)
    max_time = time_elapsed + 5

    for t in range(min_time, max_time + 1):
        new_positions = positions + velocities * t
        width, height, _, _ = get_grid_size(new_positions)
        area = width * height

        if area < min_area:
            min_area = area
            candidate = print_message(new_positions)
            if candidate:  # Only update if we got a valid message
                message = candidate
                time_elapsed = t

    return message, time_elapsed


if __name__ == "__main__":
    data = read_puzzle_input()
    message, seconds = solve(read_puzzle_input())

    print("Part 1:", f"\n{message}")  # GGLZLHCE
    print("Part 2:", seconds)         # 10144
