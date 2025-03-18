#!/usr/bin/env python


def read_puzzle_input() -> tuple[list, list]:
    """
    Read the file and split each line & append to left & right lists. Each line
    looks similar to the following in the "input.txt" file in the same
    directory:

        1    3
        3    5
        7    2

    :return: 2 lists, the left & the right
    :rtype: tuple[list, list]
    """
    left = []
    right = []
    with open("01.in", "r") as file:
        for line in file:
            l, r = line.strip().split()
            left.append(l)
            right.append(r)
    return (left, right)


def part_one(left: list, right: list) -> int:
    """
    Find the total distance between the left & the right list, add up the
    distances between all of the pairs you found. Sort the lists to compare
    each lists smallest number.

    :param list left: The list of numbers on the left half of the input file.
    :param list right: The list of numbers on the right half of the input file.
    :return: Sum of the total distances between both lists
    :rtype: int
    """
    left.sort()
    right.sort()
    sum = 0
    for i in range(len(left)):
        sum += abs(int(left[i]) - int(right[i]))
    return sum


def part_two(left: list, right: list) -> int:
    """
    Find the similarity scores between the 2 lists, and multiply that number
    by the amount of times it is found in the other list, then sum all of those
    numbers to get the overall similarity score.

    :param list left: The list of numbers on the left half of the input file.
    :param list right: The list of numbers on the right half of the input file.
    :return: Sum of the similarity scores of the lists.
    :rtype: int
    """
    sum = 0
    for x in left:
        sum += int(x) * right.count(x)
    return sum


if __name__ == "__main__":
    left, right = read_puzzle_input()
    print("Part 1:", part_one(left, right))  # 1530215
    print("Part 2:", part_two(left, right))  # 26800609
