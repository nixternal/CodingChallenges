#!/usr/bin/env python

from dataclasses import dataclass


def read_puzzle_input() -> list[str]:
    with open("05.in") as f:
        return f.read().split("\n\n")


@dataclass
class Sword:
    id: int
    quality: int
    levels: list[int]


def parse_sword(line: str) -> Sword:
    """Parse 'id:n1,n2,n3...' into a Sword with quality and levels."""
    sword_id, nums = line.split(":")
    values = [int(x) for x in nums.split(",")]

    # Build spine segments: each is [value, left, right]
    spine = [[values[0], None, None]]

    for val in values[1:]:
        placed = False
        for seg in spine:
            if val < seg[0] and seg[1] is None:
                seg[1] = val
                placed = True
                break
            elif val > seg[0] and seg[2] is None:
                seg[2] = val
                placed = True
                break
        if not placed:
            spine.append([val, None, None])

    # Calculate quality (concatenate spine values)
    quality = int("".join(str(seg[0]) for seg in spine))

    # Calculate levels (left + center + right for each segment)
    levels = [int("".join(str(x) for x in seg if x is not None)) for seg in spine]

    return Sword(int(sword_id), quality, levels)


def part_one(data: list[str]) -> int:
    """Compute quality of a single sword."""
    return parse_sword(data[0]).quality


def part_two(data: list[str]) -> int:
    """Find difference between strongest and weakest swords."""
    swords = [parse_sword(line) for line in data[1].splitlines()]
    qualities = [s.quality for s in swords]
    return max(qualities) - min(qualities)


def part_three(data: list[str]) -> int:
    """Sort swords and compute position-weighted checksum."""
    swords = [parse_sword(line) for line in data[2].splitlines()]

    # Sort by quality desc, then levels desc, then id desc
    swords.sort(key=lambda s: (s.quality, s.levels, s.id), reverse=True)

    return sum((i + 1) * s.id for i, s in enumerate(swords))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3768545768
    print("Part 2:", part_two(data))  # 8608639867112
    print("Part 3:", part_three(data))  # 31241249
