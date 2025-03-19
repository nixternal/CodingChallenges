#!/usr/bin/env python

import re
import statistics
from functools import lru_cache

# @lru_cache: cache functions to avoid recalculating the same values repeatedly


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named "02.in" and returns its content
    as a list of lines.

    Returns:
        list: A list of strings, each representing a line from the input file.
    """

    with open("02.in", "r") as file:
        return file.read().splitlines()


@lru_cache(maxsize=None)
def A(a: int, b: int) -> int:
    """
    Adds two integers together.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The sum of a and b.
    """

    return a + b


@lru_cache(maxsize=None)
def B(a: int, b: int) -> int:
    """
    Multiplies two integers together.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The product of a and b.
    """

    return a * b


@lru_cache(maxsize=None)
def C(base: int, exponent: int) -> int:
    """
    Raises a base to a given exponent.

    Args:
        base (int): The base number.
        exponent (int): The exponent to raise the base to.

    Returns:
        int: The result of base ** exponent.
    """

    return base ** exponent


def extract_function_params(data: list) -> tuple:
    """
    Extracts function parameters and a list of qualities from the input data.

    Args:
        data (list): The list of strings from the input file.

    Returns:
        tuple: A tuple containing three function parameters
               (funcA, funcB, funcC) and a list of qualities.
    """

    funcA = int(re.findall(r'\d+', data[0])[0])
    funcB = int(re.findall(r'\d+', data[1])[0])
    funcC = int(re.findall(r'\d+', data[2])[0])
    qualities = [int(x) for x in data[4:]]
    return funcA, funcB, funcC, qualities


def calculate_total(value: int, funcA: int, funcB: int, funcC: int) -> int:
    """
    Applies a series of mathematical operations on the given value using the
    extracted parameters.

    The calculation follows this order: C -> B -> A

    Args:
        value (int): The input value to modify.
        funcA (int): Addition parameter.
        funcB (int): Multiplication parameter.
        funcC (int): Exponentiation parameter.

    Returns:
        int: The final computed value.
    """

    return A(B(C(value, funcC), funcB), funcA)


def part_one(funcA: int, funcB: int, funcC: int, qualities: list) -> int:
    """
    Computes the total value based on the median of the qualities list.

    Args:
        funcA (int): Addition parameter.
        funcB (int): Multiplication parameter.
        funcC (int): Exponentiation parameter.
        qualities (list): List of integer values.

    Returns:
        int: The computed total based on the median quality value.
    """

    median = statistics.median(qualities)
    return calculate_total(median, funcA, funcB, funcC)


def part_two(funcA: int, funcB: int, funcC: int, qualities: list) -> int:
    """
    Computes the total value based on the sum of all even values in the
    qualities list.

    Args:
        funcA (int): Addition parameter.
        funcB (int): Multiplication parameter.
        funcC (int): Exponentiation parameter.
        qualities (list): List of integer values.

    Returns:
        int: The computed total based on the sum of even values.
    """

    even_sum = sum(q for q in qualities if q % 2 == 0)
    return calculate_total(even_sum, funcA, funcB, funcC)


def part_three(funcA: int, funcB: int, funcC: int, qualities: list) -> int:
    """
    Finds the maximum value from qualities such that its computed total does
    not exceed a set limit.

    Uses binary search if the qualities list is sorted; otherwise, performs a
    linear search.

    Args:
        funcA (int): Addition parameter.
        funcB (int): Multiplication parameter.
        funcC (int): Exponentiation parameter.
        qualities (list): List of integer values.

    Returns:
        int: The maximum value within the limit.
    """

    client_pecunia = 15_000_000_000_000

    # Find maximum value that doesn't exceed client_pecunia
    # Use binary search for efficiency if qualities are sorted
    if sorted(qualities) == qualities:
        # Binary search implementation
        left, right = 0, len(qualities) - 1
        while left <= right:
            mid = (left + right) // 2
            if calculate_total(
                    qualities[mid], funcA, funcB, funcC) <= client_pecunia:
                left = mid + 1
            else:
                right = mid - 1
        return qualities[right] if right >= 0 else 0
    else:
        # Linear search for unsorted list
        return max(
            (q for q in qualities if calculate_total(
                q, funcA, funcB, funcC) <= client_pecunia), default=0)


if __name__ == "__main__":
    data = read_puzzle_input()
    a, b, c, qualities = extract_function_params(data)
    print("Part 1:", part_one(a, b, c, qualities))    # 10847350540445
    print("Part 2:", part_two(a, b, c, qualities))    # 1309497166479306596
    print("Part 3:", part_three(a, b, c, qualities))  # 5698
