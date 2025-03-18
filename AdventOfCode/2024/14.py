#!/usr/bin/env python

import math
import re

WIDTH = 101
HEIGHT = 103

PRINT_TREE = True


def read_puzzle_input() -> list:
    robots = []
    with open("14.in", "r") as file:
        lines = file.read().splitlines()
    for line in lines:
        px, py, vx, vy = tuple(map(int, re.findall(r'-?\d+', line)))
        robots.append((px, py, vx, vy))
    return robots


def safety_factor(robots: list[tuple[int, int]]) -> int:
    quadrants = [0] * 4
    for fx, fy in robots:
        hw = WIDTH // 2  # Half Width
        hh = HEIGHT // 2  # Half Height
        if fx < hw:
            if fy < hh:
                quadrants[0] += 1
            if fy > hh:
                quadrants[1] += 1
        elif fx > hw:
            if fy < hh:
                quadrants[2] += 1
            if fy > hh:
                quadrants[3] += 1
    return math.prod(quadrants)


def part_one(data: list[tuple[int, int, int, int]]) -> int:
    robots = []
    for px, py, vx, vy in data:
        fx = (px + (vx * 100)) % WIDTH
        fy = (py + (vy * 100)) % HEIGHT
        robots.append((fx, fy))
    return safety_factor(robots)


def part_two(data: list) -> int:
    t = []  # Over time
    sf = []  # Safety Factors
    best_snap = []
    min_score = 1e10
    best_frame = 0
    for i in range(10000):
        snap = []
        for px, py, vx, vy in data:
            fx = (px + (vx * i)) % WIDTH
            fy = (py + (vy * i)) % HEIGHT
            snap.append((fx, fy))
        t.append(i)
        sfs = safety_factor(snap)
        sf.append(sfs)
        if sfs < min_score:
            best_snap = snap[:]
            min_score = sfs
            best_frame = i

    if PRINT_TREE:
        for y in range(HEIGHT):
            if 20 < y <= 53:
                for x in range(WIDTH):
                    if 22 < x < 54:
                        if (x, y) in best_snap:
                            print("#", end="")
                        else:
                            print(".", end="")
                print()

    return best_frame


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 210587128
    print("Part 2:", part_two(data))  # 7286
