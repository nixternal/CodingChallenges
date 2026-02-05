#!/usr/bin/env python

import math


def read_puzzle_input() -> list:
    with open("06.in", "r") as file:
        return file.read().splitlines()


def count_winning_ways(time: int, record: int) -> int:
    """
    Calculate winning hold times using quadratic formula

    Distance = hold_time * (time - hold_time) = -hold_time^2 + time * hold_time
    We need: -h^2 + th > record
    Solving: h^2 -th + record < 0
    """
    # Quadratic formula for boundary points
    discriminant = time * time - 4 * record
    if discriminant <= 0:
        return 0

    sqrt_disc = math.sqrt(discriminant)
    h1 = (time - sqrt_disc) / 2
    h2 = (time + sqrt_disc) / 2

    # Count integers in the open interval (h1, h2)
    return int(h2)- int(h1) - (1 if h2 == int(h2) else 0)

def parse_numbers(line: str) -> list[int]:
    """Extract all integers from a line."""
    return [int(x) for x in line.split(':')[1].split()]


def parse_single_number(line: str) -> int:
    """Join and parse as single integer."""
    return int(line.split(':')[1].replace(' ', ''))


def part_one(data: list) -> int:
    times, records = map(parse_numbers, data)
    return math.prod(count_winning_ways(t, r) for t, r in zip(times, records))


def part_two(data: list) -> int:
    time, record = map(parse_single_number, data)
    return count_winning_ways(time, record)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1312850
    print("Part 2:", part_two(data))  # 36749103
