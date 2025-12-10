#!/usr/bin/env python

import re
from itertools import combinations
from z3 import Int, Optimize, Sum, sat


def read_puzzle_input() -> list:
    # Reads the input file (10.in is expected to be in the execution directory)
    with open("10.in", "r") as file:
        return file.read().splitlines()


def lights_out(line: str) -> int:
    """
    Solves the 'Lights Out' variation using brute-force combinations.
    """
    light_match = re.search(r"\[([.#]+)\]", line)
    if not light_match:
        return 0

    light_str = light_match.group(1)
    target_mask = 0
    for i, char in enumerate(light_str):
        if char == "#":
            target_mask |= 1 << i

    button_matches = re.findall(r"\(([\d,]+)\)", line)
    buttons = []
    for b_str in button_matches:
        mask = 0
        indices = [int(x) for x in b_str.split(",")]
        for idx in indices:
            mask |= 1 << idx
        buttons.append(mask)

    num_buttons = len(buttons)
    for r in range(num_buttons + 1):
        for combo in combinations(buttons, r):
            current_state = 0
            for btn_mask in combo:
                current_state ^= btn_mask
            if current_state == target_mask:
                return r
    return 0


def joltage_counters(line: str) -> int:
    """
    Solves the joltage problem using the Z3 SMT optimizer.
    """
    # 1. Parse Joltage Requirements (b)
    joltage_match = re.search(r"\{([\d,]+)\}", line)
    if not joltage_match:
        return 0
    target_list = [int(x) for x in joltage_match.group(1).split(",")]
    N = len(target_list)  # Number of equations/counters

    # 2. Parse Button Schematics (A)
    button_matches = re.findall(r"\(([\d,]+)\)", line)
    buttons_vectors = []
    for b_str in button_matches:
        vec = [0] * N
        indices = [int(x) for x in b_str.split(",")]
        for idx in indices:
            if idx < N:
                vec[idx] = 1
        buttons_vectors.append(tuple(vec))

    M = len(buttons_vectors)  # Number of variables/buttons
    if N == 0 or M == 0:
        return 0

    # --- Z3 Solver Setup ---

    # 1. Create the Z3 Optimizer
    o = Optimize()

    # 2. Create M Integer Variables (x_i) for the button presses
    x = [Int(f"x_{i}") for i in range(M)]

    # 3. Add Constraints:
    for i in range(M):
        # All button presses must be non-negative integers (x_i >= 0)
        o.add(x[i] >= 0)

    # 4. Add the Linear System Constraints (A*x = b):
    for i in range(N):
        # Calculate the expression for the i-th counter
        contribution = Sum([buttons_vectors[j][i] * x[j] for j in range(M)])

        # Set the constraint: contribution must equal the target joltage
        o.add(contribution == target_list[i])

    # 5. Set the Minimization Goal and store the objective handle
    # CORRECTED: Store the result of minimize() in objective_handle
    objective_handle = o.minimize(Sum(x))

    # 6. Solve
    if o.check() == sat:
        # The optimizer found a solution. The minimized value is the result.
        # CORRECTED: Use the objective handle with o.lower()
        min_presses = o.lower(objective_handle)
        return min_presses.as_long()  # type: ignore[attr-defined]
    else:
        # No solution exists
        return 0


def part_one(data: list) -> int:
    total = 0
    for line in data:
        if line.strip():
            total += lights_out(line)
    return total


def part_two(data: list) -> int:
    total = 0
    for line in data:
        if line.strip():
            total += joltage_counters(line)
    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 475
    print("Part 2:", part_two(data))  # 18273
