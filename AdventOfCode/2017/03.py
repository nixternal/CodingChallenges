#!/usr/bin/env python


def part_one(target: int) -> int:
    """
    Calculates the Manhattan distance from a given number's position in a
    spiral grid to the center (1) using a taxicab geometry approach.

    The grid expands outward in concentric squares, and this function
    determines the layer, side position, and computes the distance accordingly.

    Parameters:
    target (int): The number in the spiral grid for which to calculate the
                  Manhattan distance.

    Returns:
    int: The Manhattan distance from the target number to the center (0,0).
    """

    # Find the ring layer
    layer = 0
    while (2 * layer + 1) ** 2 < target:
        layer += 1

    side_length = 2 * layer  # One side of the square (excluding center)
    max_value_in_layer = (2 * layer + 1) ** 2  # Largest number in this layer

    # Determine which side of the square 'target' is on
    steps_from_corner = (max_value_in_layer - target) % side_length

    # Manhattan Distance = layer + distance from the middle of the side
    return layer + abs(steps_from_corner - layer)


def part_two(target: int) -> int:
    """
    Finds the first value in a spirally filled grid that is larger than a
    given target.

    The grid is filled in a spiral pattern where each cell's value is the sum
    of all adjacent cells (including diagonals). The function stops when a
    value larger than the target is found.

    Parameters:
    target (int): The threshold value to exceed.

    Returns:
    int: The first value in the spiral grid that is larger than the target.
    """

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]   # Right, Up, Left, Down
    diag_dirs = [(1, 1), (-1, 1), (-1, -1), (1, -1)]  # Diagonal Directions

    grid = {(0, 0): 1}  # Dictionary to store values
    x, y = 0, 0         # Start at center
    step = 1            # Steps in the current direction

    while True:
        for dx, dy in directions:
            for _ in range(step):
                x, y = x + dx, y + dy

                # Sum of all adjacent cells
                value = sum(
                    grid.get(
                        (x + ddx, y + ddy),
                        0
                    ) for ddx, ddy in directions + diag_dirs
                )
                grid[(x, y)] = value

                if value > target:
                    return value

            if dx == 0:  # Increase step after vertical movement (Up or Down)
                step += 1


if __name__ == "__main__":
    print("Part 1:", part_one(347991))  # 480
    print("Part 2:", part_two(347991))  # 349975
