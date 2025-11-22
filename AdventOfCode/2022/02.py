#!/usr/bin/env python

SHAPE = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
SCORE = {0: 1, 1: 2, 2: 3}
OUTCOME = {"X": 0, "Y": 3, "Z": 6}


def read_puzzle_input() -> list:
    with open("02.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    shape = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
    score = {0: 1, 1: 2, 2: 3}
    total = 0
    for line in data:
        e, y = line.split()
        elf = shape[e]
        you = shape[y]

        # Determine outcome
        result = (you - elf) % 3
        if result == 0:  # Draw
            outcome = 3
        elif result == 1:  # Win
            outcome = 6
        else:  # You Lose!
            outcome = 0

        total += score[you] + outcome

    return total


def part_two(data: list) -> int:
    total = 0
    for line in data:
        e, y = line.split()
        elf = SHAPE[e]
        outcome = OUTCOME[y]

        if y == "Y":  # draw
            x = elf
        elif y == "Z":  # win
            x = (elf + 1) % 3
        else:  # lose
            x = (elf - 1) % 3

        total += SCORE[x] + outcome

    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10994
    print("Part 2:", part_two(data))  # 12526
