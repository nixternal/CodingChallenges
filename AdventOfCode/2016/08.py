#!/usr/bin/env python


from ast import parse


def read_puzzle_input() -> list:
    with open("08.in", "r") as file:
        return file.read().splitlines()


def parse_instruction(grid: list, instruction: str) -> list:
    if instruction.startswith('rect'):
        # Extract dimensions
        a, b = map(int, instruction.split()[1].split('x'))
        for y in range(b):
            for x in range(a):
                grid[y][x] = 1  # Turn on the pixel
    elif instruction.startswith('rotate row'):
        # Extract row and shift amount
        y, n = map(int, instruction.split('=')[1].split(' by '))
        grid[y] = grid[y][-n:] + grid[y][:-n]  # Rotate the row
    elif instruction.startswith('rotate column'):
        # Extract the column and shift amount
        x, n = map(int, instruction.split('=')[1].split(' by '))
        column = [grid[y][x] for y in range(len(grid))]
        column = column[-n:] + column[:-n]  # Rotate the column
        for y in range(len(grid)):
            grid[y][x] = column[y]

    return grid


def part_one(data: list) -> int:
    grid = [[0] * 50 for _ in range(6)]

    for instruction in data:
        grid = parse_instruction(grid, instruction)

    return sum(sum(row) for row in grid)


def part_two(data: list) -> None:
    grid = [[0] * 50 for _ in range(6)]

    for instruction in data:
        grid = parse_instruction(grid, instruction)

    for row in grid:
        print(''.join('#' if cell else '.' for cell in row))
    print()


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 106
    print("Part 2:")                  # CFLELOYFCS
    part_two(data)
