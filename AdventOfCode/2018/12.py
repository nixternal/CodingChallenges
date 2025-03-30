#!/usr/bin/env python

"""
Advent of Code: Plant Pot Simulator

This program simulates the growth of plants in pots, where each plant's state
(whether it has a plant or not) evolves according to specific rules based on
its own state and the states of its neighbors.

The problem has two parts:
1. Calculate sum of pot numbers containing plants after 20 generations
2. Calculate sum of pot numbers containing plants after 50 billion generations
"""

from typing import Dict, Tuple


def read_puzzle_input() -> Tuple[str, Dict[str, str]]:
    """
    Read the puzzle input from the file '12.in'.

    Returns:
        Tuple[str, Dict[str, str]]: A pair containing:
            - initial_state: String representation of plants in pots
            - rules: Dictionary mapping 5-pot patterns to resulting center
                     pot states
    """

    with open("12.in", "r") as file:
        lines = file.read().strip().split("\n")
        initial_state: str = lines[0].split(": ")[1]
        rules: Dict[str, str] = {}

        for line in lines[2:]:
            pattern, result = line.split(" => ")
            rules[pattern] = result

        return initial_state, rules


def simulate_growth(
        initial_state: str,
        rules: Dict[str, str],
        generations: int) -> int:
    """
    Simulate plant growth over multiple generations.

    The simulation handles pattern matching for each position and detects
    cycles in the growth pattern. When a repeating pattern is detected, it
    calculates the final result without simulating all generations.

    Args:
        initial_state: String of '#' (plant) and '.' (no plant) representing
                       the initial state
        rules: Dictionary mapping 5-character patterns to their resulting state
        generations: Number of generations to simulate

    Returns:
        Sum of indices of all pots containing plants in the final generation
    """

    state: str = initial_state
    offset: int = 0  # Tracks the index of the leftmost pot
    # Maps states to (generation, offset) for cycle detection
    seen_states: Dict[str, Tuple[int, int]] = {}

    for gen in range(generations):
        # Add padding to handle edge patterns
        state = "...." + state + "...."
        offset -= 2
        new_state: str = ""

        # Apply rules to each possible 5-pot segment
        for i in range(len(state) - 4):
            segment: str = state[i:i+5]
            new_state += rules.get(segment, ".")

        # Trim leading/trailing empty pots and adjust offset
        first_plant: int = new_state.find('#')
        if first_plant == -1:  # No plants left
            return 0

        state = new_state[first_plant:].rstrip('.')
        offset += first_plant

        # Check if we've seen this state pattern before (cycle detection)
        if state in seen_states:
            prev_gen, prev_offset = seen_states[state]

            # Calculate cycle properties
            cycle_length: int = gen - prev_gen
            offset_diff_per_cycle: int = offset - prev_offset

            # Calculate how many complete cycles remain
            remaining_cycles: int = (generations - gen - 1) // cycle_length

            # Calculate the final offset after all remaining cycles
            final_offset: int = offset + (
                remaining_cycles * offset_diff_per_cycle)

            # Calculate the final sum w/o simulating the remaining generations
            return sum(
                i + final_offset for i, c in enumerate(state) if c == '#'
            )

        # Record current state for cycle detection
        seen_states[state] = (gen, offset)

    # If we completed all generations without finding a cycle
    return sum(i + offset for i, c in enumerate(state) if c == '#')


def part_one(data: Tuple[str, Dict[str, str]]) -> int:
    """
    Solve part one: sum of pot numbers containing plants after 20 generations.

    Args:
        data: The initial state and rules as returned by read_puzzle_input()

    Returns:
        The sum of indices of all pots containing plants after 20 generations
    """

    initial_state, rules = data
    return simulate_growth(initial_state, rules, 20)


def part_two(data: Tuple[str, Dict[str, str]]) -> int:
    """
    Solve part two: sum of pot numbers containing plants after 50 billion
    generations.

    This would be impossible to simulate directly, but the solution relies on
    detecting repeating patterns that occur after a certain number of
    generations.

    Args:
        data: The initial state and rules as returned by read_puzzle_input()

    Returns:
        The sum of indices of all pots containing plants after 50 billion
        generations
    """

    initial_state, rules = data
    return simulate_growth(initial_state, rules, 50_000_000_000)


if __name__ == "__main__":
    data: Tuple[str, Dict[str, str]] = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2736
    print("Part 2:", part_two(data))  # 3150000000905
