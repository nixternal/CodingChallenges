#!/usr/bin/env python


def read_puzzle_input() -> str:
    with open("06.in", "r") as file:
        return file.read().splitlines()[0]


def find_marker(buffer: str, window_size: int) -> int:
    for i in range(window_size, len(buffer)):
        # Extract slice of the string ending at 'i'
        current_window = buffer[i - window_size:i]

        # Check if the number of unique characters equals the window size
        if len(set(current_window)) == window_size:
            return i  # This is the number of characters processed

    return 0


def part_one(data: str) -> int:
    return find_marker(data, 4)


def part_two(data: str) -> int:
    return find_marker(data, 14)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 1640
    print("Part 2:", part_two(data))  # 3613
