#!/usr/bin/env python

import itertools


def read_puzzle_input() -> list:
    with open("17.in", "r") as file:
        return [int(x) for x in file.read().splitlines()]


def part_one(data: list) -> int:
    return len([
        seq for i in range(len(data), 0, -1) for
        seq in itertools.combinations(data, i)
        if sum(seq) == 150
    ])


def part_two(data: list) -> int:
    combos = [
        seq for i in range(len(data), 0, -1) for
        seq in itertools.combinations(data, i)
        if sum(seq) == 150
    ]

    combos.sort(key=len)
    return len([c for c in combos if len(c) <= len(combos[0])])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 654
    print("Part 2:", part_two(data))  # 57
