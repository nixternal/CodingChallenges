#!/usr/bin/env python

from collections import defaultdict


def read_puzzle_input(filename: str = "01.in") -> list[str]:
    with open(filename, encoding="utf-8") as file:
        return file.read().strip().split("\n\n")


def get_component_value(component: str) -> int:
    bits = "".join("1" if char.isupper() else "0" for char in component)
    return int(bits, 2)


def part_one(section: str) -> int:
    total = 0

    for line in section.splitlines():
        identifier, components = line.split(":", 1)
        red, green, blue = map(
            get_component_value,
            components.split(),
        )

        if green > red and green > blue:
            total += int(identifier)

    return total


def part_two(section: str) -> int:
    scales = []

    for line in section.splitlines():
        identifier, components = line.split(":", 1)
        red, green, blue, shine = map(
            get_component_value,
            components.split(),
        )

        scales.append(
            (
                int(identifier),
                red + green + blue,
                shine,
            )
        )

    darkest_most_shiny = min(
        scales,
        key=lambda scale: (-scale[2], scale[1]),
    )

    return darkest_most_shiny[0]


def part_three(section: str) -> int:
    groups = defaultdict(list)

    for line in section.splitlines():
        identifier, components = line.split(":", 1)
        red, green, blue, shine = map(
            get_component_value,
            components.split(),
        )

        if shine <= 30:
            shine_group = "matte"
        elif shine >= 33:
            shine_group = "shiny"
        else:
            continue

        if red > green and red > blue:
            color_group = "red"
        elif green > red and green > blue:
            color_group = "green"
        elif blue > red and blue > green:
            color_group = "blue"
        else:
            continue

        groups[f"{color_group}-{shine_group}"].append(int(identifier))

    largest_group = max(groups.values(), key=len)
    return sum(largest_group)


if __name__ == "__main__":
    puzzle_parts = read_puzzle_input()

    print("Part 1:", part_one(puzzle_parts[0]))    # 67944
    print("Part 2:", part_two(puzzle_parts[1]))    # 30403
    print("Part 3:", part_three(puzzle_parts[2]))  # 10973041
