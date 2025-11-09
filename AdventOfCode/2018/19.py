#!/usr/bin/env python3
"""
Advent of Code 2018 - Day 19: Go With The Flow

This puzzle involves executing a program written in a custom assembly-like language
with 16 opcodes. The program computes the sum of divisors of a large number, but
does so inefficiently through brute-force iteration.

Part 1: Run the program with register 0 initialized to 0
Part 2: Run with register 0 initialized to 1, which causes the program to compute
        divisors of a much larger number (making direct execution impractical)
"""

from typing import Callable, Dict, List, Tuple

# ============================================================================
# Opcode Definitions (16 operations from Day 16)
# ============================================================================
# Each operation modifies a register array in-place
# Parameters: r (registers), a, b, c (instruction operands)


def addr(r: List[int], a: int, b: int, c: int) -> None:
    """Add register: r[c] = r[a] + r[b]"""
    r[c] = r[a] + r[b]


def addi(r: List[int], a: int, b: int, c: int) -> None:
    """Add immediate: r[c] = r[a] + b"""
    r[c] = r[a] + b


def mulr(r: List[int], a: int, b: int, c: int) -> None:
    """Multiply register: r[c] = r[a] * r[b]"""
    r[c] = r[a] * r[b]


def muli(r: List[int], a: int, b: int, c: int) -> None:
    """Multiply immediate: r[c] = r[a] * b"""
    r[c] = r[a] * b


def banr(r: List[int], a: int, b: int, c: int) -> None:
    """Bitwise AND register: r[c] = r[a] & r[b]"""
    r[c] = r[a] & r[b]


def bani(r: List[int], a: int, b: int, c: int) -> None:
    """Bitwise AND immediate: r[c] = r[a] & b"""
    r[c] = r[a] & b


def borr(r: List[int], a: int, b: int, c: int) -> None:
    """Bitwise OR register: r[c] = r[a] | r[b]"""
    r[c] = r[a] | r[b]


def bori(r: List[int], a: int, b: int, c: int) -> None:
    """Bitwise OR immediate: r[c] = r[a] | b"""
    r[c] = r[a] | b


def setr(r: List[int], a: int, _: int, c: int) -> None:
    """Set register: r[c] = r[a]"""
    r[c] = r[a]


def seti(r: List[int], a: int, _: int, c: int) -> None:
    """Set immediate: r[c] = a"""
    r[c] = a


def gtir(r: List[int], a: int, b: int, c: int) -> None:
    """Greater-than immediate/register: r[c] = 1 if a > r[b] else 0"""
    r[c] = 1 if a > r[b] else 0


def gtri(r: List[int], a: int, b: int, c: int) -> None:
    """Greater-than register/immediate: r[c] = 1 if r[a] > b else 0"""
    r[c] = 1 if r[a] > b else 0


def gtrr(r: List[int], a: int, b: int, c: int) -> None:
    """Greater-than register/register: r[c] = 1 if r[a] > r[b] else 0"""
    r[c] = 1 if r[a] > r[b] else 0


def eqir(r: List[int], a: int, b: int, c: int) -> None:
    """Equal immediate/register: r[c] = 1 if a == r[b] else 0"""
    r[c] = 1 if a == r[b] else 0


def eqri(r: List[int], a: int, b: int, c: int) -> None:
    """Equal register/immediate: r[c] = 1 if r[a] == b else 0"""
    r[c] = 1 if r[a] == b else 0


def eqrr(r: List[int], a: int, b: int, c: int) -> None:
    """Equal register/register: r[c] = 1 if r[a] == r[b] else 0"""
    r[c] = 1 if r[a] == r[b] else 0


# Opcode lookup table
OPS: Dict[str, Callable[[List[int], int, int, int], None]] = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def read_puzzle_input(
    filename: str = "19.in",
) -> Tuple[int, List[Tuple[str, int, int, int]]]:
    """
    Parse the puzzle input file.

    Format:
        #ip <register>       -- Declares which register is bound to instruction pointer
        <opcode> <a> <b> <c> -- Program instructions

    Args:
        filename: Input file path

    Returns:
        Tuple of (ip_register, program_instructions)
    """
    with open(filename, "r") as file:
        lines = [line.strip() for line in file.read().splitlines() if line.strip()]

        # First line: #ip <register_number>
        ip_reg = int(lines[0].split()[1])

        # Parse program instructions
        program = []
        for line in lines[1:]:
            parts = line.split()
            op = parts[0]
            a, b, c = map(int, parts[1:])
            program.append((op, a, b, c))

    return ip_reg, program


