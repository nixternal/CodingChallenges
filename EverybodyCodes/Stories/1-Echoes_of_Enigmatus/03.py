#!/usr/bin/env python
from math import gcd


def read_puzzle_input() -> list:
    """Read and split the input file into three sections separated by blank lines."""
    with open("03.in", "r") as file:
        return file.read().split("\n\n")


def parse_snails(data: str) -> list[tuple[int, int]]:
    """Parse a block of 'x=N y=M' lines into a list of (x, y) tuples."""
    snails = []
    for line in data.strip().splitlines():
        parts = line.split()
        x = int(parts[0].split("=")[1])
        y = int(parts[1].split("=")[1])
        snails.append((x, y))
    return snails


def advance(x: int, y: int, days: int) -> tuple[int, int]:
    """
    Advance a snail by `days` steps along its disc.

    Since disc = x + y - 1 is invariant (a snail never changes discs), movement
    is pure modular arithmetic along the diagonal. The snail's 0-indexed position
    is (x - 1), and it advances by 1 each day, wrapping modulo disc size.
    """
    disc = x + y - 1
    pos = (x - 1 + days) % disc  # 0-indexed position along the diagonal
    return pos + 1, disc - pos  # convert back to (x, y)


def score(snails: list[tuple[int, int]], days: int) -> int:
    """
    Advance all snails by `days` and return the sum of x + days*y for each.
    """
    total = 0
    for x, y in snails:
        nx, ny = advance(x, y, days)
        total += nx + days * ny
    return total


def golden_alignment(snails: list[tuple[int, int]]) -> int:
    """
    Find the first day all snails are simultaneously on the golden line (y=1).

    Each snail on disc d returns to y=1 with period d. The snail at (x, y)
    first hits y=1 after r = (d - x) % d days. We need the smallest t > 0
    satisfying t ≡ r (mod d) for every snail — a classic Chinese Remainder
    Theorem (CRT) problem.

    We solve it iteratively: maintain a running solution (t, lcm) that satisfies
    all constraints seen so far. For each new constraint, step t forward by the
    current lcm until it satisfies the new modulus, then update lcm = lcm/gcd*d.
    """
    t, lcm = 0, 1
    for x, y in snails:
        d = x + y - 1  # disc size = period for this snail
        r = (d - x) % d  # days until this snail first reaches y=1

        g = gcd(lcm, d)
        if (r - t) % g != 0:
            raise ValueError("No solution exists (incompatible constraints)")
        step = lcm // g * d
        while t % d != r:
            t += lcm
        lcm = step

    # t=0 only if all snails start on the golden line; return full period instead
    return t if t > 0 else lcm


def part_one(data: list) -> int:
    snails = parse_snails(data[0])
    return score(snails, 100)


def part_two(data: list) -> int:
    snails = parse_snails(data[1])
    return golden_alignment(snails)


def part_three(data: list) -> int:
    snails = parse_snails(data[2])
    return golden_alignment(snails)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3642
    print("Part 2:", part_two(data))  # 1043934
    print("Part 3:", part_three(data))  # 90550686296
