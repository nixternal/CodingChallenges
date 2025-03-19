#!/usr/bin/env python

"""
Advent of Code - Day 18: Duet

This program simulates a sound-based assembly language for two connected
programs. It processes instructions like playing sounds, setting register
values, performing arithmetic operations, and recovering sounds.
"""


def read_puzzle_input() -> list:
    """
    Read input data from the file '18.in'.

    Returns:
        list: A list of strings, each representing an instruction.
    """

    with open("18.in", "r") as file:
        return file.read().splitlines()


def part_one(data: list) -> int:
    """
    Simulate a single program executing the given instructions.

    The program has registers (like variables) and can play sounds.
    It returns the frequency of the first recovered sound.

    Instructions:
    - snd X: Play sound with frequency X
    - set X Y: Set register X to value Y
    - add X Y: Increase register X by value Y
    - mul X Y: Multiply register X by value Y
    - mod X Y: Set register X to X modulo Y
    - rcv X: Recover the most recently played sound if X is not zero
    - jgz X Y: Jump Y steps if X is greater than zero

    Args:
        data (list): A list of instructions to execute.

    Returns:
        int: The frequency of the first recovered sound.
    """

    registers = {}  # Dictionary to store register values
    sound = -1  # Most recently played sound frequency
    i = 0  # Instruction pointer

    while 0 <= i < len(data):  # Continue until we jump outside the program
        parts = data[i].split()  # Split the instruction into parts
        cmd = parts[0]  # The command (snd, set, add, etc.)
        x = parts[1]  # The first parameter (usually a register)

        # Helper function to get the value of a register or literal
        def get_val(v):
            """
            Get the value of a register or literal.

            Args:
                v (str): A register name or literal value.

            Returns:
                int: The value of the register or the literal as an integer.
            """
            if v.isalpha():  # If it's a letter (register name)
                return registers.get(v, 0)  # Get register value, default to 0
            return int(v)  # Otherwise, it's a literal value

        # Initialize register if it doesn't exist yet
        if x.isalpha() and x not in registers:
            registers[x] = 0

        # Execute the instruction based on the command
        if cmd == "snd":  # Play sound
            sound = get_val(x)
        elif cmd == "set":  # Set register
            y = parts[2]  # The second parameter
            registers[x] = get_val(y)
        elif cmd == "add":  # Add to register
            y = parts[2]
            registers[x] += get_val(y)
        elif cmd == "mul":  # Multiply register
            y = parts[2]
            registers[x] *= get_val(y)
        elif cmd == "mod":  # Modulo operation
            y = parts[2]
            registers[x] %= get_val(y)
        elif cmd == "rcv":  # Recover sound
            if get_val(x) != 0:
                return sound  # Return the last played sound
        elif cmd == "jgz":  # Jump if greater than zero
            y = parts[2]
            if get_val(x) > 0:
                i += get_val(y)  # Jump forward or backward
                continue  # Skip the normal increment

        i += 1  # Move to the next instruction

    return sound  # Return the last played sound if we exit normally


def part_two(data: list) -> int:
    """
    Simulate two programs running in parallel, communicating through message
    queues.

    Instructions are the same as in part_one, except:
    - snd X: Send value X to the other program's queue
    - rcv X: Receive a value from the queue and store it in register X

    The simulation runs until both programs are waiting for messages
    and both queues are empty (deadlock).

    Args:
        data (list): A list of instructions to execute.

    Returns:
        int: The number of times program 1 sends a value.
    """

    def create_program(pid):
        """
        Create a new program with the given ID.

        Args:
            pid (int): Program ID (0 or 1).

        Returns:
            dict: A dictionary representing the program's state.
        """

        return {
            "registers": {"p": pid},  # Initialize register 'p' with program ID
            "position": 0,  # Instruction pointer
            "queue": [],  # Message queue
            "send_count": 0,  # Counter for sent messages
            "waiting": False  # Flag for waiting on receive
        }

    programs = [create_program(0), create_program(1)]  # Create both programs

    # Helper function to get value
    def get_val(program, v):
        """
        Get the value of a register or literal for a specific program.

        Args:
            program (dict): The program's state.
            v (str): A register name or literal value.

        Returns:
            int: The value of the register or the literal as an integer.
        """

        if v.isalpha():  # If it's a letter (register name)
            # Return the register value, default to 0
            return program["registers"].get(v, 0)
        return int(v)  # Otherwise, it's a literal value

    # Run until deadlock (both programs waiting or terminated)
    while True:
        deadlock = True  # Assume deadlock until proven otherwise

        for pid in [0, 1]:  # Process both programs
            program = programs[pid]  # Current program
            other = programs[1 - pid]  # The other program

            # Skip if program is terminated (outside instruction range)
            if not (0 <= program["position"] < len(data)):
                continue

            # Skip if program is waiting and has no messages
            if program["waiting"] and not program["queue"]:
                continue

            # We can execute at least one instruction
            deadlock = False

            # Execute instruction
            parts = data[program["position"]].split()
            cmd = parts[0]  # The command
            x = parts[1]  # The first parameter

            # Initialize register if needed
            if x.isalpha() and x not in program["registers"]:
                program["registers"][x] = 0

            # Execute the instruction based on the command
            if cmd == "snd":  # Send value to other program
                val = get_val(program, x)
                other["queue"].append(val)  # Add to other program's queue
                program["send_count"] += 1  # Increment send counter
                program["position"] += 1
            elif cmd == "set":  # Set register
                y = parts[2]
                program["registers"][x] = get_val(program, y)
                program["position"] += 1
            elif cmd == "add":  # Add to register
                y = parts[2]
                program["registers"][x] += get_val(program, y)
                program["position"] += 1
            elif cmd == "mul":  # Multiply register
                y = parts[2]
                program["registers"][x] *= get_val(program, y)
                program["position"] += 1
            elif cmd == "mod":  # Modulo operation
                y = parts[2]
                program["registers"][x] %= get_val(program, y)
                program["position"] += 1
            elif cmd == "rcv":  # Receive value from queue
                if program["queue"]:  # If there's a message in the queue
                    # Get first message
                    program["registers"][x] = program["queue"].pop(0)

                    program["waiting"] = False
                    program["position"] += 1
                else:
                    program["waiting"] = True  # Wait for a message
            elif cmd == "jgz":  # Jump if greater than zero
                y = parts[2]
                if get_val(program, x) > 0:
                    program["position"] += get_val(program, y)
                else:
                    program["position"] += 1

        # If both programs are in deadlock, we're done
        if deadlock:
            break

    return programs[1]["send_count"]  # Return program 1's send count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 8600
    print("Part 2:", part_two(data))  # 7239
