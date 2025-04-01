#!/usr/bin/env python

import math


def read_puzzle_input() -> tuple:
    """
    Reads the puzzle input from '16.in' file and returns its content as a
    string.
    """

    with open("16.in", "r") as file:
        lines = file.readlines()

    instructions = [line.strip() for line in lines[:-2]]
    twists = lines[-1].strip()

    return instructions, twists


def rotate_face_clockwise(grid: list) -> None:
    """
    Rotates a 2D grid (face of the cube) 90 degrees clockwise in-place.

    Args:
        grid: The 2D list representing a face of the cube to be rotated
    """

    new_grid = [list(reversed(x)) for x in zip(*grid)]
    for row, new_row in zip(grid, new_grid):
        row[:] = new_row


def rotate_face_counterclockwise(grid: list) -> None:
    """
    Rotates a 2D grid (face of the cube) 90 degrees counter-clockwise in-place.
    Implemented as three clockwise rotations.

    Args:
        grid: The 2D list representing a face of the cube to be rotated
    """

    for _ in range(3):
        rotate_face_clockwise(grid)


def reorder_faces(faces: list, twist: str) -> None:
    """
    Reorders the faces list based on the cube twist direction.
    The faces list represents the current orientation of the cube's faces.

    Args:
        faces: List of face indices representing current cube orientation
               (modified in-place)
        twist: String indicating the twist direction
               ('U', 'D', 'L', 'R', or empty)
    """

    match twist:
        case "D":
            order = [1, 2, 3, 0, 4, 5]  # Down twist reordering
        case "U":
            order = [3, 0, 1, 2, 4, 5]  # Up twist reordering
        case "L":
            order = [4, 1, 5, 3, 2, 0]  # Left twist reordering
        case "R":
            order = [5, 1, 4, 3, 0, 2]  # Right twist reordering
        case "":
            order = list(range(6))      # No twist - maintain current order
        case _:
            assert False, f"Unknown twist: {twist}"

    faces[:] = [faces[i] for i in order]


def rotate_grids_for_twist(grids: list, faces: list, twist: str) -> None:
    """
    Rotates specific faces of the cube based on the twist direction.
    Some faces require 180-degree rotations during certain twists.

    Args:
        grids: List of all face grids (6 faces)
        faces: Current ordering of face indices
        twist: Direction of cube twist
    """

    match twist:
        case "D":
            # Rotate bottom face clockwise and top face counter-clockwise
            rotate_face_clockwise(grids[faces[5]])
            rotate_face_counterclockwise(grids[faces[4]])
            # Rotate front and back faces 180 degrees
            for _ in range(2):
                rotate_face_clockwise(grids[faces[2]])
                rotate_face_clockwise(grids[faces[3]])
        case "U":
            # Rotate top face clockwise and bottom face counter-clockwise
            rotate_face_clockwise(grids[faces[4]])
            rotate_face_counterclockwise(grids[faces[5]])
            # Rotate front and right faces 180 degrees
            for _ in range(2):
                rotate_face_clockwise(grids[faces[2]])
                rotate_face_clockwise(grids[faces[1]])
        case "L":
            # Rotate left face clockwise and right face counter-clockwise
            rotate_face_clockwise(grids[faces[1]])
            rotate_face_counterclockwise(grids[faces[3]])
        case "R":
            # Rotate right face clockwise and left face counter-clockwise
            rotate_face_clockwise(grids[faces[3]])
            rotate_face_counterclockwise(grids[faces[1]])
        case "":
            pass  # No rotation needed for no twist
        case _:
            assert False, f"Unknown twist: {twist}"


def apply_twist(grids: list, faces: list, twist: str) -> None:
    """
    Applies a full cube twist by rotating appropriate faces and reordering
    face positions.

    Args:
        grids: List of all face grids
        faces: Current face ordering (modified in-place)
        twist: Direction of cube twist
    """

    rotate_grids_for_twist(grids, faces, twist)
    reorder_faces(faces, twist)


def normalize_grid_values(grid: list) -> None:
    """
    Normalizes all values in a grid to be ≤ 100 by repeatedly subtracting 100.

    Args:
        grid: The 2D grid to normalize
    """

    for r in range(80):
        for c in range(80):
            while grid[r][c] > 100:
                grid[r][c] -= 100


def modify_row(grid: list, row: int, value: int) -> None:
    """
    Adds a value to all cells in a specified row, normalizing values to ≤ 100.

    Args:
        grid: The 2D grid to modify
        row: Row index (1-based)
        value: Value to add to each cell
    """

    row_idx = row - 1
    for c in range(80):
        grid[row_idx][c] += value
        while grid[row_idx][c] > 100:
            grid[row_idx][c] -= 100


def modify_column(grid: list, col: int, value: int) -> None:
    """
    Adds a value to all cells in specified column, normalizing values to ≤ 100.

    Args:
        grid: The 2D grid to modify
        col: Column index (1-based)
        value: Value to add to each cell
    """

    col_idx = col - 1
    for r in range(80):
        grid[r][col_idx] += value
        while grid[r][col_idx] > 100:
            grid[r][col_idx] -= 100


