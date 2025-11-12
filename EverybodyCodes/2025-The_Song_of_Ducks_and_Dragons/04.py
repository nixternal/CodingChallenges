#!/usr/bin/env python

import math


def read_puzzle_input() -> list:
    with open("04.in", "r") as file:
        return file.read().split("\n\n")


def part_one(data: list) -> int:
    gears = list(map(int, data[0].split()))
    return int(2025 * gears[0] / gears[-1])


def part_two(data: list) -> int:
    gears = list(map(int, data[1].split()))
    return math.ceil(10000000000000 * gears[-1] / gears[0])


def part_three(data: list) -> int:
    lines = data[2].splitlines()
    total = float(lines[0])

    for line in lines[1:-1]:
        a, b = line.split("|")
        total *= int(b) / int(a)

    total /= int(lines[-1])

    return int(total * 100)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10024
    print("Part 2:", part_two(data))  # 3299595141701
    print("Part 3:", part_three(data))  # 131861053440
