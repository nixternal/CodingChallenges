#!/usr/bin/env python

from itertools import permutations


def read_puzzle_input() -> str:
    """Read and return the intcode program from input file."""
    with open("07.in", "r") as file:
        return file.read().strip()


def get_parameter_value(memory, instruction_pointer, parameter_offset, mode):
    """
    Fetch parameter value based on addressing mode.

    Args:
        memory: The program memory (list of integers)
        instruction_pointer: Current position in memory
        parameter_offset: Which parameter to fetch (1, 2, or 3)
        mode: 0 for position mode, 1 for immediate mode

    Returns:
        The parameter value
    """
    parameter = memory[instruction_pointer + parameter_offset]

    if mode == 0:  # Position mode: parameter is an address
        return memory[parameter]
    elif mode == 1:  # Immediate mode: parameter is the value
        return parameter
    else:
        raise ValueError(f"Invalid parameter mode: {mode}")


def execute_intcode(memory, instruction_pointer, inputs):
    """
    Execute intcode program until it outputs a value, needs input, or halts.

    Args:
        memory: Program memory (will be modified)
        instruction_pointer: Current execution position
        inputs: List of input values (consumed from front)

    Returns:
        tuple: (output_value, new_ip, is_halted, modified_memory)
               output_value is None if no output was produced
    """
    while True:
        instruction = memory[instruction_pointer]
        opcode = instruction % 100
        modes = instruction // 100

        # Extract parameter modes
        mode1 = modes % 10
        mode2 = (modes // 10) % 10

        if opcode == 99:  # HALT
            return None, instruction_pointer, True, memory

        elif opcode == 1:  # ADD
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            dest = memory[instruction_pointer + 3]
            memory[dest] = val1 + val2
            instruction_pointer += 4

        elif opcode == 2:  # MULTIPLY
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            dest = memory[instruction_pointer + 3]
            memory[dest] = val1 * val2
            instruction_pointer += 4

        elif opcode == 3:  # INPUT
            if not inputs:  # Need input but none available - pause execution
                return None, instruction_pointer, False, memory
            dest = memory[instruction_pointer + 1]
            memory[dest] = inputs.pop(0)
            instruction_pointer += 2

        elif opcode == 4:  # OUTPUT
            output = get_parameter_value(memory, instruction_pointer, 1, mode1)
            instruction_pointer += 2
            return output, instruction_pointer, False, memory

        elif opcode == 5:  # JUMP-IF-TRUE
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            instruction_pointer = val2 if val1 != 0 else instruction_pointer + 3

        elif opcode == 6:  # JUMP-IF-FALSE
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            instruction_pointer = val2 if val1 == 0 else instruction_pointer + 3

        elif opcode == 7:  # LESS-THAN
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            dest = memory[instruction_pointer + 3]
            memory[dest] = 1 if val1 < val2 else 0
            instruction_pointer += 4

        elif opcode == 8:  # EQUALS
            val1 = get_parameter_value(memory, instruction_pointer, 1, mode1)
            val2 = get_parameter_value(memory, instruction_pointer, 2, mode2)
            dest = memory[instruction_pointer + 3]
            memory[dest] = 1 if val1 == val2 else 0
            instruction_pointer += 4

        else:
            raise ValueError(
                f"Unknown opcode {opcode} at position {instruction_pointer}"
            )


def part_one(data: str) -> int:
    """
    Part 1: Find maximum thrust from single-pass amplifier chain.
    Each amplifier runs once with phase settings 0-4.
    """
    program = [int(x) for x in data.split(",")]
    max_thrust = 0

    # Try all permutations of phase settings 0-4
    for phases in permutations(range(5)):
        signal = 0

        # Pass signal through each amplifier in sequence
        for phase in phases:
            inputs = [phase, signal]
            output, _, _, _ = execute_intcode(list(program), 0, inputs)
            signal = output if output is not None else 0

        max_thrust = max(max_thrust, signal)

    return max_thrust


def part_two(data: str) -> int:
    """
    Part 2: Find maximum thrust using feedback loop mode.
    Amplifiers run in a loop with phase settings 5-9 until the last one halts.
    """
    program = [int(x) for x in data.split(",")]
    max_thrust = 0

    # Try all permutations of phase settings 5-9
    for phases in permutations(range(5, 10)):
        # Initialize each amplifier with its phase setting
        amplifiers = [
            {"memory": list(program), "ip": 0, "inputs": [phase], "halted": False}
            for phase in phases
        ]

        # Add initial signal to first amplifier
        amplifiers[0]["inputs"].append(0)

        current_amp = 0
        last_output = 0

        # Run until the last amplifier halts
        while not amplifiers[4]["halted"]:
            amp = amplifiers[current_amp]

            if not amp["halted"]:
                output, new_ip, halted, new_memory = execute_intcode(
                    amp["memory"], amp["ip"], amp["inputs"]
                )

                amp["memory"] = new_memory
                amp["ip"] = new_ip
                amp["halted"] = halted

                # If amplifier produced output, send to next amplifier
                if output is not None:
                    next_amp = (current_amp + 1) % 5
                    amplifiers[next_amp]["inputs"].append(output)
                    last_output = output

            current_amp = (current_amp + 1) % 5

        max_thrust = max(max_thrust, last_output)

    return max_thrust


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 14902
    print("Part 2:", part_two(data))  # 6489132