def modify_face(grid: list, value: int) -> None:
    """
    Adds a value to all cells in a face, normalizing values to ≤ 100.

    Args:
        grid: The 2D grid to modify
        value: Value to add to each cell
    """

    for r in range(80):
        for c in range(80):
            grid[r][c] += value
            while grid[r][c] > 100:
                grid[r][c] -= 100


def get_dominant_sum(grid: list) -> int:
    """
    Calculates the dominant sum of a grid - the maximum of all row and column
    sums.

    Args:
        grid: The 2D grid to analyze

    Returns:
        The maximum sum found among all rows and columns
    """

    return max(
        max(sum(row) for row in grid),
        max(sum(col) for col in zip(*grid)),
    )


def part_one(data: tuple) -> int:
    """
    Solves Part 1 of the puzzle:
    - Processes a series of instructions that modify cube face values
    - Tracks 'power' values for each face based on modifications
    - Returns the product of the two highest power values

    Args:
        data: The puzzle input string containing instructions and twists

    Returns:
        The product of the two highest face powers
    """

    instructions, twists = data

    faces = list(range(6))  # FDBULR - Front, Down, Back, Up, Left, Right
    powers = [0] * 6
    grids = [[[1 for _ in range(80)] for _ in range(80)] for _ in range(6)]

    for instruction, twist in zip(instructions, list(twists) + [""]):
        match instruction.split():
            case ["FACE", "-", "VALUE", value]:
                powers[faces[0]] += int(value) * 80 * 80
                grid = grids[faces[0]]
                for r in range(80):
                    for c in range(80):
                        grid[r][c] += int(value)
            case ["ROW", row, "-", "VALUE", value]:
                powers[faces[0]] += int(value) * 80
                grid = grids[faces[0]]
                for c in range(80):
                    grid[int(row) - 1][c] += int(value)
            case ["COL", col, "-", "VALUE", value]:
                powers[faces[0]] += int(value) * 80
                grid = grids[faces[0]]
                for r in range(80):
                    grid[r][int(col) - 1] += int(value)
            case _:
                assert False, f"Unknown instruction: {instruction}"

        normalize_grid_values(grids[faces[0]])

        if twist:
            reorder_faces(faces, twist)

    return math.prod(sorted(powers)[-2:])


def part_two(data: tuple) -> int:
    """
    Solves Part 2 of the puzzle:
    - Processes modifications to cube faces while handling twists
    - Calculates dominant sums for each face after all modifications
    - Returns the product of all dominant sums

    Args:
        data: The puzzle input string containing instructions and twists

    Returns:
        The product of all face dominant sums
    """

    instructions, twists = data

    faces = list(range(6))  # FDBULR - Front, Down, Back, Up, Left, Right
    grids = [[[1 for _ in range(80)] for _ in range(80)] for _ in range(6)]

    for instruction, twist in zip(instructions, list(twists) + [""]):
        match instruction.split():
            case ["FACE", "-", "VALUE", value]:
                modify_face(grids[faces[0]], int(value))
            case ["ROW", row, "-", "VALUE", value]:
                modify_row(grids[faces[0]], int(row), int(value))
            case ["COL", col, "-", "VALUE", value]:
                modify_column(grids[faces[0]], int(col), int(value))
            case _:
                assert False, f"Unknown instruction: {instruction}"

        if twist:
            apply_twist(grids, faces, twist)

    dominant_sums = [get_dominant_sum(grid) for grid in grids]
    return math.prod(dominant_sums)


def part_three(data: tuple) -> int:
    """
    Solves Part 3 of the puzzle:
    - Similar to Part 2 but applies row/column modifications to all 4 rotated
      versions
    - Maintains original orientation after modifications
    - Returns the product of all dominant sums

    Args:
        data: The puzzle input string containing instructions and twists

    Returns:
        The product of all face dominant sums
    """

    instructions, twists = data

    faces = list(range(6))  # FDBULR - Front, Down, Back, Up, Left, Right
    grids = [[[1 for _ in range(80)] for _ in range(80)] for _ in range(6)]

    for instruction, twist in zip(instructions, list(twists) + [""]):
        match instruction.split():
            case ["FACE", "-", "VALUE", value]:
                modify_face(grids[faces[0]], int(value))
            case ["ROW", row, "-", "VALUE", value]:
                # Save current orientation
                original_faces = faces.copy()
                # Apply modification in all 4 right-rotated positions
                for _ in range(4):
                    apply_twist(grids, faces, "R")
                    modify_row(grids[faces[0]], int(row), int(value))
                # Restore original orientation
                faces[:] = original_faces
            case ["COL", col, "-", "VALUE", value]:
                # Save current orientation
                original_faces = faces.copy()
                # Apply modification in all 4 up-rotated positions
                for _ in range(4):
                    apply_twist(grids, faces, "U")
                    modify_column(grids[faces[0]], int(col), int(value))
                # Restore original orientation
                faces[:] = original_faces
            case _:
                assert False, f"Unknown instruction: {instruction}"

        if twist:
            apply_twist(grids, faces, twist)

    dominant_sums = [get_dominant_sum(grid) for grid in grids]
    return math.prod(dominant_sums)


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data))    # 263777343897600
    print("Part 2:", part_two(data))    # 55202380673451368107608
    print("Part 3:", part_three(data))  # 12111805734249037050000
