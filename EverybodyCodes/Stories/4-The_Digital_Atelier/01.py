#!/usr/bin/env python
"""Recamán-style ornament puzzle.

Each line of the notes is a list of jump lengths. Starting at point 0 on a
number line, every jump is applied in order, and the answer for each part is
the sum of the final points of all sequences in that part's block of input.

Input format (01.in): three blocks separated by a blank line, one per part.

Rules, cumulative across parts:
    Part 1: Try to jump backward. If the landing point is positive and not
            yet visited, take it. Otherwise jump forward.
    Part 2: As part 1, but a forward landing on a visited point is bumped up
            by one until an unvisited point is found.
    Part 3: As part 2, but arcs may never cross. Arcs alternate between
            below and above the line, and a skipped jump draws no arc.
            A backward jump that would cross is replaced by a forward jump.
            A forward jump that would cross is lengthened until it is valid.
            If no forward jump is valid, the jump is skipped entirely.
"""

from collections.abc import Callable


def read_puzzle_input(path: str = "01.in") -> list[str]:
    """Return the puzzle input as one text block per part."""
    with open(path, "r") as file:
        return file.read().strip().split("\n\n")


def parse_line(line: str) -> list[int]:
    """Convert a line like '1,2,3' into [1, 2, 3]."""
    return [int(x) for x in line.split(",")]


def recaman_sequence(jumps: list[int]) -> int:
    """Part 1: return the final point after applying all jumps.

    Backward if the target is positive and unvisited, otherwise forward.
    Forward landings on visited points are allowed here.
    """
    position = 0
    visited = {0}
    for i in jumps:
        back = position - i
        if back > 0 and back not in visited:
            position = back
        else:
            position += i
        visited.add(position)
    return position


def recaman_sequence_no_overlap(jumps: list[int]) -> int:
    """Part 2: like part 1, but never land on a visited point.

    A forward landing on a visited point is bumped up by one until it hits
    an unvisited point. Backward jumps are unchanged (they are already
    guaranteed to be unvisited).
    """
    position = 0
    visited = {0}
    for i in jumps:
        back = position - i
        if back > 0 and back not in visited:
            position = back
        else:
            position += i
            while position in visited:
                position += 1
        visited.add(position)
    return position


def crosses(a: int, b: int, arcs: list[tuple[int, int]]) -> bool:
    """Return True if an arc between a and b crosses any arc in `arcs`.

    `arcs` holds (low, high) endpoint pairs for arcs drawn on the SAME side
    of the number line. Two such semicircles cross exactly when their
    endpoints strictly interleave. Sharing an endpoint does not count, which
    matters because consecutive arcs always touch at the current position.
    """
    lo, hi = min(a, b), max(a, b)
    for c, d in arcs:
        if lo < c < hi < d or c < lo < d < hi:
            return True
    return False


def recaman_sequence_no_cross(jumps: list[int]) -> int:
    """Part 3: like part 2, but arcs may not cross.

    Arcs alternate sides (below, above, ...). Skipped jumps draw nothing, so
    they do not flip the side. Returns the final point.
    """
    position = 0
    top = 0  # highest visited point
    visited = {0}
    arcs = [[], []]  # arcs[0] = below the line, arcs[1] = above
    drawn = 0  # number of arcs drawn so far, picks the side
    for i in jumps:
        side = arcs[drawn % 2]
        back = position - i
        if back > 0 and back not in visited and not crosses(position, back, side):
            new = back
        else:
            new = None
            dest = position + i
            while True:
                if dest not in visited and not crosses(position, dest, side):
                    new = dest
                    break
                if dest > top:
                    # Past every visited endpoint, so every further bump
                    # behaves the same as this one and cannot help.
                    break
                dest += 1
            if new is None:
                continue  # no valid forward jump: skip this jump
        side.append((min(position, new), max(position, new)))
        position = new
        visited.add(position)
        top = max(top, position)
        drawn += 1
    return position


def sum_final_points(block: str, sequence_func: Callable[[list[int]], int]) -> int:
    """Apply `sequence_func` to every non-empty line and sum the results."""
    return sum(
        sequence_func(parse_line(line)) for line in block.splitlines() if line.strip()
    )


def part_one(data: list[str]) -> int:
    return sum_final_points(data[0], recaman_sequence)


def part_two(data: list[str]) -> int:
    return sum_final_points(data[1], recaman_sequence_no_overlap)


def part_three(data: list[str]) -> int:
    return sum_final_points(data[2], recaman_sequence_no_cross)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 291
    print("Part 2:", part_two(data))  # 32846
    print("Part 3:", part_three(data))  # 40245
