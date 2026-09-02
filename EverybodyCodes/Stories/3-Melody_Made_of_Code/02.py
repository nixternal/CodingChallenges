#!/usr/bin/env python
"""
Sound Wave Simulation Puzzle Solver

This module solves a 3-part puzzle involving sound wave propagation through a grid.
The sound originates from a source '@' and must navigate around obstacles ('#')
to reach or surround vocal bones.

Part 1: Sound moves in repeating U,R,D,L pattern until it reaches a single bone
Part 2: Sound moves in repeating U,R,D,L pattern, treating bones as obstacles,
        until all bones are surrounded by sound
Part 3: Same as Part 2 but direction pattern is UUU, RRR, DDD, LLL
"""

from collections import deque

# Cardinal directions: Up, Right, Down, Left
DIRECTIONS = [
    (-1, 0),  # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1),  # Left
]

# Part 3: Each direction is attempted three times consecutively
PART_THREE_DIRECTIONS = [
    (-1, 0),
    (-1, 0),
    (-1, 0),  # Up x3
    (0, 1),
    (0, 1),
    (0, 1),  # Right x3
    (1, 0),
    (1, 0),
    (1, 0),  # Down x3
    (0, -1),
    (0, -1),
    (0, -1),  # Left x3
]


def read_puzzle_input() -> list[str]:
    with open("02.in", "r", encoding="utf-8") as file:
        return file.read().strip().split("\n\n")


def find_source_and_bones(
    lines: list[str],
) -> tuple[tuple[int, int], set[tuple[int, int]]]:
    """
    Locate the sound source and all bone cells in the grid.

    Args:
        lines: Grid representation as list of strings

    Returns:
        tuple of (source_coordinate, set_of_bone_coordinates)

    Raises:
        ValueError: If source '@' is missing or no bones '#' found
    """
    source = None
    bones = set()

    for row, line in enumerate(lines):
        for col, cell in enumerate(line):
            if cell == "@":
                source = (row, col)
            elif cell == "#":
                bones.add((row, col))

    if source is None:
        raise ValueError("No sound source '@' found.")
    if not bones:
        raise ValueError("No vocal bone '#' found.")

    return source, bones


