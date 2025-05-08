#!/usr/bin/env python
"""
Advent of Code - Day 2: Intcode Computer Implementation

This script implements an Intcode computer which processes operations on integer
arrays. The program reads a list of integers, where every four integers represent an
instruction:
- opcode (1=add, 2=multiply, 99=halt)
- two input positions
- output position
"""


def read_puzzle_input() -> list:
    """
    Read and parse puzzle input from file.

    Returns:
        list: List of integers representing the Intcode program
    """

    with open("02.in", "r") as file:
        return list(map(int, file.read().split(",")))


def run_intcode(program: list) -> int:
    """
    Execute an Intcode program.

    Args:
        program: List of integers representing the Intcode program

    Returns:
        int: Value at position 0 after program execution
    """

    memory = program.copy()  # Create a copy to avoid modifying the original
    position = 0

    while position < len(memory):
        opcode = memory[position]

        # Check for halt instruction
        if opcode == 99:
            break

        # Ensure we have enough elements for a complete instruction
        if position + 3 >= len(memory):
            break

        # Extract instruction parameters
        input1_pos = memory[position + 1]
        input2_pos = memory[position + 2]
        output_pos = memory[position + 3]

        # Validate memory addresses
        if not all(
            0 <= pos < len(memory) for pos in [input1_pos, input2_pos, output_pos]
        ):
            break

        # Process instruction
        if opcode == 1:  # Addition
            memory[output_pos] = memory[input1_pos] + memory[input2_pos]
        elif opcode == 2:  # Multiplication
            memory[output_pos] = memory[input1_pos] * memory[input2_pos]
        else:  # Invalid opcode
            break

        position += 4  # Move to next instruction

    return memory[0]


def part_one(data: list) -> int:
    """
    Solve part one: Run the program with noun=12 and verb=2.

    Args:
        data: Original Intcode program

    Returns:
        int: Value at position 0 after program execution
    """

    program = data.copy()
    program[1] = 12  # Set noun
    program[2] = 2  # Set verb
    return run_intcode(program)


def part_two(data: list) -> int:
    """
    Solve part two: Find noun and verb that produce the target output.

    The solution is 100 * noun + verb, where noun and verb are values between 0 and 99
    that result in the program producing 19690720.

    Args:
        data: Original Intcode program

    Returns:
        int: 100 * noun + verb for the solution, or -1 if not found
    """

    target = 19690720

    for noun in range(100):
        for verb in range(100):
            program = data.copy()
            program[1] = noun
            program[2] = verb

            if run_intcode(program) == target:
                return 100 * noun + verb

    return -1  # No solution found


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 6568671
    print("Part 2:", part_two(data))  # 3951
