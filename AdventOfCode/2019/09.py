#!/usr/bin/env python3


def read_puzzle_input() -> list:
    """Return the raw input as a list of strings (one per line)."""
    with open("09.in", "r") as file:
        return file.read().splitlines()


def get_value(memory: dict[int, int], pos: int, mode: int, relative_base: int) -> int:
    """Return the parameter value according to its mode."""
    if mode == 0:  # position mode
        addr = memory.get(pos, 0)
        return memory.get(addr, 0)
    elif mode == 1:  # immediate mode
        return memory.get(pos, 0)
    elif mode == 2:  # relative mode
        addr = relative_base + memory.get(pos, 0)
        return memory.get(addr, 0)
    else:
        raise ValueError(f"Unknown parameter mode {mode}")


def get_address(memory: dict[int, int], pos: int, mode: int, relative_base: int) -> int:
    """Return the address for writes according to its mode."""
    if mode == 0:  # position mode
        return memory.get(pos, 0)
    elif mode == 2:  # relative mode
        return relative_base + memory.get(pos, 0)
    else:
        raise ValueError(f"Invalid mode {mode} for write address")


def run_intcode(program: list[int], input_values: list[int]) -> list[int]:
    # Use dict for expandable memory, default to 0
    memory = {i: val for i, val in enumerate(program)}
    ip = 0
    relative_base = 0
    input_iter = iter(input_values)
    outputs: list[int] = []

    while True:
        instr = memory.get(ip, 0)
        opcode = instr % 100
        modes = [(instr // (10**i)) % 10 for i in range(2, 5)]

        if opcode == 99:
            break

        elif opcode in {1, 2}:  # add or multiply
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            dest = get_address(memory, ip + 3, modes[2], relative_base)
            memory[dest] = a + b if opcode == 1 else a * b
            ip += 4

        elif opcode == 3:  # input
            try:
                value = next(input_iter)
            except StopIteration:
                raise RuntimeError("Program requested more input than supplied.")
            dest = get_address(memory, ip + 1, modes[0], relative_base)
            memory[dest] = value
            ip += 2

        elif opcode == 4:  # output
            val = get_value(memory, ip + 1, modes[0], relative_base)
            outputs.append(val)
            ip += 2

        elif opcode in {5, 6}:  # jump-if-true / jump-if-false
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                ip = b
            else:
                ip += 3

        elif opcode in {7, 8}:  # less-than / equals
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            dest = get_address(memory, ip + 3, modes[2], relative_base)
            if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                memory[dest] = 1
            else:
                memory[dest] = 0
            ip += 4

        elif opcode == 9:  # adjust relative base
            a = get_value(memory, ip + 1, modes[0], relative_base)
            relative_base += a
            ip += 2

        else:
            raise ValueError(f"Unknown opcode {opcode} at position {ip}")

    return outputs


def part_one(data: list) -> int:
    """
    Part 1 asks for the BOOST keycode produced when the program is run with input value 1.
    This runs the BOOST program in test mode.
    """
    program = [int(x) for x in data[0].split(",")]
    outputs = run_intcode(program, [1])
    return outputs[-1] if outputs else -2


def part_two(data: list) -> int:
    """
    Part 2 asks for the distress signal coordinates when the program is run with input value 2.
    This runs the BOOST program in sensor boost mode.
    """
    program = [int(x) for x in data[0].split(",")]
    outputs = run_intcode(program, [2])
    return outputs[-1] if outputs else -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3598076521
    print("Part 2:", part_two(data))  # 90722
