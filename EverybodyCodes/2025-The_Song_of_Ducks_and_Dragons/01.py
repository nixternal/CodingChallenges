#!/usr/bin/env python


def read_puzzle_input() -> list[str]:
    """Read and return puzzle input as a list of lines."""
    with open("01.in", "r") as file:
        return file.read().splitlines()


def parse_names_and_moves(
    data: list[str], names_idx: int, moves_idx: int
) -> tuple[list[str], list[str]]:
    """Parse names and moves from data at specified indices."""
    return data[names_idx].split(","), data[moves_idx].split(",")


def part_one(data: list[str]) -> str:
    """Find name after applying moves with boundary clamping."""
    names, moves = parse_names_and_moves(data, 0, 2)
    current_index = 0

    for move in moves:
        direction = 1 if move[0] == "R" else -1
        position = direction * int(move[1:])
        # Clamp to valid range
        current_index = max(0, min(len(names) - 1, current_index + position))

    return names[current_index]


def part_two(data: list[str]) -> str:
    """Find name after applying moves with wraparound."""
    names, moves = parse_names_and_moves(data, 4, 6)
    n = len(names)
    current_index = 0

    for move in moves:
        direction = 1 if move[0] == "R" else -1
        current_index = (current_index + direction * int(move[1:])) % n

    return names[current_index]


def part_three(data: list[str]) -> str:
    """Find name after swapping with position 0 after each move."""
    names, moves = parse_names_and_moves(data, 8, 10)
    n = len(names)

    for move in moves:
        direction = 1 if move[0] == "R" else -1
        target_index = (direction * int(move[1:])) % n
        # Swap position 0 with target
        names[0], names[target_index] = names[target_index], names[0]

    return names[0]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # Elarkryth
    print("Part 2:", part_two(data))  # Wynnix
    print("Part 3:", part_three(data))  # Quenfeth
