#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("04.in", "r") as file:
        return file.read().split("\n\n")


def level_nails(nails: list[int], target: int | None = None) -> int:
    if target is None:
        target = min(nails)
    return sum(abs(nail - target) for nail in nails)


def part_one(data: list) -> int:
    nails = [int(x) for x in data[0].splitlines()]
    return level_nails(nails)


def part_two(data: list) -> int:
    nails = [int(x) for x in data[1].splitlines()]
    return level_nails(nails)


def part_three(data: list) -> int:
    nails = sorted([int(x) for x in data[2].splitlines()])
    return level_nails(nails, nails[len(nails) // 2])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 91
    print("Part 2:", part_two(data))  # 857900
    print("Part 3:", part_three(data))  # 121820510
