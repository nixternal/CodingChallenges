#!/usr/bin/env python
"""
Advent of Code 2018 - Day 16: Chronal Classification

This script solves both parts of Day 16's puzzle, which involves:
1. Analyzing CPU operation samples to determine how many behave like 3+ opcodes (Part 1)
2. Determining the actual opcode mapping and executing a test program (Part 2)

The puzzle involves a CPU with 16 operations and 4 registers. We're given:
- Samples showing register states before/after unknown operations
- A test program to run once we've determined the opcode mapping

Solution Approach:
1. Implements all 16 possible operations as functions that modify registers
2. For Part 1, tests each sample against all operations to count matches
3. For Part 2, uses process of elimination to map opcodes to operations,
   then executes the test program with the resolved mapping
"""

import re
from collections import defaultdict


def read_puzzle_input() -> str:
    """Reads the input file containing samples and test program.

    Returns:
        str: The complete contents of the input file
    """

    with open("16.in", "r") as file:
        return file.read()


# Register operation functions
# Each follows the signature (registers, a, b, c)
# where registers is modified in-place and a,b,c are instruction parameters


def addr(regs, a, b, c):
    """addr (add register): stores into register C the sum of register A and register B"""

    regs[c] = regs[a] + regs[b]


def addi(regs, a, b, c):
    """addi (add immediate): stores into register C the sum of register A and value B"""

    regs[c] = regs[a] + b


def mulr(regs, a, b, c):
    """mulr (multiply register): stores into register C the product of register A and register B"""

    regs[c] = regs[a] * regs[b]


def muli(regs, a, b, c):
    """muli (multiply immediate): stores into register C the product of register A and value B"""

    regs[c] = regs[a] * b


def banr(regs, a, b, c):
    """banr (bitwise AND register): stores into register C the bitwise AND of register A and register B"""

    regs[c] = regs[a] & regs[b]


def bani(regs, a, b, c):
    """bani (bitwise AND immediate): stores into register C the bitwise AND of register A and value B"""

    regs[c] = regs[a] & b


def borr(regs, a, b, c):
    """borr (bitwise OR register): stores into register C the bitwise OR of register A and register B"""

    regs[c] = regs[a] | regs[b]


def bori(regs, a, b, c):
    """bori (bitwise OR immediate): stores into register C the bitwise OR of register A and value B"""

    regs[c] = regs[a] | b


def setr(regs, a, b, c):
    """setr (set register): copies the contents of register A into register C (ignores B)"""

    regs[c] = regs[a]


def seti(regs, a, b, c):
    """seti (set immediate): stores value A into register C (ignores B)"""

    regs[c] = a


def gtir(regs, a, b, c):
    """gtir (greater-than immediate/register):
    stores 1 in register C if value A is greater than register B, else 0"""

    regs[c] = 1 if a > regs[b] else 0


def gtri(regs, a, b, c):
    """gtri (greater-than register/immediate):
    stores 1 in register C if register A is greater than value B, else 0"""

    regs[c] = 1 if regs[a] > b else 0


def gtrr(regs, a, b, c):
    """gtrr (greater-than register/register):
    stores 1 in register C if register A is greater than register B, else 0"""

    regs[c] = 1 if regs[a] > regs[b] else 0


def eqir(regs, a, b, c):
    """eqir (equal immediate/register):
    stores 1 in register C if value A equals register B, else 0"""

    regs[c] = 1 if a == regs[b] else 0


def eqri(regs, a, b, c):
    """eqri (equal register/immediate):
    stores 1 in register C if register A equals value B, else 0"""

    regs[c] = 1 if regs[a] == b else 0


def eqrr(regs, a, b, c):
    """eqrr (equal register/register):
    stores 1 in register C if register A equals register B, else 0"""

    regs[c] = 1 if regs[a] == regs[b] else 0


def parse_samples(data: str) -> list:
    """Parses the input data to extract sample cases.

    Each sample consists of:
    - Initial register state (before)
    - Instruction (opcode and parameters)
    - Final register state (after)

    Args:
        data (str): Complete puzzle input

    Returns:
        list: List of tuples (before, instruction, after)
    """
    samples = []
    parts = data.split("\n\n\n\n")[0].split("\n\n")
    for part in parts:
        lines = part.split("\n")
        before = list(map(int, re.findall(r"\d+", lines[0])))
        instruction = list(map(int, re.findall(r"\d+", lines[1])))
        after = list(map(int, re.findall(r"\d+", lines[2])))
        samples.append((before, instruction, after))
    return samples


def part_one(data: str, operations: list) -> int:
    """Solves Part 1 by counting samples that behave like 3 or more operations.

    For each sample, tests all operations to see which could produce the observed result.

    Args:
        data (str): Puzzle input
        operations (list): List of all operation functions

    Returns:
        int: Number of samples matching 3+ operations
    """
    samples = parse_samples(data)
    count = 0

    for before, instruction, after in samples:
        _, a, b, c = instruction
        matches = 0

        # Test each operation against the sample
        for op in operations:
            regs = before.copy()
            op(regs, a, b, c)
            if regs == after:
                matches += 1

        if matches >= 3:
            count += 1

    return count


def part_two(data: str, operations: list) -> int:
    """Solves Part 2 by:
    1. Determining the correct opcode-to-operation mapping
    2. Executing the test program with the resolved mapping

    Args:
        data (str): Puzzle input
        operations (list): List of all operation functions

    Returns:
        int: Value in register 0 after program execution
    """
    parts = data.split("\n\n\n\n")
    samples = parse_samples(parts[0])
    program = [
        list(map(int, line.split())) for line in parts[1].strip().split("\n")
    ]

    # Initialize possible mappings: each operation could be any opcode
    possible = defaultdict(set)
    for op in operations:
        possible[op].update(range(16))

    # Eliminate impossible mappings using samples
    for before, instruction, after in samples:
        opcode, a, b, c = instruction

        for op in list(possible.keys()):
            regs = before.copy()
            op(regs, a, b, c)
            if regs != after:
                possible[op].discard(opcode)

    # Resolve mappings through process of elimination
    opcode_to_func = {}
    while len(opcode_to_func) < 16:
        for op in list(possible.keys()):
            if len(possible[op]) == 1:  # Found a definitive mapping
                opcode = possible[op].pop()
                opcode_to_func[opcode] = op
                del possible[op]
                # Remove this opcode from other operations' possibilities
                for other_op in possible:
                    possible[other_op].discard(opcode)
                break

    # Execute the test program
    regs = [0, 0, 0, 0]
    for instruction in program:
        opcode, a, b, c = instruction
        op = opcode_to_func[opcode]
        op(regs, a, b, c)

    return regs[0]


if __name__ == "__main__":
    # List of all possible operations the CPU can perform
    operations = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    ]

    data = read_puzzle_input()
    print("Part 1:", part_one(data, operations))  # 588
    print("Part 2:", part_two(data, operations))  # 627
