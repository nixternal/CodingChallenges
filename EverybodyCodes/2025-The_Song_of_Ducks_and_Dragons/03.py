#!/usr/bin/env python


def read_puzzle_input() -> list[str]:
    with open("03.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list[str]) -> int:
    return sum(set(map(int, data[0].split(','))))


def part_two(data: list[str]) -> int:
    return sum(sorted(set(map(int, data[1].split(','))))[:20])


def part_three(data: list[str]) -> int:
    crates = list(map(int, data[2].split(',')))

    # Build frequency dictionary manually
    counts = {}
    for crate in crates:
        counts[crate] = counts.get(crate, 0) + 1

    # Return the maximum count
    return max(counts.values())


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2612
    print("Part 2:", part_two(data))  # 262
    print("Part 3:", part_three(data))  # 3350
