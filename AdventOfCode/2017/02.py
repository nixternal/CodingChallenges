#!/usr/bin/env python


def read_puzzle_input() -> list:
    """
    Read and parse the puzzle input from a file named '02.in'.

    The input file should contain rows of space-separated integers.
    Each line is converted into a list of integers.

    Returns:
        List[List[int]]: A 2D list where each inner list contains
        the integers from one line of the input file.

    Example:
        If 02.in contains:
        5 1 9 5
        7 5 3
        2 4 6 8

        The function returns: [[5,1,9,5], [7,5,3], [2,4,6,8]]
    """

    with open("02.in", "r") as file:
        return [[int(num) for num in line.strip().split()] for line in file]


def part_one(data: list) -> int:
    """
    Calculate the checksum based on the difference between the largest
    and smallest numbers in each row.

    Args:
        data (List[List[int]]): A 2D list of integers where each inner list
            represents a row of numbers.

    Returns:
        int: The sum of the differences between the maximum and minimum
        values in each row.

    Example:
        >>> part_one([[5,1,9,5], [7,5,3], [2,4,6,8]])
        18  # (9-1) + (7-3) + (8-2) = 8 + 4 + 6 = 18
    """

    return sum(max(line) - min(line) for line in data)


def part_two(data: list) -> int:
    """
    Calculate the checksum based on finding pairs of evenly divisible numbers
    in each row and summing their quotients.

    For each row, find the only two numbers where one evenly divides the other
    (division results in a whole number with no remainder) and add the result
    of the division to the checksum.

    Args:
        data (List[List[int]]): A 2D list of integers where each inner list
            represents a row of numbers.

    Returns:
        int: The sum of all evenly divisible quotients found in each row.

    Example:
        >>> part_two([[5,9,2,8], [9,4,7,3], [3,8,6,5]])
        9  # In first row: 8/2 = 4, in second row: none, in third row: 6/3 = 2
            # Total: 4 + 0 + 2 = 6
    """

    checksum = []
    for line in data:
        for i in range(len(line)):
            for j in range(len(line)):
                if line[i] != line[j] and line[i] % line[j] == 0:
                    checksum.append(line[i] // line[j])
    return sum(checksum)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 44887
    print("Part 2:", part_two(data))  # 242
