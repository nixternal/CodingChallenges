#!/usr/bin/env python


CREATURES = {"x": 0, "A": 0, "B": 1, "C": 3, "D": 5}


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """Sum potions for individual creatures"""
    return sum(CREATURES[c] for c in data[0])


def part_two(data: list) -> int:
    """Sum potions for creature pairs with bonuses"""
    potions = 0
    line = data[1]

    for i in range(0, len(line), 2):
        pair = line[i : i + 2]

        # Add base potion costs
        potions += sum(CREATURES[c] for c in pair)

        # Add bonus: 2 if no 'x', 0 if any 'x'
        potions += 2 if "x" not in pair else 0

    return potions


def part_three(data: list) -> int:
    """Sum potions for creatures pairs & groups with bonuses"""
    potions = 0
    line = data[2]

    for i in range(0, len(line), 3):
        group = line[i : i + 3]

        # Add base costs
        potions += sum(CREATURES[c] for c in group)

        # Add bonus: 6 if no 'x', 2 if one 'x', 0 if two or more 'x'
        xct = group.count("x")
        potions += 6 if xct == 0 else 2 if xct == 1 else 0

    return potions


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1359
    print("Part 2:", part_two(data))  # 5600
    print("Part 3:", part_three(data))  # 28105
