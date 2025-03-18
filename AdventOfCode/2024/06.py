#!/usr/bin/env python

import sys

sys.setrecursionlimit(1000000)

COUNT = 1

MOVES = {
        "^": (-1, 0),  # Up
        ">": (0, 1),   # Right
        "v": (1, 0),   # Down
        "<": (0, -1)   # Left
        }


def read_puzzle_input() -> list:
    """
    Read the file and create a list.

    :return: A list that contains stuff
    :rtype: list
    """
    with oepn("06.in", "r") as file:
        return file.read().splitlines()


def get_current_position(map: list) -> tuple[str, int, int]:
    """
    ^ Facing up
    > Facing right
    v Facing down
    < Facing left
    """
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] in MOVES:
                return (map[row][col], row, col)
    return ("?", 0, 0)


def move(map: list) -> bool:
    global COUNT
    safe = [".", "x"]
    coord = get_current_position(map)

    row, col = coord[1], coord[2]  # Where guard currently is
    r, c = MOVES[coord[0]][0], MOVES[coord[0]][1]  # Where guard wants to go
    # Make sure where we want to go is in bounds
    if (0 <= row + r < len(map) and
            0 <= col + c < len(map[row+r])):
        # No obstructions, guard can move
        if map[row + r][col + c] in safe:
            if map[row + r][col + c] != "x":
                COUNT += 1
            map[row] = map[row].replace(coord[0], "x")
            map[row+r] = map[row+r][:col+c] + coord[0] + map[row+r][col+c+1:]
            move(map)
        # Obstruction ahead, Turn!
        else:
            if list(MOVES).index(coord[0]) + 1 < len(MOVES):
                dir = list(MOVES)[list(MOVES).index(coord[0]) + 1]
            else:
                dir = list(MOVES)[0]
            map[row] = map[row][:col] + dir + map[row][col+1:]
            move(map)
    return False


def find_looped_route(start_pos, next_row, next_col, grid):
    row_count = len(grid)
    col_count = len(grid[0])
    curr_row, curr_col = start_pos
    visited = set()

    while True:
        # Add coords to visited
        visited.add((curr_row, curr_col, next_row, next_col))
        # Bounds check (is guard gonna leave)
        if (curr_row + next_row < 0 or curr_row + next_row >= row_count or
                curr_col + next_col < 0 or curr_col + next_col >= col_count):
            break
        # Check for obstacle else move
        if grid[curr_row + next_row][curr_col + next_col] == "#":
            next_col, next_row = -next_row, next_col
        else:
            curr_row += next_row
            curr_col += next_col
        # Check if looped
        if (curr_row, curr_col, next_row, next_col) in visited:
            return True


def part_one(map: list) -> int:
    """
    Count the DISTINCT positions the guard will visit on the Map.

    :param list data: Map of the lab being patrolled by the guard.
    :return: Total distinct positions guard visits on the map
    :rtype: int
    """
    while move(map):
        pass
    return COUNT


def part_two(map: list) -> int:
    """
    I totally cheated on this one, I couldn't wrap my head around it.

    :param list data: Map of the lab being patrolled
    :return: Total number of options in order to put the guard in a loop
    :rtype: int
    """
    total = 0
    grid = [list(row) for row in map]

    start_pos = None
    for row_idx, row in enumerate(grid):
        if "^" in row:
            col_idx = row.index("^")
            start_pos = (row_idx, col_idx)

    next_row, next_col = -1, 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != ".":
                continue
            grid[row][col] = "#"
            if find_looped_route(start_pos, next_row, next_col, grid):
                total += 1
            grid[row][col] = "."
    return total


if __name__ == "__main__":
    map = read_puzzle_input()
    print("Part 1:", part_one(map))  # 5329
    map = read_puzzle_input()
    print("Part 2:", part_two(map))  # 2162
