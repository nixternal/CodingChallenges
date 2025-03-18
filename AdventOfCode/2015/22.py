#!/usr/bin/env python

import sys

# Hard Mode
HARD_MODE = True

# Boss Stats
boss_hp = 55
boss_damage = 8

# Player Stats
player_hp = 50
player_mana = 500

MIN_MANA_SPENT = sys.maxsize

SPELLS = {
    "Magic Missile": {"cost": 53,  "damage": 4},
    "Drain":         {"cost": 73,  "damage": 2, "heal": 2},
    "Shield":        {"cost": 113, "armor": 7,  "duration": 6},
    "Poison":        {"cost": 173, "damage": 3, "duration": 6},
    "Recharge":      {"cost": 229, "mana": 101, "duration": 5}
}


def simulate(player_hp, player_mana, boss_hp, player_armor, effects,
             mana_spent, hard_mode, player_turn):
    global MIN_MANA_SPENT

    # Hard Mode
    if hard_mode and player_turn:
        player_hp -= 1
        if player_hp <= 0:
            return

    # Apply active effects
    if effects.get("Shield", 0) > 0:
        player_armor = 7
        effects["Shield"] -= 1
    else:
        player_armor = 0

    if effects.get("Poison", 0) > 0:
        boss_hp -= 3
        effects["Poison"] -= 1

    if effects.get("Recharge", 0) > 0:
        player_mana += 101
        effects["Recharge"] -= 1

    # Check win/lose conditions
    if boss_hp <= 0:
        MIN_MANA_SPENT = min(MIN_MANA_SPENT, mana_spent)
        return
    if player_hp <= 0 or mana_spent >= MIN_MANA_SPENT:
        return

    # Player's turn
    if player_turn:
        for spell, details in SPELLS.items():
            # Skip spells the player can't afford
            if details["cost"] > player_mana:
                continue

            # Skip spells that are already active
            if spell in effects and effects[spell] > 0:
                continue

            # Apply the spell's effects
            new_effects = effects.copy()
            new_player_hp = player_hp
            new_player_mana = player_mana - details["cost"]
            new_mana_spent = mana_spent + details["cost"]
            new_boss_hp = boss_hp

            if spell == "Magic Missile":
                new_boss_hp -= details["damage"]
            elif spell == "Drain":
                new_boss_hp -= details["damage"]
                new_player_hp += details["heal"]
            elif spell == "Shield":
                new_effects["Shield"] = details["duration"]
            elif spell == "Poison":
                new_effects["Poison"] = details["duration"]
            elif spell == "Recharge":
                new_effects["Recharge"] = details["duration"]

            simulate(new_player_hp, new_player_mana, new_boss_hp, player_armor,
                     new_effects, new_mana_spent, hard_mode, player_turn=False)

    # Boss's turn
    else:
        damage = max(1, boss_damage - player_armor)
        simulate(player_hp - damage, player_mana, boss_hp, player_armor,
                 effects, mana_spent, hard_mode, player_turn=True)


def part_one() -> int:
    simulate(player_hp=player_hp,
             player_mana=player_mana,
             boss_hp=boss_hp,
             player_armor=0,
             effects={"Shield": 0, "Poison": 0, "Recharge": 0},
             mana_spent=0,
             hard_mode=False,
             player_turn=True
             )
    return MIN_MANA_SPENT


def part_two() -> int:
    global MIN_MANA_SPENT
    MIN_MANA_SPENT = sys.maxsize
    simulate(player_hp=player_hp,
             player_mana=player_mana,
             boss_hp=boss_hp,
             player_armor=0,
             effects={"Shield": 0, "Poison": 0, "Recharge": 0},
             mana_spent=0,
             hard_mode=True,
             player_turn=True
             )
    return MIN_MANA_SPENT


if __name__ == "__main__":
    print("Part 1:", part_one())  # 953
    print("Part 2:", part_two())  # 1289
