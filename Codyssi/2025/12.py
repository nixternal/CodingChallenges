#!/usr/bin/env python

import re
from typing import List, Optional, Tuple


def read_puzzle_input() -> Tuple[List[List[int]], List[str], List[str]]:
    """
    Read and parse the puzzle input file.

    Returns:
    - grid: 2D list of integers representing the initial grid
    - instructions: list of string instructions to modify the grid
    - flow_control: list of control flow instructions (TAKE, CYCLE, ACT)
    """
    with open("12.in", "r") as file:
        lines = file.readlines()

    grid = []
    instructions = []
    flow_control = []
    reading_grid = True

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if reading_grid:
            # Check if line contains non-digit characters to switch to
            # instructions
            if re.match(r'\D', line):
                reading_grid = False
                instructions.append(line)
            else:
                # Convert grid line to list of integers
                grid.append(list(map(int, line.split())))
        elif "TAKE" in line or "CYCLE" in line or "ACT" in line:
            flow_control.append(line)
        else:
            instructions.append(line)

    return grid, instructions, flow_control


def apply_shift(grid: List[List[int]],
                axis: str,
                index: int,
                shift: int
                ) -> None:
    """
    Apply a cyclic shift to a specific row or column in the grid.

    Args:
    - grid: 2D list to modify
    - axis: 'ROW' or 'COL' to specify shift direction
    - index: row or column index to shift
    - shift: number of positions to shift
    """
    if axis == "ROW":
        # Normalize shift to grid width
        shift %= len(grid[index])
        grid[index] = grid[index][-shift:] + grid[index][:-shift]
    else:  # COL
        # Extract column
        col = [grid[i][index] for i in range(len(grid))]

        # Normalize shift to column length
        shift %= len(col)
        col = col[-shift:] + col[:-shift]

        # Update column in grid
        for i in range(len(grid)):
            grid[i][index] = col[i]


def apply_operation(
    grid: List[List[int]],
    operation: str,
    value: int,
    axis: Optional[str] = None,
    index: Optional[int] = None
) -> None:
    """
    Apply a mathematical operation to the entire grid or a specific row/column.

    Args:
    - grid: 2D list to modify
    - operation: 'ADD', 'SUB', or 'MULTIPLY'
    - value: number to apply in the operation
    - axis: optional 'ROW' or 'COL' to limit operation
    - index: optional row or column index when axis is specified
    """
    # Large prime modulo to prevent integer overflow
    MODULO = 1073741824

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Skip rows/columns not matching index if specified
            if axis == "ROW" and i != index:
                continue
            if axis == "COL" and j != index:
                continue

            # Apply operation with modulo
            if operation == "ADD":
                grid[i][j] = (grid[i][j] + value) % MODULO
            elif operation == "SUB":
                grid[i][j] = (grid[i][j] - value) % MODULO
            elif operation == "MULTIPLY":
                grid[i][j] = (grid[i][j] * value) % MODULO


def process_grid(grid: List[List[int]],
                 instructions: List[str]
                 ) -> List[List[int]]:
    """
    Process a series of instructions to modify the grid.

    Args:
    - grid: 2D list to modify
    - instructions: list of string instructions

    Returns:
    Modified grid after applying all instructions
    """
    for instr in instructions:
        parts = instr.split()

        if parts[0] == "SHIFT":
            apply_shift(grid, parts[1], int(parts[2]) - 1, int(parts[4]))
        elif parts[0] in {"ADD", "SUB", "MULTIPLY"}:
            if parts[2] == "ALL":
                apply_operation(grid, parts[0], int(parts[1]))
            else:
                apply_operation(
                    grid, parts[0], int(parts[1]), parts[2], int(parts[3]) - 1
                )

    return grid


def execute_flow_control(
    grid: List[List[int]],
    instructions: List[str],
    flow_control: List[str]
) -> List[List[int]]:
    """
    Execute flow control instructions on the grid.

    Args:
    - grid: 2D list to modify
    - instructions: list of string instructions
    - flow_control: list of control flow instructions

    Returns:
    Modified grid after applying flow control
    """
    queue = list(instructions)
    taken = None

    for action in flow_control:
        if action == "TAKE":
            taken = queue.pop(0) if queue else None
        elif action == "CYCLE" and taken:
            queue.append(taken)
        elif action == "ACT" and taken:
            process_grid(grid, [taken])
            taken = None

    return grid


def part_one(grid: List[List[int]]) -> int:
    """
    Solve part one by finding the maximum row or column sum.

    Args:
    - grid: 2D list of integers

    Returns:
    Maximum sum of any row or column
    """
    return max(max(map(sum, grid)), max(map(sum, zip(*grid))))


def part_two(
    grid: List[List[int]],
    instructions: List[str],
    flow_control: List[str]
) -> int:
    """
    Solve part two by applying flow control and finding max row/column sum.

    Args:
    - grid: 2D list of integers
    - instructions: list of string instructions
    - flow_control: list of control flow instructions

    Returns:
    Maximum sum of any row or column after flow control
    """
    grid = execute_flow_control(grid, instructions, flow_control)
    return max(max(map(sum, grid)), max(map(sum, zip(*grid))))


def part_three(
    grid: List[List[int]],
    instructions: List[str],
    flow_control: List[str]
) -> int:
    """
    Solve part three by continuously applying flow control until queue is empty

    Args:
    - grid: 2D list of integers
    - instructions: list of string instructions
    - flow_control: list of control flow instructions

    Returns:
    Maximum sum of any row or column after exhausting all instructions
    """
    queue = list(instructions)
    taken = None

    while queue:
        for action in flow_control:
            if action == "TAKE" and queue:
                taken = queue.pop(0)
            elif action == "CYCLE" and taken:
                queue.append(taken)
            elif action == "ACT" and taken:
                process_grid(grid, [taken])
                taken = None

    return max(max(map(sum, grid)), max(map(sum, zip(*grid))))


if __name__ == "__main__":
    original_grid, instructions, flow_control = read_puzzle_input()

    print(  # 18720856565
        "Part 1:",
        part_one(
            process_grid([row[:] for row in original_grid], instructions)
        )
    )

    print(  # 246282407
        "Part 2:",
        part_two(
            [row[:] for row in original_grid], instructions, flow_control
        )
    )

    print(  # 20025502527
        "Part 3:",
        part_three(
            [row[:] for row in original_grid], instructions, flow_control
        )
    )
