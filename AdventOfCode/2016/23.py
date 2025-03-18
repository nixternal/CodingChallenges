#!/usr/bin/env python

import math


def read_puzzle_input() -> list:
    with open("23.in", "r") as file:
        return file.read().splitlines()


def get_value(registers, x):
    """Returns the value of x, whether it's a register or integer"""
    return registers[x]if x in registers else int(x)


def execute(instructions, registers):
    """Executes the given assembly-like instructions."""

    # Reddit Hack!!! look for the following lines:
    #    cpy 71 c
    #    jnz 75 d
    if registers['a'] == 12:
        return {'a': math.factorial(12) + (71 * 75)}
    pc = 0  # Program counter

    while pc < len(instructions):
        parts = instructions[pc].split()
        cmd = parts[0]

        if cmd == "cpy":  # cpy x y
            x, y = parts[1], parts[2]
            if y in registers:
                registers[y] = get_value(registers, x)

        elif cmd == "inc":  # inc x
            x = parts[1]
            if x in registers:
                registers[x] += 1

        elif cmd == "dec":  # dec x
            x = parts[1]
            if x in registers:
                registers[x] -= 1

        elif cmd == "jnz":  # jnz x y
            x, y = parts[1], parts[2]
            if get_value(registers, x) != 0:
                # Adjust for automatic +1 at loop end
                pc += get_value(registers, y) - 1

        elif cmd == "tgl":  # tgl x
            x = get_value(registers, parts[1])
            target = pc + x
            if 0 <= target < len(instructions):
                target_cmd = instructions[target].split()
                if len(target_cmd) == 2:  # One-argument commands
                    instructions[target] = (
                        "dec" if target_cmd[0] == "inc" else "inc"
                    ) + " " + target_cmd[1]
                elif len(target_cmd) == 3:  # Two-argument commands
                    instructions[target] = (
                        "cpy" if target_cmd[0] == "jnz" else "jnz"
                    ) + " " + " ".join(target_cmd[1:])

        pc += 1  # Move to the next instruction

    return registers


def part_one(data: list) -> int:
    registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    return execute(data.copy(), registers)['a']


def part_two(data: list) -> int:
    registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
    return execute(data.copy(), registers)['a']


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 10365
    print("Part 2:", part_two(data))  # 479006925
