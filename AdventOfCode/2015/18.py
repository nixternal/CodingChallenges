#!/usr/bin/env python

import numpy as np


def read_puzzle_input() -> str:
    with open("18.in", "r") as file:
        return file.read()


def part_one(data):
    # Parse input and convert to a boolean grid
    g = np.array([list(line) for line in data.split('\n') if line]) == '#'

    def update(grid):
        c = np.pad(grid, pad_width=1, mode='constant', constant_values=False)
        offsets = [
            (-1, -1), (-1, 0), (-1, 1), (0, 1),
            (1, 1), (1, 0), (1, -1), (0, -1)
        ]

        nb = sum(
            np.roll(np.roll(c, dx, axis=0), dy, axis=1)[1:-1, 1:-1]
            for dx, dy in offsets
        )

        # Apply rules
        return (grid & ((nb == 2) | (nb == 3))) | (~grid & (nb == 3))

    # Run 100 iterations
    for _ in range(100):
        g = update(g)

    return np.sum(g)


def part_two(data):
    # Parse input and convert to a boolean grid
    g = np.array([list(line) for line in data.split('\n') if line]) == '#'

    # Force the corners to be active
    g[0, 0] = g[0, -1] = g[-1, 0] = g[-1, -1] = True

    def update(grid):
        c = np.pad(grid, pad_width=1, mode='constant', constant_values=False)
        offsets = [
            (-1, -1), (-1, 0), (-1, 1), (0, 1),
            (1, 1), (1, 0), (1, -1), (0, -1)
        ]

        nb = sum(
            np.roll(np.roll(c, dx, axis=0), dy, axis=1)[1:-1, 1:-1]
            for dx, dy in offsets
        )

        # Apply rules
        ng = (grid & ((nb == 2) | (nb == 3))) | (~grid & (nb == 3))

        # Force the corners to remain active
        ng[0, 0] = ng[0, -1] = ng[-1, 0] = ng[-1, -1] = True

        return ng

    # Run 100 iterations
    for _ in range(100):
        g = update(g)

    return np.sum(g)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 814
    print("Part 2:", part_two(data))  # 924
