#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("03.in", "r") as file:
        return [list(map(int, line.split())) for line in file]


def is_valid_triangle(sides: list) -> bool:
    a, b, c = sorted(sides)
    return a + b > c


def part_one(data: list) -> int:
    # Initialize counter
    valid = 0

    for sides in data:
        if is_valid_triangle(sides):
            valid += 1

    return valid


def part_two(data: list) -> int:
    # Initialize counter
    valid = 0

    # Process in groups of 3 rows at a time
    for i in range(0, len(data), 3):
        # Take the 3 rows
        group = data[i:i+3]

        # Transpose the group to extract columns as triangles
        for col in range(3):
            triangle = [group[0][col], group[1][col], group[2][col]]
            if is_valid_triangle(triangle):
                valid += 1

    return valid


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 982
    print("Part 2:", part_two(data))  # 1826
