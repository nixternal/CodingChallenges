#!/usr/bin/env python3


def read_puzzle_input() -> list:
    """Return the raw input as a list of strings (one per line)."""
    with open("05.in", "r") as file:
        return file.read().splitlines()


def get_value(memory: list[int], pos: int, mode: int) -> int:
    """Return the parameter value according to its mode."""
    if mode == 0:  # position mode
        return memory[memory[pos]]
    elif mode == 1:  # immediate mode
        return memory[pos]
    else:
        raise ValueError(f"Unknown parameter mode {mode}")


def run_intcode(program: list[int], input_values: list[int]) -> list[int]:
    """
    Execute an Intcode program.

    Parameters
    ----------
    program : list[int]
        The raw program (will be copied so the caller is not mutated).
    input_values : list[int]
        Values to feed into opcode 3 instructions, in order.

    Returns
    -------
    output_values : list[int]
        All values produced by opcode 4 during execution.
    """
    memory = program[:]  # work on a copy
    ip = 0  # instruction pointer
    input_iter = iter(input_values)
    outputs: list[int] = []

    while True:
        instr = memory[ip]
        opcode = instr % 100
        modes = [(instr // (10**i)) % 10 for i in range(2, 5)]

        if opcode == 99:  # halt
            break

        elif opcode in {1, 2}:  # add or multiply
            a = get_value(memory, ip + 1, modes[0])
            b = get_value(memory, ip + 2, modes[1])
            dest = memory[ip + 3]  # destination is always position mode
            memory[dest] = a + b if opcode == 1 else a * b
            ip += 4

        elif opcode == 3:  # input
            try:
                value = next(input_iter)
            except StopIteration:
                raise RuntimeError("Program requested more input than supplied.")
            dest = memory[ip + 1]  # destination is always position mode
            memory[dest] = value
            ip += 2

        elif opcode == 4:  # output
            val = get_value(memory, ip + 1, modes[0])
            outputs.append(val)
            ip += 2

        elif opcode in {5, 6}:  # jump-if-true / jump-if-false
            a = get_value(memory, ip + 1, modes[0])
            b = get_value(memory, ip + 2, modes[1])
            if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                ip = b
            else:
                ip += 3

        elif opcode in {7, 8}:  # less-than / equals
            a = get_value(memory, ip + 1, modes[0])
            b = get_value(memory, ip + 2, modes[1])
            dest = memory[ip + 3]  # destination is always position mode
            if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                memory[dest] = 1
            else:
                memory[dest] = 0
            ip += 4

        else:
            raise ValueError(f"Unknown opcode {opcode} at position {ip}")

    return outputs


def part_one(data: list) -> int:
    """
    Part 1 asks for the diagnostic code produced when the program is run with input value 1.
    The puzzle guarantees that exactly one output will be emitted.
    """
    # Convert the single comma‑separated line into a list of integers
    program = [int(x) for x in data[0].split(",")]
    outputs = run_intcode(program, [1])
    return outputs[-1] if outputs else -2


def part_two(data: list) -> int:
    """
    Part 2 asks for the diagnostic code produced when the program is run with input value 5.
    Again exactly one output will be emitted.
    """
    program = [int(x) for x in data[0].split(",")]
    outputs = run_intcode(program, [5])
    return outputs[-1] if outputs else -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 9431221
    print("Part 2:", part_two(data))  # 1409363
