#!/usr/bin/env python
"""
This script solves a puzzle by dividing a list of weights (integers) into
subsets of equal total weight. It calculates the "quantum entanglement" of
the smallest subset that meets this condition.

Key Functions:
- Read input from a file
- Generate all combinations of a given size
- Calculate the product of elements in an iterable
- Find subsets of weights that meet a specific weight distribution
"""


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '24.in'.
    Assumes each line in the file contains an integer weight.

    Returns:
        list: A list of integers representing the weights.
    """

    with open("24.in", "r") as file:
        return list(map(int, file.readlines()))


def product(iterable):
    """
    Calculates the product of all elements in an iterable.
    This is equivalent to multiplying all numbers together.

    Args:
        iterable (iterable): A collection of numbers.

    Returns:
        int: The product of all elements.
    """
    result = 1
    for x in iterable:
        result *= x
    return result


def combinations(data, n):
    """
    Generates all combinations of size `n` from the input list `data`.
    This is a recursive implementation of the combinations algorithm.

    Args:
        data (list): The list of items to generate combinations from.
        n (int): The size of each combination.

    Yields:
        list: A combination of `n` elements.
    """

    if n == 0:  # Base case: If n is 0, yield an empty combination
        yield []
    elif len(data) < n:  # If data items < n, no combos are possible
        return
    else:
        # Recursive case: Include the first element in the combination
        for combo in combinations(data[1:], n - 1):
            yield [data[0]] + combo

        # Recursive case: Exclude the first element in the combination
        for combo in combinations(data[1:], n):
            yield combo


def balance(data: list, k: int) -> int:
    """
    Finds the smallest subset of weights such that:
    1. The sum of the subset equals the total weight divided by `k`.
    2. Returns the minimum "quantum entanglement" (product of elements in the
       subset).

    Args:
        data (list): A list of integers representing weights.
        k (int): The number of groups to divide the weights into.

    Returns:
        int: The minimum quantum entanglement of the smallest valid subset.
    """

    # Calculate the target weight for each group
    target_weight = sum(data) / k
    subsets = []  # To store valid subsets
    i = 2  # Start with subsets of size 2

    # Find the smallest subsets whose sum equals the target weight
    while not subsets:
        subsets = [
            subset for subset in
            combinations(data, i)
            if sum(subset) == target_weight
        ]
        i += 1

    # Calculate the quantum entanglement of each subset and return the smallest
    return min(product(subset) for subset in subsets)


def part_one(data: list) -> int:
    return balance(data, 3)


def part_two(data: list) -> int:
    return balance(data, 4)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10723906903
    print("Part 2:", part_two(data))  # 74850409
