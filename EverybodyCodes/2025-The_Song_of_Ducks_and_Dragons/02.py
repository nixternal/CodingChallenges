#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    with open("02.in", "r") as file:
        return file.read().splitlines()


def iterate_mandelbrot(R, A, iterations, divisor):
    """Optimized Mandelbrot-style iteration."""
    for _ in range(iterations):
        R = R * R
        R = complex(int(R.real / divisor), int(R.imag / divisor))
        R += A
    return R


def is_bounded(P, iterations=100, divisor=100_000, bound=1_000_000):
    """Check if point remains bounded after iterations."""
    R = 0j
    for _ in range(iterations):
        R = R * R
        R = complex(int(R.real / divisor), int(R.imag / divisor))
        R += P
        # Early exit if unbounded
        if not (-bound <= R.real <= bound and -bound <= R.imag <= bound):
            return False
    return True


def part_one(data: list) -> str:
    nums = list(map(int, re.findall(r"\d+", data[0])))
    A = complex(nums[0], nums[1])
    R = iterate_mandelbrot(0j, A, 3, 10)
    return f"[{int(R.real)},{int(R.imag)}]"


def part_two(data: list) -> int:
    nums = list(map(int, re.findall(r"-?\d+", data[1])))
    A = complex(nums[0], nums[1])

    count = 0
    for real in range(101):
        for imag in range(101):
            P = complex(A.real + real * 10, A.imag + imag * 10)
            if is_bounded(P):
                count += 1

    return count


def part_three(data: list) -> int:
    nums = list(map(int, re.findall(r"-?\d+", data[1])))
    A = complex(nums[0], nums[1])

    count = 0
    for real in range(1001):
        for imag in range(1001):
            P = complex(A.real + real, A.imag + imag)
            if is_bounded(P):
                count += 1

    return count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # [107568,965966]
    print("Part 2:", part_two(data))  # 1177
    print("Part 3:", part_three(data))  # 115262
