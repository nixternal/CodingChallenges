#!/usr/bin/env python

from math import prod


def read_puzzle_input() -> list:
    with open("03.in", "r") as file:
        return [line.strip() for line in file]


def count_trees(lines: list[str], right: int, down: int) -> int:
    width = len(lines[0])
    row = col = trees = 0

    while row < len(lines):
        if lines[row][col % width] == "#":
            trees += 1
        col += right
        row += down

    return trees


def part_one(data: list[str]) -> int:
    return count_trees(data, 3, 1)


def part_two(data: list[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return prod(count_trees(data, r, d) for r, d in slopes)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 164
    print("Part 2:", part_two(data))  # 5007658656
