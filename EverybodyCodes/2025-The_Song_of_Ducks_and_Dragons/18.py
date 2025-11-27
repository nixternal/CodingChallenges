#!/usr/bin/env python
"""
Plant Energy Network Calculator

This module calculates energy flow through a network of interconnected plants.
Each plant has a thickness threshold and receives energy from source plants
through branches with specific thickness multipliers.
"""

import re
from typing import Dict, List, Set, Tuple


def read_puzzle_input() -> List[str]:
    """Read and parse the puzzle input file."""
    with open("18.in", "r") as file:
        return file.read().split("\n\n\n\n")


def parse_plant_block(block: str) -> Tuple[int, int, List[Tuple[int, int]], bool]:
    """
    Parse a single plant block.

    Returns:
        (plant_number, thickness, branches, is_free)
        where branches is [(source_plant, branch_thickness), ...]
    """
    lines = block.splitlines()
    header = lines[0]
    branch_lines = lines[1:]

    # Parse plant header
    match = re.match(r"^Plant (\d+) with thickness (\d+):$", header)
    if not match:
        raise ValueError(f"Invalid plant header: {header}")

    plant_number = int(match[1])
    thickness = int(match[2])

    # Parse branches
    branches = []
    is_free = False

    for line in branch_lines:
        if line.startswith("- free"):
            is_free = True
            break

        match = re.match(r"^- branch to Plant (\d+) with thickness (-?\d+)$", line)
        if not match:
            raise ValueError(f"Invalid branch line: {line}")

        source_plant = int(match[1])
        branch_thickness = int(match[2])
        branches.append((source_plant, branch_thickness))

    return plant_number, thickness, branches, is_free


def parse_network(
    data: str,
) -> Tuple[Dict[int, int], Dict[int, List[Tuple[int, int]]], Set[int]]:
    """
    Parse network data into structured format.

    Returns:
        (thicknesses, branches, free_plants)
        - thicknesses: {plant_number: threshold}
        - branches: {plant_number: [(source, thickness), ...]}
        - free_plants: set of plant numbers that are free
    """
    thicknesses = {}
    branches = {}
    free_plants = set()

    for block in data.split("\n\n"):
        plant_num, thickness, plant_branches, is_free = parse_plant_block(block)

        thicknesses[plant_num] = thickness
        branches[plant_num] = plant_branches

        if is_free:
            free_plants.add(plant_num)

    return thicknesses, branches, free_plants


def calculate_energy(
    activations: List[int],
    plant_count: int,
    branches: Dict[int, List[Tuple[int, int]]],
    thresholds: Dict[int, int],
) -> Dict[int, int]:
    """
    Calculate energy levels for all plants.

    Args:
        activations: Initial energy values for first N plants
        plant_count: Total number of plants
        branches: Branch connections for each plant
        thresholds: Minimum energy threshold for each plant

    Returns:
        Dictionary mapping plant numbers to their energy levels
    """
    energy = {i + 1: value for i, value in enumerate(activations)}

    # Calculate energy for remaining plants in order
    for plant_num in range(len(activations) + 1, plant_count + 1):
        # Sum energy from all source branches
        total_energy = sum(
            energy[source] * thickness
            for source, thickness in branches.get(plant_num, [])
        )

        # Apply threshold: energy drops to 0 if below threshold
        energy[plant_num] = total_energy if total_energy >= thresholds[plant_num] else 0

    return energy


def part_one(data: List[str]) -> int:
    """
    Calculate final energy at the last plant with free/linked structure.

    Free plants start with energy 1, linked plants sum their source energies.
    """
    thresholds, branches, free_plants = parse_network(data[0])
    plant_count = len(thresholds)

    energy = {}

    for plant_num in range(1, plant_count + 1):
        if plant_num in free_plants:
            energy[plant_num] = 1
        else:
            total_energy = sum(
                energy[source] * thickness
                for source, thickness in branches.get(plant_num, [])
            )
            energy[plant_num] = (
                total_energy if total_energy >= thresholds[plant_num] else 0
            )

    return energy[plant_count]


def part_two(data: List[str]) -> int:
    """
    Sum energy outputs for multiple test activation patterns.
    """
    network_data, test_data = data[1].split("\n\n\n")
    thresholds, branches, _ = parse_network(network_data)
    plant_count = len(thresholds)

    total = 0
    for test_line in test_data.splitlines():
        activations = list(map(int, test_line.split()))
        energy = calculate_energy(activations, plant_count, branches, thresholds)
        total += energy[plant_count]

    return total


def part_three(data: List[str]) -> int:
    """
    Find optimal activation pattern and sum differences from test patterns.

    The optimal pattern activates plants with positive-thickness branches.
    """
    network_data, test_data = data[2].split("\n\n\n")
    thresholds, branches, _ = parse_network(network_data)
    plant_count = len(thresholds)

    # Find optimal activation: activate plants with positive incoming branches
    optimal_activation = [0] * 81
    for plant_branches in branches.values():
        for source, thickness in plant_branches:
            if thickness > 0 and source <= 81:
                optimal_activation[source - 1] = 1

    # Calculate optimal energy
    optimal_energy = calculate_energy(
        optimal_activation, plant_count, branches, thresholds
    )[plant_count]

    # Sum differences from optimal for all test patterns
    total = 0
    for test_line in test_data.splitlines():
        activations = list(map(int, test_line.split()))
        energy = calculate_energy(activations, plant_count, branches, thresholds)
        test_energy = energy[plant_count]

        if test_energy > 0:
            total += optimal_energy - test_energy

    return total


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2037668
    print("Part 2:", part_two(data))  # 11778745853
    print("Part 3:", part_three(data))  # 320110