def execute_program(
    ip_reg: int,
    program: List[Tuple[str, int, int, int]],
    initial_r0: int = 0,
    max_steps: int = None,
) -> List[int]:
    """
    Execute the program with the given initial register state.

    The instruction pointer (IP) is bound to a specific register. Before each
    instruction executes, the IP value is written to that register. After
    execution, the register value is read back as the new IP, then incremented.

    Args:
        ip_reg: Which register is bound to the instruction pointer
        program: List of (opcode, a, b, c) tuples
        initial_r0: Initial value for register 0
        max_steps: Maximum steps to execute (None for unlimited)

    Returns:
        Final register state
    """
    registers = [0] * 6
    registers[0] = initial_r0
    ip = 0
    steps = 0

    while 0 <= ip < len(program):
        if max_steps is not None and steps >= max_steps:
            break

        # Write IP to bound register
        registers[ip_reg] = ip

        # Execute instruction
        op, a, b, c = program[ip]
        OPS[op](registers, a, b, c)

        # Read IP from bound register and increment
        ip = registers[ip_reg] + 1
        steps += 1

    return registers


def detect_target_number(ip_reg: int, program: List[Tuple[str, int, int, int]]) -> int:
    """
    Detect the large number N that the program will compute divisors for.

    The program has two phases:
    1. Initialization: Build a large constant N in one of the registers
    2. Divisor loop: Iterate from 1 to N checking divisors (very slow)

    This function runs the initialization phase (first ~1000-2000 steps) and
    captures the largest value that appears in any register, which is the
    target number N.

    Args:
        ip_reg: Instruction pointer register
        program: Program instructions

    Returns:
        The target number N whose divisors will be summed
    """
    registers = execute_program(ip_reg, program, initial_r0=1, max_steps=2000)
    # The target number is typically the largest value in any register
    return max(registers)


def sum_of_divisors(n: int) -> int:
    """
    Calculate the sum of all divisors of n (including 1 and n).

    Optimized to O(√n) by checking pairs of divisors simultaneously.
    For each divisor i found, n/i is also a divisor.

    Args:
        n: Number to find divisors for

    Returns:
        Sum of all divisors

    Example:
        >>> sum_of_divisors(12)
        28  # 1 + 2 + 3 + 4 + 6 + 12
    """
    total = 0
    sqrt_n = int(n**0.5)

    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            total += i
            # Add the paired divisor (n/i) if it's different from i
            if i != n // i:
                total += n // i

    return total


def part_one(ip_reg: int, program: List[Tuple[str, int, int, int]]) -> int:
    """
    Part 1: Execute the program with register 0 initialized to 0.

    The program runs relatively quickly with r0=0, completing in a reasonable
    number of steps and returning the result in register 0.
    """
    registers = execute_program(ip_reg, program, initial_r0=0)
    return registers[0]


def part_two(ip_reg: int, program: List[Tuple[str, int, int, int]]) -> int:
    """
    Part 2: Compute result when register 0 is initialized to 1.

    With r0=1, the program builds a much larger target number (typically
    10+ million), making direct execution impractical. Instead, we:
    1. Run the initialization phase to detect the target number N
    2. Calculate sum of divisors of N using optimized O(√n) algorithm

    This is millions of times faster than letting the program run its
    inefficient O(n) divisor-checking loop.
    """
    target = detect_target_number(ip_reg, program)
    return sum_of_divisors(target)


if __name__ == "__main__":
    """Run solutions for both parts."""
    ip_reg, program = read_puzzle_input()

    print(f"Part 1: {part_one(ip_reg, program)}")
    print(f"Part 2: {part_two(ip_reg, program)}")
