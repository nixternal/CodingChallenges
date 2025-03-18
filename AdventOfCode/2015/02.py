#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("02.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    sqft = 0
    present_dimensions = [[int(x) for x in d.split('x')] for d in data]
    for pd in present_dimensions:
        sides = (pd[0]*pd[1], pd[1]*pd[2], pd[2]*pd[0])
        sqft += min(sides) + 2 * sum(sides)

    return sqft


def part_two(data: list) -> int:
    feet = 0
    present_dimensions = [[int(x) for x in d.split('x')] for d in data]
    for pd in present_dimensions:
        pd.sort()
        feet += 2 * (pd[0]) + 2 * pd[1] + pd[0] * pd[1] * pd[2]

    return feet


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1588178
    print("Part 2:", part_two(data))  # 3783758
