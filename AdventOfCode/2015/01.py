#!/usr/bin/env python


def read_puzzle_input() -> str:
    with open("01.in", "r") as file:
        return file.read()


def part_one(data: str) -> int:
    return data.count('(') - data.count(')')


def part_two(data: str) -> int:
    floor = 0
    for i, char in enumerate(data, 1):
        if char == "(":
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            return i
    return 0


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 232
    print("Part 2:", part_two(data))  # 1783
