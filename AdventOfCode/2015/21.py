#!/usr/bin/env python

from itertools import combinations

# Item stats: Each item is represented as a tuple (name, cost, damage, armor)

# List of weapons available for purchase
weapons = [
    # Name, Cost, Damage, Armor
    ("Dagger", 8, 4, 0),
    ("Shortsword", 10, 5, 0),
    ("Warhammer", 25, 6, 0),
    ("Longsword", 40, 7, 0),
    ("Greataxe", 74, 8, 0),
]

# List of armor available for purchase
armor = [
    # Name, Cost, Damage, Armor
    ("No Armor", 0, 0, 0),  # Optional armor
    ("Leather", 13, 0, 1),
    ("Chainmail", 31, 0, 2),
    ("Splintmail", 53, 0, 3),
    ("Bandedmail", 75, 0, 4),
    ("Platemail", 102, 0, 5),
]

# List of rings available for purchase
rings = [
    # Name, Cost, Damage, Armor
    ("No Ring 1", 0, 0, 0),  # Optional ring 1
    ("No Ring 2", 0, 0, 0),  # Optional ring 2
    ("Damage +1", 25, 1, 0),
    ("Damage +2", 50, 2, 0),
    ("Damage +3", 100, 3, 0),
    ("Defense +1", 20, 0, 1),
    ("Defense +2", 40, 0, 2),
    ("Defense +3", 80, 0, 3),
]


def generate_item_combinations():
    """
    Generate all possible combinations of items the player can equip.
    Includes one weapon (mandatory), optional armor, and up to two rings.

    Yields:
        list: A combination of weapon, armor, and rings.
    """

    for weapon in weapons:
        for arm in armor:
            # Choose up to 2 rings (0, 1, or 2 rings)
            for ring_combo in combinations(rings, 2):
                yield [weapon, arm, *ring_combo]


def calculate_damage(attacker_damage, defender_armor):
    """
    Calculate the effective damage dealt in a single turn.

    Args:
        attacker_damage (int): The attacker's damage stat.
        defender_armor (int): The defender's armor stat.

    Returns:
        int: Effective damage dealt (minimum of 1).
    """

    return max(1, attacker_damage - defender_armor)


def simulate_fight(player_hp, player_damage, player_armor, boss_hp,
                   boss_damage, boss_armor):
    """
    Simulate a turn-based fight between the player and the boss.

    Args:
        player_hp (int): Player's hit points.
        player_damage (int): Player's damage stat.
        player_armor (int): Player's armor stat.
        boss_hp (int): Boss's hit points.
        boss_damage (int): Boss's damage stat.
        boss_armor (int): Boss's armor stat.

    Returns:
        bool: True if the player wins, False otherwise.
    """

    # Calculate the number of turns required for each to defeat the other
    player_turns_to_win = (
        boss_hp + calculate_damage(
            player_damage, boss_armor) - 1) // calculate_damage(
            player_damage, boss_armor)
    boss_turns_to_win = (
        player_hp + calculate_damage(
            boss_damage, player_armor) - 1) // calculate_damage(
            boss_damage, player_armor)
    return player_turns_to_win <= boss_turns_to_win


def find_least_expensive_win(player_hp, boss_hp, boss_damage, boss_armor):
    """
    Find the least amount of gold spent to ensure a win against the boss.

    Args:
        player_hp (int): Player's hit points.
        boss_hp (int): Boss's hit points.
        boss_damage (int): Boss's damage stat.
        boss_armor (int): Boss's armor stat.

    Returns:
        int: Minimum gold spent to win.
    """

    min_gold_spent = float('inf')
    for items in generate_item_combinations():
        # Calculate player stats
        total_cost = sum(item[1] for item in items)    # Calculate total cost
        total_damage = sum(item[2] for item in items)  # Calculate total damage
        total_armor = sum(item[3] for item in items)   # Calculate total armor

        # Check if this combination wins the fight
        if simulate_fight(player_hp, total_damage, total_armor, boss_hp,
                          boss_damage, boss_armor):
            min_gold_spent = min(min_gold_spent, total_cost)
    return int(min_gold_spent)


def find_most_expensive_loss(player_hp, boss_hp, boss_damage, boss_armor):
    """
    Find the most gold that can be spent while still losing to the boss.

    Args:
        player_hp (int): Player's hit points.
        boss_hp (int): Boss's hit points.
        boss_damage (int): Boss's damage stat.
        boss_armor (int): Boss's armor stat.

    Returns:
        int: Maximum gold spent while losing.
    """

    max_gold_spent = 0
    for items in generate_item_combinations():
        # Calculate player stats
        total_cost = sum(item[1] for item in items)    # Calculate total cost
        total_damage = sum(item[2] for item in items)  # Calculate total damage
        total_armor = sum(item[3] for item in items)   # Calculate total armor

        # Check if this combination results in a loss
        if not simulate_fight(player_hp, total_damage, total_armor, boss_hp,
                              boss_damage, boss_armor):
            max_gold_spent = max(max_gold_spent, total_cost)
    # None if no loss is possible
    return int(max_gold_spent) if max_gold_spent > 0 else -1


def part_one(data: list) -> int:
    """
    Solve Part 1: Find the least gold spent to ensure a win.
    """

    return find_least_expensive_win(data[0], data[1], data[2], data[3])


def part_two(data: list) -> int:
    """
    Solve Part 2: Find the most gold spent while still losing.
    """

    return find_most_expensive_loss(data[0], data[1], data[2], data[3])


if __name__ == "__main__":
    # Player Hit Points, Boss Hit Points, Boss Damage, Boss Armor
    data = [
        100,  # Player Hit Points
        109,  # Boss Hit Points
        8,    # Boss Damage
        2,    # Boss Armor
    ]
    print("Part 1:", part_one(data))  # 111
    print("Part 2:", part_two(data))  # 188
