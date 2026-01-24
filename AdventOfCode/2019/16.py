#!/usr/bin/env python


from types import new_class


def read_puzzle_input() -> list:
    with open("16.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> str:
    signal = [int(x) for x in data[0]]
    base_pattern = [0, 1, 0, -1]

    for _ in range(100):
        new_signal = []
        for i in range(len(signal)):
            total = 0
            repeat = i + 1
            # Calculate pattern on-the-fly to save memory
            for j in range(len(signal)):
                pattern_value = base_pattern[((j + 1) // repeat) % 4]
                if pattern_value != 0:  # Skip multiplication by zero
                    total += signal[j] * pattern_value
            new_signal.append(abs(total) % 10)
        signal = new_signal

    return "".join(map(str, signal[:8]))


def part_two(data: list) -> str:
    offset = int(data[0][:7])
    input_signal = [int(x) for x in data[0]]
    input_len = len(input_signal)
    total_length = input_len * 10_000

    # Validate offset for suffix sum optimization
    if offset < total_length // 2:
        raise ValueError("Offset is too small for the suffix sum trick!")

    # Build relevant signal more efficiently
    relevant_length = total_length - offset
    relevant_signal = []

    # More efficient signal construction
    start_idx = offset % input_len
    for i in range(relevant_length):
        relevant_signal.append(input_signal[(start_idx + i) % input_len])

    # Optimized suffix sum calculation (100 phases)
    for _ in range(100):
        total = 0
        for i in range(len(relevant_signal) - 1, -1, -1):
            total += relevant_signal[i]
            relevant_signal[i] = total % 10

    return "".join(map(str, relevant_signal[:8]))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 11833188
    print("Part 2:", part_two(data))  # 55005000
