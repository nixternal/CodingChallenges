#!/usr/bin/env python
"""
This script solves a problem where a set of assembly-like instructions
is used to modify registers and navigate a program. The instructions include
basic operations like halving, tripling, incrementing values in registers,
and conditional jumps. The solution is implemented for two parts, where the
initial state of the registers differs.

Functions:
- `read_puzzle_input`: Reads the puzzle input from a file.
- `calculate`: Simulates the execution of instructions and updates registers.
- `part_one`: Solves part one of the problem.
- `part_two`: Solves part two of the problem.

Algorithm:
The script implements a simple **interpreter for a custom assembly language**.
This involves iterating through instructions sequentially, handling control
flow statements (`jmp`, `jie`, `jio`), and modifying registers based on
specific operations (`hlf`, `tpl`, `inc`).
"""

from typing import List, Dict


def read_puzzle_input() -> List[str]:
    """
    Reads the puzzle input from a file named '23.in'.

    Returns:
        List[str]: A list of strings where each string is a line from the file.
    """

    with open("23.in", "r") as file:
        return file.read().splitlines()


def calculate(data: List[str], regs: Dict[str, int]) -> Dict[str, int]:
    """
    Simulates the execution of assembly-like instructions on the given
    registers.

    Args:
        data (List[str]): A list of instructions to execute.
        regs (Dict[str, int]): A dictionary representing the registers and
                               their initial values.

    Returns:
        Dict[str, int]: The final state of the registers after executing the
                        instructions.

    Raises:
        ValueError: If an unknown instruction is encountered.

    Instructions:
        - `hlf r`: Halve the value in register `r`.
        - `tpl r`: Triple the value in register `r`.
        - `inc r`: Increment the value in register `r` by 1.
        - `jmp offset`: Jump to a new instruction by adding `offset` to the
                        current index.
        - `jie r, offset`: Jump if the value in register `r` is even.
        - `jio r, offset`: Jump if the value in register `r` is exactly 1.

    Algorithm:
        - Use a while loop to iterate over the instructions.
        - Modify the current index (`i`) based on jump instructions
          (`jmp`, `jie`, `jio`).
        - Update register values as specified by the instruction set.
    """

    i = 0
    while True:
        if i not in range(len(data)):  # Ensure index is within valid bounds.
            break

        line = data[i]
        inst, r = line.split(' ', 1)  # Split instruction & arguments.
        di = 1  # Default increment for index.

        if inst == 'hlf':    # Halve the value in the specified register.
            regs[r] //= 2
        elif inst == 'tpl':  # Triple the value in the specified register.
            regs[r] *= 3
        elif inst == 'inc':  # Increment the value in the specified register.
            regs[r] += 1
        elif inst == 'jmp':  # Unconditional jump.
            di = int(r)
        elif inst == 'jie':  # Jump if the register value is even.
            r, offset = r.split(',')
            if regs[r] % 2 == 0:
                di = int(offset)
        elif inst == 'jio':  # Jump if the register value is exactly 1.
            r, offset = r.split(',')
            if regs[r] == 1:
                di = int(offset)
        else:
            raise ValueError(f"Unknown instruction: {line}")

        i += di  # Update the instruction pointer.
    return regs


def part_one(data: list) -> int:
    """
    Solves part one of the problem.

    Args:
        data (List[str]): The list of instructions to execute.

    Returns:
        int: The value of register `b` after executing the instructions with
             initial state {'a': 0, 'b': 0}.
    """

    return calculate(data, {'a': 0, 'b': 0})['b']


def part_two(data: list) -> int:
    """
    Solves part two of the problem.

    Args:
        data (List[str]): The list of instructions to execute.

    Returns:
        int: The value of register `b` after executing the instructions with
             initial state {'a': 1, 'b': 0}.
    """

    return calculate(data, {'a': 1, 'b': 0})['b']


if __name__ == "__main__":
    # Read the input data
    data = read_puzzle_input()

    # Solve and print the results for both parts
    print("Part 1:", part_one(data))  # 307
    print("Part 2:", part_two(data))  # 160
