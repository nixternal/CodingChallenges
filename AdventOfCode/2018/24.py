#!/usr/bin/env python

import re
from copy import deepcopy
from typing import Optional


def read_puzzle_input() -> str:
    with open("24.in", "r") as file:
        return file.read()


def parse_input(data: str) -> tuple[list[dict], list[dict]]:
    """Parse puzzle input into immune system and infection armies."""

    def parse_army(block: str, army_name: str) -> list[dict]:
        """Parse a single army block into group dictionaries."""
        groups = []

        for line in block.strip().splitlines()[1:]:  # Skip header line
            # Extract all numbers
            numbers = list(map(int, re.findall(r"\d+", line)))
            units, hp = numbers[0], numbers[1]
            attack, initiative = numbers[-2], numbers[-1]

            # Extract weaknesses and immunities
            weaknesses = re.findall(r"weak to ([a-z, ]+)", line)
            immunities = re.findall(r"immune to ([a-z, ]+)", line)

            # Extract attack type
            attack_match = re.search(r'(\w+) damage', line)
            attack_type = attack_match.group(1) if attack_match else 'unknown'

            groups.append(
                {
                    "army": army_name,
                    "units": units,
                    "hp": hp,
                    "attack": attack,
                    "attack_type": attack_type,
                    "initiative": initiative,
                    "weaknesses": frozenset(weaknesses[0].split(", "))
                    if weaknesses
                    else frozenset(),
                    "immunities": frozenset(immunities[0].split(", "))
                    if immunities
                    else frozenset(),
                }
            )

        return groups

    immune_block, infection_block = data.split("\n\n")
    immune_army = parse_army(immune_block, "immune")
    infection_army = parse_army(infection_block, "infection")

    return immune_army, infection_army


def effective_power(group: dict) -> int:
    """Calculate total damage output: units × attack."""
    return group["units"] * group["attack"]


def calculate_damage(attacker: dict, defender: dict) -> int:
    """Calculate damage attacker would deal to defender."""
    if attacker["attack_type"] in defender["immunities"]:
        return 0

    damage = effective_power(attacker)
    if attacker["attack_type"] in defender["weaknesses"]:
        damage *= 2

    return damage


def select_targets(groups: list[dict]) -> dict[int, dict]:
    """
    Target selection phase: groups choose targets in order of power and initiative.
    Returns mapping of attacker initiative -> defender dict.
    """
    # Sort by effective power (desc), then initiative (desc)
    selection_order = sorted(
        groups, key=lambda g: (effective_power(g), g["initiative"]), reverse=True
    )

    available_targets = set(g["initiative"] for g in groups)
    targets = {}

    for attacker in selection_order:
        # Find enemies that can be damaged
        potential_targets = [
            defender
            for defender in groups
            if defender["army"] != attacker["army"]
            and defender["initiative"] in available_targets
            and calculate_damage(attacker, defender) > 0
        ]

        if not potential_targets:
            continue

        # Choose target with max damage, then power, then initiative
        target = max(
            potential_targets,
            key=lambda d: (
                calculate_damage(attacker, d),
                effective_power(d),
                d["initiative"],
            ),
        )

        targets[attacker["initiative"]] = target
        available_targets.remove(target["initiative"])

    return targets


def execute_attacks(groups: list[dict], targets: dict[int, dict]) -> int:
    """
    Attack phase: groups attack in initiative order.
    Returns total units killed this round.
    """
    total_killed = 0

    # Attack in initiative order (descending)
    for initiative in sorted(targets.keys(), reverse=True):
        # Find attacker (might be dead)
        attacker = next((g for g in groups if g["initiative"] == initiative), None)
        if not attacker or attacker["units"] <= 0:
            continue

        defender = targets[initiative]
        damage = calculate_damage(attacker, defender)
        units_killed = min(damage // defender["hp"], defender["units"])
        defender["units"] -= units_killed
        total_killed += units_killed

    return total_killed


def simulate_battle(
    immune: list[dict], infection: list[dict]
) -> Optional[tuple[str, int]]:
    """
    Run complete battle simulation.
    Returns (winning_army, remaining_units) or None if stalemate.
    """
    all_groups = immune + infection

    while True:
        # Remove dead groups
        all_groups = [g for g in all_groups if g["units"] > 0]

        # Check for winner
        armies_remaining = {g["army"] for g in all_groups}
        if len(armies_remaining) == 1:
            winner = armies_remaining.pop()
            total_units = sum(g["units"] for g in all_groups)
            return winner, total_units

        # Target selection
        targets = select_targets(all_groups)

        # No valid targets = stalemate
        if not targets:
            return None

        # Execute attacks
        units_killed = execute_attacks(all_groups, targets)

        # No casualties = stalemate
        if units_killed == 0:
            return None


def part_one(data: str) -> int:
    immune, infection = parse_input(data)

    result = simulate_battle(deepcopy(immune), deepcopy(infection))
    return result[1] if result else 0


def part_two(data: str) -> int:
    immune_template, infection_template = parse_input(data)

    boost = 1
    while True:
        # Create boosted immune army
        immune = deepcopy(immune_template)
        for group in immune:
            group["attack"] += boost

        # Create fresh infection army
        infection = deepcopy(infection_template)

        result = simulate_battle(immune, infection)

        # Check if immune system won
        if result and result[0] == "immune":
            return result[1]

        boost += 1


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 15919
    print("Part 2:", part_two(data))  # 354
