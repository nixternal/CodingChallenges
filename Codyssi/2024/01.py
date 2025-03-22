#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return [int(x) for x in file.read().splitlines()]


def part_one(data: list) -> int:
    return sum(data)


def part_two(data: list) -> int:
    data = sorted(data)
    return sum(data[:-20])


def part_three(data: list) -> int:
    total = data[0]
    for i in range(1, len(data)):
        if i % 2 == 0:
            total += data[i]
        else:
            total -= data[i]
    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 147676791
    print("Part 2:", part_two(data))    # 128268069
    print("Part 3:", part_three(data))  # -2959477
