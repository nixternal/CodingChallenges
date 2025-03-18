#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("04.in", "r") as file:
        data = file.read()
    return data.split()


def part_one() -> int:
    """
    Look for XMAS in the page of letters provided. Horizontally, Vertically,
    Diagonally, Forwards & Backwards, find the letters XMAS together

    :return: The amount of times XMAS was found
    :rtype: int
    """
    W = read_puzzle_input()
    XMAS = ["XMAS", "SAMX"]
    count = 0
    for R in range(len(W)):
        for C in range(len(W[R])):
            # Horizontal
            if (C + 3 < len(W[R]) and
                    f"{W[R][C]}{W[R][C+1]}{W[R][C+2]}{W[R][C+3]}" in XMAS):
                count += 1
            # Vertical
            if (R + 3 < len(W) and
                    f"{W[R][C]}{W[R+1][C]}{W[R+2][C]}{W[R+3][C]}" in XMAS):
                count += 1
            # Diagonal
            if (R + 3 < len(W) and C + 3 < len(W[R]) and
                    f"{W[R][C]}{W[R+1][C+1]}{W[R+2][C+2]}{W[R+3][C+3]}" in
                    XMAS):
                count += 1
            # Anti-Diagonal
            if (R + 3 < len(W) and C - 3 >= 0 and
                    f"{W[R][C]}{W[R+1][C-1]}{W[R+2][C-2]}{W[R+3][C-3]}" in
                    XMAS):
                count += 1
    return count


def part_two() -> int:
    """
    Look for X-MAS, that is the letters MAS in an X pattern, both forwards and
    backwards.

    :return: The amount of times MAS was found in an X pattern
    :rtype: int
    """
    W = read_puzzle_input()
    MAS = ["MAS", "SAM"]
    count = 0
    for R in range(len(W)):
        for C in range(len(W[R])):
            if (C - 1 >= 0 and R - 1 >= 0 and
                R + 1 < len(W) and C + 1 < len(W[R]) and
                f"{W[R-1][C-1]}{W[R][C]}{W[R+1][C+1]}" in MAS and
                    f"{W[R-1][C+1]}{W[R][C]}{W[R+1][C-1]}" in MAS):
                count += 1
    return count


if __name__ == "__main__":
    print("Part 1:", part_one())  # 2549
    print("Part 2:", part_two())  # 2003