def get_grid_bounds(walls: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculate the bounding box for the grid with a one-cell margin.

    Args:
        walls: Set of wall coordinates (sound + bones)

    Returns:
        Tuple of (min_row, max_row, min_col, max_col) with margin
    """
    min_row = min(row for row, _ in walls) - 1
    max_row = max(row for row, _ in walls) + 1
    min_col = min(col for _, col in walls) - 1
    max_col = max(col for _, col in walls) + 1
    return min_row, max_row, min_col, max_col


def is_valid_cell(row: int, col: int, bounds: tuple[int, int, int, int]) -> bool:
    """Check if a cell is within the grid bounds."""
    min_row, max_row, min_col, max_col = bounds
    return min_row <= row <= max_row and min_col <= col <= max_col


def fill_enclosed_air(
    sound: set[tuple[int, int]], bones: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    """
    Identify and fill all enclosed air cells with sound.

    Using flood fill from the exterior of a bounded region, this function
    identifies all air cells that are not connected to the outside. These
    enclosed cells are immediately converted to sound.

    Args:
        sound: Current set of sound cells (treated as walls)
        bones: Set of bone cells (treated as walls)

    Returns:
        Set of exterior air cells (air connected to outside)
    """
    walls = sound | bones
    bounds = get_grid_bounds(walls)
    min_row, max_row, min_col, max_col = bounds

    # Start flood fill from the top-left corner outside the grid
    exterior_start = (min_row, min_col)
    exterior_air = {exterior_start}
    queue = deque([exterior_start])

    # BFS to find all cells connected to the exterior
    while queue:
        row, col = queue.popleft()

        for delta_row, delta_col in DIRECTIONS:
            next_row = row + delta_row
            next_col = col + delta_col
            next_cell = (next_row, next_col)

            if not is_valid_cell(next_row, next_col, bounds):
                continue
            if next_cell in walls or next_cell in exterior_air:
                continue

            exterior_air.add(next_cell)
            queue.append(next_cell)

    # Find enclosed air cells (not walls and not connected to exterior)
    enclosed_air = set()
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            cell = (row, col)
            if cell not in walls and cell not in exterior_air:
                enclosed_air.add(cell)

    # Enclosed air instantly becomes sound
    sound.update(enclosed_air)
    return exterior_air


def bones_are_surrounded(
    bones: set[tuple[int, int]], exterior_air: set[tuple[int, int]]
) -> bool:
    """
    Check if all bones are completely surrounded by sound.

    A bone is surrounded when none of its adjacent cells (up, right, down, left)
    are connected to the exterior air. This works for single bones, connected
    bone structures, and multiple disconnected bones.

    Args:
        bones: Set of bone coordinates
        exterior_air: Set of air cells connected to the outside

    Returns:
        True if all bones are surrounded, False otherwise
    """
    for row, col in bones:
        for delta_row, delta_col in DIRECTIONS:
            neighbor = (row + delta_row, col + delta_col)
            if neighbor in exterior_air:
                return False
    return True


def simulate_sound(
    lines: list[str],
    move_sequence: list[tuple[int, int]],
    stop_when_reaching_bone: bool,
) -> int:
    """
    Main simulation engine for sound wave propagation.

    The sound starts at '@' and follows the given movement pattern. Each step
    extends the sound wave by one cell. Depending on the mode, the simulation
    stops when the sound reaches a bone or when all bones are surrounded.

    Args:
        lines: Grid representation
        move_sequence: List of (row_delta, col_delta) moves
        stop_when_reaching_bone: If True, stop when sound reaches a bone
                                If False, treat bones as obstacles and stop
                                when all are surrounded

    Returns:
        Number of steps taken until stopping condition is met

    Raises:
        ValueError: If Part 1 mode is used with more than one bone
    """
    source, bones = find_source_and_bones(lines)

    # Validate Part 1 has exactly one bone
    if stop_when_reaching_bone and len(bones) != 1:
        raise ValueError("Part 1 expects exactly one vocal bone.")

    # Initialize simulation state
    sound = {source}
    row, col = source
    direction_index = 0
    steps = 0

    while True:
        # Get next move direction
        delta_row, delta_col = move_sequence[direction_index]
        direction_index = (direction_index + 1) % len(move_sequence)

        # Calculate target cell
        next_row = row + delta_row
        next_col = col + delta_col
        next_cell = (next_row, next_col)

        # Skip if target already has sound
        if next_cell in sound:
            continue

        # In obstacle mode, bones block movement
        if not stop_when_reaching_bone and next_cell in bones:
            continue

        # Move sound to new cell
        row, col = next_row, next_col
        sound.add((row, col))
        steps += 1

        # Part 1: Stop when reaching the single bone
        if stop_when_reaching_bone and next_cell in bones:
            return steps

        # Parts 2 & 3: Update enclosed air and check surround condition
        exterior_air = fill_enclosed_air(sound, bones)
        if bones_are_surrounded(bones, exterior_air):
            return steps


def steps_to_vocal_bone(lines: list[str]) -> int:
    """
    Part 1: Find steps to reach the vocal bone.

    Uses pattern: U, R, D, L (repeating)
    Bone cells are not obstacles (sound can pass through them)
    """
    return simulate_sound(
        lines,
        DIRECTIONS,
        stop_when_reaching_bone=True,
    )


def steps_to_surround_vocal_bone(lines: list[str]) -> int:
    """
    Part 2: Find steps to surround the vocal bone.

    Uses pattern: U, R, D, L (repeating)
    Bone cells ARE obstacles (sound cannot pass through them)
    """
    return simulate_sound(
        lines,
        DIRECTIONS,
        stop_when_reaching_bone=False,
    )


def steps_to_surround_all_bones(lines: list[str]) -> int:
    """
    Part 3: Find steps to surround all vocal bones.

    Uses pattern: UUU, RRR, DDD, LLL (repeating)
    All bone cells ARE obstacles
    """
    return simulate_sound(
        lines,
        PART_THREE_DIRECTIONS,
        stop_when_reaching_bone=False,
    )


def part_one(data: list[str]) -> int:
    return steps_to_vocal_bone(data[0].splitlines())


def part_two(data: list[str]) -> int:
    return steps_to_surround_vocal_bone(data[1].splitlines())


def part_three(data: list[str]) -> int:
    return steps_to_surround_all_bones(data[2].splitlines())


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data))  # 257
    print("Part 2:", part_two(data))  # 3104
    print("Part 3:", part_three(data))  # 2375
