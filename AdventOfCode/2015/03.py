#!/usr/bin/env python

DIRS = {"^": [1, 0], ">": [0, 1], "v": [-1, 0], "<": [0, -1]}


def read_puzzle_input() -> str:
    with open("03.in", "r") as file:
        return file.read().strip()


def part_one(data: str) -> int:
    pos = [0, 0]
    visited = [pos]

    for move in data:
        pos = [pos[0] + DIRS[move][0], pos[1] + DIRS[move][1]]
        if pos not in visited:
            visited.append(pos)

    return len(visited)


def part_two(data: str) -> int:
    santa = [0, 0]
    robosanta = [0, 0]
    visited = [[0, 0]]

    for turn, move in enumerate(data, 1):
        if turn % 2 == 0:
            santa = [santa[0] + DIRS[move][0], santa[1] + DIRS[move][1]]
            if santa not in visited:
                visited.append(santa)
        else:
            robosanta = [robosanta[0] + DIRS[move][0],
                         robosanta[1] + DIRS[move][1]]
            if robosanta not in visited:
                visited.append(robosanta)

    return len(visited)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2565
    print("Part 2:", part_two(data))  # 2639
