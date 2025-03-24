#!/usr/bin/env python

import re


def read_puzzle_input() -> str:
    """
    Reads the puzzle input from a file named '25.in'.

    Returns:
        str: The raw input data as a string.
    """

    with open("25.in", "r") as file:
        return file.read()


def parse_input(data: str) -> tuple:
    """
    Parses the input data to extract the initial state, number of steps, and
    state transition rules.

    Args:
        data (str): The raw input data as a string.

    Returns:
        tuple: (initial_state (str), steps (int), states (dict))
            - initial_state: The state in which the Turing machine starts.
            - steps: The number of steps to execute.
            - states: A dictionary mapping state names to their transition
                      rules.
    """

    lines = data.strip().split('\n')

    # Extract initial state (last character of the 1st line, before the period)
    initial_state = lines[0].split()[-1][:-1]

    # Extract the number of steps to perform
    match = re.search(r'\d+', lines[1])
    if not match:
        raise ValueError("Could not extract the number of steps from input.")
    steps = int(match.group())

    # Dictionary to store states and their rules
    states = {}
    i = 3  # Start at the third line, where the first state definition begins
    while i < len(lines):
        # Extract the state name (e.g., "A" from "In state A:")
        state_name = lines[i].split()[-1][:-1]
        states[state_name] = {}

        # Extract rules for when the current value is 0
        write_0 = int(lines[i+2].split()[-1][:-1])  # "Write the value X."
        move_0 = 1 if "right" in lines[i+3] else -1  # "Move 1 slot left/right"
        next_0 = lines[i+4].split()[-1][:-1]  # "Continue with state X."

        # Extract rules for when the current value is 1
        write_1 = int(lines[i+6].split()[-1][:-1])  # "Write the value Y."
        move_1 = 1 if "right" in lines[i+7] else -1  # "Move 1 slot left/right"
        next_1 = lines[i+8].split()[-1][:-1]  # "Continue with state Y."

        # Store both conditions in the state dictionary
        states[state_name][0] = (write_0, move_0, next_0)
        states[state_name][1] = (write_1, move_1, next_1)

        # Move to the next state definition (each state block is 10 lines long)
        i += 10

    return initial_state, steps, states


if __name__ == "__main__":
    # Read and parse the input file
    data = read_puzzle_input()
    initial_state, steps, states = parse_input(data)

    # Use a set to store positions with value 1, as the default value is 0
    # Instead of a dictionary, we use a set to track positions holding `1`
    tape = set()
    cursor = 0  # The current position of the Turing machine
    state = initial_state  # The current active state of the machine

    # Run the Turing machine for the given number of steps
    for _ in range(steps):
        # Cache transition rules for current state
        state_rules = states[state]
        # Check if current position is in the set (1) or not (0)
        current_value = 1 if cursor in tape else 0

        # Get the rule for the current value
        write_value, direction, state = state_rules[current_value]

        # Update the tape based on the rule
        if write_value == 1:
            tape.add(cursor)  # Store position if writing 1
        else:
            tape.discard(cursor)  # Remove position if writing 0

        # Move the cursor left or right
        cursor += direction

    # The checksum is the number of 1s on the tape (size of the set)
    print(f"Part 1: {len(tape)}")  # Expected output: 5593
