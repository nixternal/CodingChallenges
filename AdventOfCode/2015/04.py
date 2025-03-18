#!/usr/bin/env python

from functools import cache

import hashlib
import re


@cache
def find_hash(secret: str, regex: str) -> int:
    hex = hashlib.md5(data.encode("utf-8")).hexdigest()
    i = 0
    while not re.match(regex, hex):
        i += 1
        hex = hashlib.md5(f"{data}{i}".encode("utf-8")).hexdigest()
    return i


def part_one(data: str) -> int:
    return find_hash(data, r"^00000\d")


def part_two(data: str) -> int:
    return find_hash(data, r"^000000")


if __name__ == "__main__":
    data = 'bgvyzdsv'
    print("Part 1:", part_one(data))  # 254575
    print("Part 2:", part_two(data))  # < 47134621
