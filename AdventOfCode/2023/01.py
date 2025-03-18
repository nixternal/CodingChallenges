#!/usr/bin/env python

import os
import re


def parse_input() -> list:
    """
    Reads the input file and splits the contents into a list of lines.

    Returns:
        list: A list of strings, where each string is line from the input file.
    """

    with open(
            os.path.splitext(os.path.basename(__file__))[0] + '.in',
            'r') as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Processes the input data to compute a sum based on the first and last
    integers found in each line.

    Steps:
        1. Iterates through each line in the input data.
        2. Extracts numeric characters from the line.
        3. Forms a number by combining the first & last digits & adds this to
           the sum.

    Args:
        data (list): Lines of input data

    Returns:
        int: The computed sum of numbers formed from "Steps: #3"
    """

    # sum = 0
    # for line in data:
    #     a = []
    #     for char in line:
    #         try:
    #             a.append(int(char))
    #         except ValueError:
    #             pass
    #     sum += int(f"{a[0]}{a[-1]}")
    # return sum

    # Above logic converted in to list comprehension
    return sum(
            int(f"{digits[0]}{digits[-1]}")
            for line in data
            if (digits := [int(char) for char in line if char.isdigit()])
            )


def part_two(data: list) -> int:
    """
    Processes the input data to replace specific words representing numbers
    (e.g., "one", "two") with their numeric equivalents, then calculates the
    sum using logic from part_one().

    Steps:
        1. Uses a regex to match either digits or specific words for numbers.
        2. Replaces matching words with their numeric equivalents.
        3. Passes the transformed data to part_one for computation

    Args:
        data (list): Lines of input data

    Returns:
        int: The computed sum after transforming and processing the data.
    """

    nums = "one|two|three|four|five|six|seven|eight|nine"
    # Match digits or specific words
    nums_re = re.compile(r"(?=(\d|{}))".format(nums))
    nums_list = nums.split("|")

    # new_data = []
    # for line in data:
    #     new_line = []
    #     for num in nums_re.findall(line):
    #         if num in nums:
    #             num = str(nums.index(num) + 1)
    #         new_line.append(num)
    #     new_data.append(new_line)
    # return part_one(new_data)

    # Above logic converted in to list comprehension
    transformed_data = [
            "".join(
                str(nums_list.index(num) + 1) if num in nums_list else num
                for num in nums_re.findall(line)
            )
            for line in data
        ]
    return part_one(transformed_data)


if __name__ == "__main__":
    data = parse_input()
    print("Part 1:", part_one(data))  # 53651
    print("Part 2:", part_two(data))  # 53894
