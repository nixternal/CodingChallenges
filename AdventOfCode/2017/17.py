#!/usr/bin/env python


def part_one() -> int:
    steps = 356
    iterations = 2017
    buffer = [0]
    position = 0

    for i in range(1, iterations + 1):
        position = ((position + steps) % len(buffer)) + 1
        buffer.insert(position, i)

    return buffer[(position + 1) % len(buffer)]


def part_two() -> int:
    steps = 356
    iterations = 50_000_000
    position = 0
    value_after_zero = 0

    # Since we only care about what's after position 0, and 0 always stays at
    # index 0 in the buffer, we only need to track when we insert at position 1
    for i in range(1, iterations + 1):
        position = ((position + steps) % i) + 1

        # If we're inserting at position 1 (right after 0)
        if position == 1:
            value_after_zero = i

    return value_after_zero


if __name__ == "__main__":
    print("Part 1:", part_one())  # 808
    print("Part 2:", part_two())  # 47_465_686
