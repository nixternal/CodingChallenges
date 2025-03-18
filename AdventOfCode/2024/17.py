#!/usr/bin/env python

import re
from typing import List, Optional

# Instruction Constants
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)


def read_puzzle_input() -> str:
    with open("17.in", "r") as file:
        return file.read()


def get_operand_value(operand: int, a: int, b: int, c: int) -> int:
    """
    Retrieve the value of an operand based on its identifier.

    Args:
        operand (int): The operand identifier (0-6).
        a (int): Value of register 'a'.
        b (int): Value of register 'b'.
        c (int): Value of register 'c'.

    Returns:
        int: The resolved operand value.

    Raises:
        ValueError: If the operand is not recognized.
    """

    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    else:
        raise ValueError(f"Unrecognized operand: {operand}")


def part_one(data: str) -> str:
    """
    Execute the program instructions and return the output as a
    comma-separated string.

    Args:
        data (str): The program data containing instructions and initial
        values.

    Returns:
        str: A comma-separated string of output values.

    Raises:
        ValueError: If an invalid instruction is encountered.
    """

    # Parse initial register values and program instructions
    a, b, c, *program = map(int, re.findall(r"\d+", data))

    pointer = 0  # Program counter
    output: List[int] = []  # Collected out put values

    # Execute instructions until the end of the program
    while pointer < len(program):
        instruction, operand = program[pointer], program[pointer + 1]

        # Process instructions based on their type
        if instruction == ADV:  # Shift register 'a' to the right
            a >>= get_operand_value(operand, a, b, c)
        elif instruction == BXL:  # XOR register 'b' with operand
            b ^= operand
        elif instruction == BST:  # Set 'b' to operand value modulo 8
            b = get_operand_value(operand, a, b, c) % 8
        elif instruction == JNZ:  # Jump if 'a' is not zero
            if a != 0:
                pointer = operand
                continue
        elif instruction == BXC:  # XOR register 'b' with 'c'
            b ^= c
        elif instruction == OUT:  # Append output value modulo 8
            output.append(get_operand_value(operand, a, b, c) % 8)
        elif instruction == BDV:  # Shift 'a' right and store in 'b'
            b = a >> get_operand_value(operand, a, b, c)
        elif instruction == CDV:  # Shift 'a' right and store 'c'
            c = a >> get_operand_value(operand, a, b, c)
        else:
            raise ValueError(f"Invalid instruction: {instruction}")

        pointer += 2  # Advance to the next instruction pair

    return ','.join(map(str, output))  # Join output values as a string


def part_two(data: str) -> Optional[int]:
    """
    Recursively determine a value that matches a sequence of outputs.

    Args:
        data (str): The program data containing instructions.

    Returns:
        Optional[int]: The resolved value matching the sequence, or None if
                       no match is found.

    Raises:
        AssertionError: If the program does not conform to expected structure.
        ValueError: If an invalid instruction is encountered.
    """

    # Parse the program instructions (ignoring the first three numbers)
    program = list(map(int, re.findall(r"\d+", data)[3:]))
    assert program[-2:] == [JNZ, 0], "Program must end with JNZ 0"

    def find(target: List[int], ans: int) -> Optional[int]:
        """
        Recursively find a value that matches the target output sequence.

        Args:
            target (List[int]): The target output sequence.
            ans (int): The current candidate answer.

        Returns:
            Optional[int]: The resolved value, or None if no match is found.
        """

        if not target:  # Base case: if no targets are left, return the answer
            return ans

        for t in range(8):  # Iterate over possible values(0-7)
            # Generate new 'a' by shifting and including 't'
            a, b, c = ans << 3 | t, 0, 0
            output, adv3 = None, False

            # Execute the program instructions
            for pointer in range(0, len(program) - 2, 2):
                instruction, operand = program[pointer], program[pointer + 1]

                if instruction == ADV:
                    assert operand == 3, "ADV must have operand 3"
                    assert not adv3, "Program has multiple ADVs"
                    adv3 = True
                elif instruction == BXL:  # XOR register 'b' with operand
                    b ^= operand
                elif instruction == BST:  # Set 'b' to operand value modulo 8
                    b = get_operand_value(operand, a, b, c) % 8
                elif instruction == JNZ:
                    raise AssertionError(
                        "Program contains instruction JNZ inside the loop body"
                    )
                elif instruction == BXC:  # XOR register 'b' with 'c'
                    b ^= c
                elif instruction == OUT:  # Set 'out' to operand value modulo 8
                    assert (
                        output is None
                    ), "Program has multiple OUT instructions"
                    output = get_operand_value(operand, a, b, c) % 8
                elif instruction == BDV:  # Shift 'a' right and store in 'b'
                    b = a >> get_operand_value(operand, a, b, c)
                elif instruction == CDV:  # Shift 'a' right and store in 'c'
                    c = a >> get_operand_value(operand, a, b, c)
                else:
                    raise ValueError(f"Invalid instruction: {instruction}")

                # If output == the last target, recurse w/ the reduced target
                if output == target[-1]:
                    result = find(target[:-1], a)
                    if result is not None:
                        return result
        return None

    return find(program, 0)  # Start the recursive search w/ initial value 0


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 4,0,4,7,1,2,7,1,6
    print("Part 2:", part_two(data))  # 202322348616234
