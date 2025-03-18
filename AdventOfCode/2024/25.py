#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("25.in", "r") as file:
        return file.read().split('\n\n')


def part_one(data: list) -> int:
    locks = []
    keys = []
    for line in data:
        current = {i for i, c in enumerate(line) if c == "#"}
        if line.startswith("#"):
            locks.append(current)
        else:
            keys.append(current)

    return sum(not lock & key for lock in locks for key in keys)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # answer
