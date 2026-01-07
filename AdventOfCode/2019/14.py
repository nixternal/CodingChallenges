#!/usr/bin/env python

import math
from collections import defaultdict


def read_puzzle_input() -> list:
    with open("14.in", "r") as file:
        return file.read().splitlines()


def parse_reactions(data: list) -> dict:
    """Parse reactions into a dictionary keyed by output chemical."""
    reactions = {}

    for line in data:
        inputs, output = line.split(" => ")

        # Parse output
        out_qty, out_chem = output.strip().split()
        out_qty = int(out_qty)

        # Parse inputs
        ingredients = []
        for inp in inputs.split(", "):
            qty, chem = inp.strip().split()
            ingredients.append((int(qty), chem))

        reactions[out_chem] = (out_qty, ingredients)

    return reactions


def calculate_ore_needed(reactions: dict, fuel_amount: int = 1) -> int:
    """Calculate how much ORE is needed to produce the given amount of FUEL."""
    # Track what we need to produce
    needs = defaultdict(int)
    needs["FUEL"] = fuel_amount

    # Track excess materials we've produced
    excess = defaultdict(int)

    ore_needed = 0

    # Keep processing until only ORE is left
    while needs:
        # Find a chemical we need that isn't ORE
        chemical = None
        for chem in list(needs.keys()):
            if chem != "ORE":
                chemical = chem
                break

        if chemical is None:
            # Only ORE left
            ore_needed += needs.get("ORE", 0)
            break

        needed = needs[chemical]
        del needs[chemical]

        # Use any excess we have first
        if excess[chemical] > 0:
            used = min(excess[chemical], needed)
            excess[chemical] -= used
            needed -= used

        if needed <= 0:
            continue

        # Get the reaction for this chemical
        produces_qty, ingredients = reactions[chemical]

        # Calculate how many times we need to run this reaction
        times = math.ceil(needed / produces_qty)

        # Add the produced amount to excess
        produced = times * produces_qty
        leftover = produced - needed
        if leftover > 0:
            excess[chemical] += leftover

        # Add ingredients to our needs
        for qty, chem in ingredients:
            needs[chem] += qty * times

    return ore_needed


def part_one(data: list) -> int:
    """Calculate minimum ORE needed to produce 1 FUEL."""
    reactions = parse_reactions(data)
    return calculate_ore_needed(reactions, 1)


def part_two(data: list) -> int:
    """Calculate maximum FUEL that can be produced with 1 trillion ORE."""
    reactions = parse_reactions(data)
    target_ore = 1_000_000_000_000

    # Binary search for the answer
    # Lower bound: simple division (ignores leftovers, so underestimates)
    ore_per_fuel = calculate_ore_needed(reactions, 1)
    low = target_ore // ore_per_fuel

    # Upper bound: find by doubling until we exceed target
    high = low * 2
    while calculate_ore_needed(reactions, high) < target_ore:
        high *= 2

    # Binary search between low and high
    best = low
    while low <= high:
        mid = (low + high) // 2
        ore_needed = calculate_ore_needed(reactions, mid)

        if ore_needed <= target_ore:
            best = mid
            low = mid + 1
        else:
            high = mid - 1

    return best


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 374457
    print("Part 2:", part_two(data))  # 3568888
