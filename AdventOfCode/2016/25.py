#!/usr/bin/env python

from itertools import count


def read_puzzle_input() -> list:
    with open("25.in", "r") as file:
        return file.read().splitlines()


def get_value(registers, x):
    """Returns the value of x, whether it's a register or integer"""
    return registers[x] if x in registers else int(x)


def execute(instructions, a_start):
    """Executes the given assembly-like instructions."""

    registers = {'a': a_start, 'b': 0, 'c': 0, 'd': 0}

    pc = 0  # Program counter
    output = []

    while 0 <= pc < len(instructions):
        parts = instructions[pc].split()
        cmd = parts[0]

        if cmd == 'cpy':
            x, y = parts[1], parts[2]
            if y in registers:
                registers[y] = get_value(registers, x)

        elif cmd == 'inc':
            x = parts[1]
            if x in registers:
                registers[x] += 1

        elif cmd == 'dec':
            x = parts[1]
            if x in registers:
                registers[x] -= 1

        elif cmd == 'jnz':
            x, y = parts[1], parts[2]
            if get_value(registers, x) != 0:
                pc += get_value(registers, y) - 1

        elif cmd == 'out':
            value = get_value(registers, parts[1])
            output.append(value)
            if len(output) >= 20:
                return output

        pc += 1

    return output


def part_one(data: list) -> int:
    for a in count(0):  # Infinite loop trying increasing values of 'a'
        output = execute(data, a)
        if all(output[i] == (i % 2) for i in range(len(output))):
            return a
    return -1


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 182
