#!/usr/bin/env python

import re


def read_puzzle_input() -> tuple[str, str]:
    """Read and split the input file into crate diagram and procedures."""
    with open("05.in", "r") as file:
        crates, procedures = file.read().split("\n\n")
        return crates, procedures


def parse_crates(diagram: str) -> list[list[str]]:
    """
    Parse the ASCII art crate diagram into a list of stacks.
    Returns a list where each element is a stack (list) of crates.
    """
    lines = diagram.splitlines()

    # Find the line with stack numbers
    index_line = next(i for i, line in enumerate(lines) if line.strip().startswith("1"))
    num_stacks = len(lines[index_line].split())

    # Initialize stacks
    stacks = [[] for _ in range(num_stacks)]

    # Parse crates from bottom to top (reverse the lines above the index line)
    for line in reversed(lines[:index_line]):
        for i in range(num_stacks):
            # Each crate is at column position 4*i + 1
            pos = 4 * i + 1
            if pos < len(line) and line[pos].isalpha():
                stacks[i].append(line[pos])

    return stacks


def parse_procedure(procedure: str) -> tuple[int, int, int]:
    """Extract move count, source stack, and destination stack from a procedure line."""
    move, source, dest = map(int, re.findall(r"\d+", procedure))
    return move, source, dest


def part_one(data: tuple[str, str]) -> str:
    """
    Solve part 1: move crates one at a time (reversing order).
    Returns the top crates from each stack.
    """
    stacks = parse_crates(data[0])
    procedures = data[1].splitlines()

    for procedure in procedures:
        move, source, dest = parse_procedure(procedure)
        # Move crates one at a time (LIFO - last in, first out)
        for _ in range(move):
            stacks[dest - 1].append(stacks[source - 1].pop())

    return "".join(stack[-1] for stack in stacks if stack)


def part_two(data: tuple[str, str]) -> str:
    """
    Solve part 2: move crates in groups (preserving order).
    Returns the top crates from each stack.
    """
    stacks = parse_crates(data[0])
    procedures = data[1].splitlines()

    for procedure in procedures:
        move, source, dest = parse_procedure(procedure)
        # Move multiple crates at once (preserving order)
        temp = [stacks[source - 1].pop() for _ in range(move)]
        stacks[dest - 1].extend(reversed(temp))

    return "".join(stack[-1] for stack in stacks if stack)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # CVCWCRTVQ
    print("Part 2:", part_two(data))  # CNSCZWLVT
