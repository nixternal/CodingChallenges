#!/usr/bin/env python

from operator import add, mul

import re


def read_puzzle_input() -> list:
    """
    Read the file and create a list.

    :return: A list that contains stuff
    :rtype: list
    """
    with open("07.in", "r") as file:
        return [[int(num) for num in re.findall(r"\d+", line)]for line in file]


def calibration(funcs, result: int, total: int, *args) -> bool:
    if args:
        for func in funcs:
            if calibration(funcs, result, func(total, args[0]), *args[1:]):
                return True
        return False
    else:
        return result == total


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def part_one(data: list) -> int:
    """
    Calculate & return the total calibration result

    :param list data: Data to be used
    :return: Sum of acceptable calibrations
    :rtype: int
    """
    return sum(calib[0] for calib in data if calibration((add, mul), *calib))


def part_two(data: list) -> int:
    """
    Use the || concat operator and recalculate the total calibration result

    :param list data: Data to be used
    :return: Sum of acceptable calibrations
    :rtype: int
    """
    return sum(calib[0] for calib in data
               if calibration((add, mul, concat), *calib))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3245122495150
    print("Part 2:", part_two(data))  # 105517128211543
