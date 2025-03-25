#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return [int(x) for x in file.read().splitlines()]


def part_one(data: list) -> int:
    return sum(data)


def part_two(data: list) -> int:
    current_frequency = 0
    frequencies = {0}

    while True:
        for change in data:
            current_frequency += change
            if current_frequency in frequencies:
                return current_frequency

            frequencies.add(current_frequency)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 585
    print("Part 2:", part_two(data))  # answer
