#!/usr/bin/env python

import json
import re


def hook(obj: dict) -> dict:
    if "red" in obj.values():
        return {}
    else:
        return obj


def read_puzzle_input() -> str:
    with open("12.in", "r") as file:
        return file.read()


def part_one(data: str) -> int:
    return sum(map(int, re.findall(r"-?\d+", data)))


def part_two(data: str) -> int:
    d = str(json.loads(data, object_hook=hook))
    return sum(map(int, re.findall(r"-?\d+", d)))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 191164
    print("Part 1:", part_two(data))  # 87842
