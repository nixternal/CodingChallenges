#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    with open("05.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    nice = 0
    for line in data:
        if len(re.findall(r"[aeiou]", line)) < 3:
            continue
        if not re.findall(r"(.)\1", line):
            continue
        if re.findall(r"ab|cd|pq|xy", line):
            continue
        nice += 1

    return nice


def part_two(data: list) -> int:
    nice = 0
    for line in data:
        if not re.findall(r"([a-z]{2}).*?(\1)", line):
            continue
        if not re.findall(r"(.)*?(.)\1", line):
            continue
        nice += 1
    return nice


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 255
    print("Part 2:", part_two(data))  # 55
