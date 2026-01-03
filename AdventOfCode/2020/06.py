#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("06.in", "r") as file:
        return file.read().strip().split("\n\n")


def part_one(data: list) -> int:
    count = 0
    for group in data:
        count += len(set(group.replace("\n", "")))
    return count


def part_two(data: list) -> int:
    total = 0
    for group in data:
        people = group.split("\n")

        # Start with the 1st person's answers
        common = set(people[0])

        # Intersect with each other person's answers
        for person in people[1:]:
            common &= set(person)

        total += len(common)
    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 6387
    print("Part 2:", part_two(data))  # 3039
