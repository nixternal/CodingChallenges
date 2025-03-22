#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("02.in", "r") as file:
        return [line == 'TRUE' for line in file.read().splitlines()]


def part_one(data: list) -> int:
    sum_true = 0
    for i in range(len(data)):
        if data[i]:
            sum_true += i + 1
    return sum_true


def part_two(data: list) -> int:
    true_gates_count = 0

    for i in range(0, len(data), 2):
        gate_index = i // 2
        if gate_index % 2 == 0:  # Even index - AND gate
            gate_output = data[i] and data[i + 1]
        else:  # Odd index - OR gate
            gate_output = data[i] or data[i + 1]

        if gate_output:
            true_gates_count += 1

    return true_gates_count


def part_three(data: list) -> int:
    # Count TRUE sensors
    true_count = sum(data)

    # Process each layer of the circuit
    current_layer = data.copy()

    layer_num = 0
    while len(current_layer) > 1:
        next_layer = []

        for i in range(0, len(current_layer), 2):
            if i + 1 < len(current_layer):
                # Gate type alternates within each layer
                gate_index = i // 2
                if gate_index % 2 == 0:  # Even layer - AND gates
                    gate_output = current_layer[i] and current_layer[i + 1]
                else:  # Odd layer - OR gates
                    gate_output = current_layer[i] or current_layer[i + 1]

                next_layer.append(gate_output)
                if gate_output:
                    true_count += 1

        current_layer = next_layer
        layer_num += 1

    return true_count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 63931
    print("Part 2:", part_two(data))    # 124
    print("Part 3:", part_three(data))  # 494
