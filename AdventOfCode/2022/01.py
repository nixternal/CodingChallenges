#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return file.read().split("\n\n")


def parse_elves(data: list) -> list:
    """Convert raw data into list of calorie totals per elf."""
    return [sum(int(x) for x in elf.splitlines()) for elf in data]


def part_one(data: list) -> int:
    return max(parse_elves(data))


def part_two(data: list) -> int:
    return sum(sorted(parse_elves(data), reverse=True)[:3])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 72718
    print("Part 2:", part_two(data))  # 213089
