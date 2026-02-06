#!/usr/bin/env python


def read_puzzle_input() -> list[int]:
    with open("06.in", "r") as file:
        return [int(x) for x in file.read().split(',')]


def spawn_lanternfish(initial_ages: list[int], days: int) -> int:
    # Create a list where the index is the age (0-8) and the value is the count
    # of fish at that age.
    counts = [initial_ages.count(i) for i in range(9)]

    for _ in range(days):
        # How many fish are ready to create new ones?
        spawning_lanternfish = counts[0]

        # Shift everyone down by one day (1->0, 2->1, etc.). counts[0] is
        # effectively removed here
        counts = counts[1:] + [0]

        # The fish that just spawned reset to age 6
        counts[6] += spawning_lanternfish

        # The new babies start at age 8
        counts[8] += spawning_lanternfish

    return sum(counts)


def part_one(data: list[int]) -> int:
    return spawn_lanternfish(data, 80)


def part_two(data: list[int]) -> int:
    return spawn_lanternfish(data, 256)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 360610
    print("Part 2:", part_two(data))  # 1631629590423
