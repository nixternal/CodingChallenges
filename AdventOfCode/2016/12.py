#!/usr/bin/env python

"""
A Python script to simulate a simple virtual machine that processes a set of
instructions to manipulate registers. The script solves a puzzle by executing
two parts with different initial register configurations.

The instructions include:
- `cpy x y`: Copy the value of `x` (either a number or a register) into
             register `y`.
- `inc x`:   Increment the value of register `x` by 1.
- `dec x`:   Decrement the value of register `x` by 1.
- `jnz x y`: Jump `y` instructions away if the value of `x` (either a number
             or a register) is not zero.

The script reads instructions from a file (`12.in`), processes them, and
outputs the final value of a specified register for both parts of the puzzle.
"""


def read_puzzle_input() -> list:
    """
    Read the puzzle input from a file and return it as a list of strings.

    Returns:
        list: A list of strings, where each string represents an instruction.
    """

    with open("12.in", "r") as file:
        return file.read().splitlines()


def calculate(data: list, registers: dict, register: str) -> int:
    """
    Execute a series of instructions to manipulate the registers and return
    the final value of the specified register.

    Args:
        data (list): A list of instructions to execute.
        registers (dict): A dictionary representing the registers and their
                          initial values.
        register (str): The name of the register whose final value is to be
                        returned.

    Returns:
        int: The final value of the specified register after executing all
             instructions.
    """

    i = 0  # Instruction pointer
    while i < len(data):
        # Split the current instruction into its components
        instruction = data[i].split()
        cmd = instruction[0]  # The command to execute

        if cmd == 'cpy':
            # Copy value of `x` (either number or register) into register `y`
            x, y = instruction[1], instruction[2]
            registers[y] = int(x) if x.isdigit() else registers[x]
            i += 1  # Move to the next instruction
        elif cmd == 'inc':
            # Increment the value of the specified register by 1
            registers[instruction[1]] += 1
            i += 1  # Move to the next instruction
        elif cmd == 'dec':
            # Decrement the value of the specified register by 1
            registers[instruction[1]] -= 1
            i += 1  # Move to the next instruction
        elif cmd == 'jnz':
            # Jump `offset` instructions away if the value of `x` is not zero
            x, offset = instruction[1], int(instruction[2])
            value = int(x) if x.isdigit() else registers[x]
            if value != 0 and 0 <= i + offset < len(data):
                i += offset  # Perform the jump
            else:
                i += 1  # Move to the next instruction

    # Return the final value of the specified register
    return registers[register]


def part_one(data: list) -> int:
    """
    Execute the instructions with initial register values for Part 1 of the
    puzzle.

    Args:
        data (list): A list of instructions to execute.

    Returns:
        int: The final value of register 'a' after executing all instructions.
    """

    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}  # Initial register values
    return calculate(data, registers, 'a')


def part_two(data: list) -> int:
    """
    Execute the instructions with initial register values for Part 2 of the
    puzzle.

    Args:
        data (list): A list of instructions to execute.

    Returns:
        int: The final value of register 'a' after executing all instructions.
    """

    registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}  # Initial register values
    return calculate(data, registers, 'a')


if __name__ == "__main__":
    """
    Entry point of the script. Reads the puzzle input, executes both parts of
    the puzzle, and prints the results.
    """

    data = read_puzzle_input()  # Read the puzzle input

    print("Part 1:", part_one(data))  # 318077
    print("Part 2:", part_two(data))  # 9227731
