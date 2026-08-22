#!/usr/bin/env python
"""
Day 3 puzzle: dice with 'pulse'-driven pseudo-random rolls.

Input blocks (separated by blank lines):
  1. Dice definitions only          -> part_one: total points >= target
  2. Dice definitions + a track     -> part_two: race finishing order
  3. Dice definitions + a grid      -> part_three: reachable coin count

Each die line looks like:  "<id>: faces=[<comma-separated ints>] seed=<int>"
"""

import re

DIE_RE = re.compile(r"^(\d+):\s+faces=\[([-\d,\s]+)\]\s+seed=(-?\d+)$")


def read_puzzle_input() -> list[list[str]]:
    """Read 03.in and split it into blank-line-separated blocks of lines."""
    with open("03.in", "r") as file:
        contents = file.read().strip()

    if not contents:
        return []

    blocks = re.split(r"\n[ \t]*\n", contents)

    return [
        [line.strip() for line in block.splitlines() if line.strip()]
        for block in blocks
    ]


def parse_dice(data: list[str]) -> tuple[list[int], list[list[int]], list[int]]:
    """Parse every 'faces=[...] seed=...' line into parallel id/faces/seed lists."""
    die_ids = []
    faces_by_die = []
    seeds = []

    for line in data:
        match = DIE_RE.fullmatch(line)

        if match is None:
            continue

        die_id_text, faces_text, seed_text = match.groups()

        die_ids.append(int(die_id_text))
        faces_by_die.append([int(value.strip()) for value in faces_text.split(",")])
        seeds.append(int(seed_text))

    return die_ids, faces_by_die, seeds


def roll_die(
    faces: list[int],
    seed: int,
    face_index: int,
    pulse: int,
    roll_number: int,
) -> tuple[int, int, int]:
    """Advance one die by one roll.

    Computes `spin` from the roll number and current pulse, uses it to move
    to a new face, then updates the pulse for next time. This is the single
    source of truth for the roll formula — both the synchronous (parts 1 & 3)
    and per-die asynchronous (part 2) simulations call this instead of each
    re-implementing the math.

    Returns (result, new_face_index, new_pulse).
    """
    spin = roll_number * pulse

    face_index = (face_index + spin) % len(faces)
    result = faces[face_index]

    pulse = (pulse + spin) % seed
    pulse += 1 + roll_number + seed

    return result, face_index, pulse


def simulate_until_target(data: list[str], target: int = 10_000) -> int:
    """Roll all dice together each round until total points reach target."""
    _die_ids, faces_by_die, seeds = parse_dice(data)

    # Every die starts on its first face, with pulse initialized to seed.
    positions = [0] * len(faces_by_die)
    pulses = seeds[:]

    total_points = 0
    roll_number = 1

    while total_points < target:
        roll_points = 0

        for die_index, faces in enumerate(faces_by_die):
            result, positions[die_index], pulses[die_index] = roll_die(
                faces,
                seeds[die_index],
                positions[die_index],
                pulses[die_index],
                roll_number,
            )
            roll_points += result

        total_points += roll_points
        roll_number += 1

    return roll_number - 1


def parse_track(data: list[str]) -> list[int]:
    """Find the single digit-string line describing the race track."""
    for line in data:
        if re.fullmatch(r"[1-9]+", line):
            return [int(character) for character in line]

    raise ValueError("Could not find a racetrack line")


def parse_grid(data: list[str]) -> list[list[int]]:
    """Parse the digit-grid lines (ignoring die definition lines) into a grid."""
    grid = []

    for line in data:
        if DIE_RE.fullmatch(line):
            continue

        if re.fullmatch(r"[1-9]+", line):
            grid.append([int(value) for value in line])
        else:
            raise ValueError(f"Invalid grid row: {line!r}")

    if not grid:
        raise ValueError("Could not find a grid")

    width = len(grid[0])

    if any(len(row) != width for row in grid):
        raise ValueError("All grid rows must have the same width")

    return grid


def reachable_coins_for_die(
    grid: list[list[int]],
    faces: list[int],
    seed: int,
) -> set[tuple[int, int]]:
    """Track every board cell an unlimited swarm of players could occupy
    while following one die's rolls, collecting a coin whenever a player
    lands on a matching cell. A coin only counts once, no matter how many
    players could reach it."""
    height = len(grid)
    width = len(grid[0])

    # Before roll 1, unlimited players may start on every board cell.
    reachable = {(row, column) for row in range(height) for column in range(width)}

    collected_coins = set()

    face_index = 0
    pulse = seed
    roll_number = 1

    while reachable:
        result, face_index, pulse = roll_die(
            faces,
            seed,
            face_index,
            pulse,
            roll_number,
        )

        # Players on non-matching squares leave the game.
        matching_positions = {
            (row, column) for row, column in reachable if grid[row][column] == result
        }

        # A coin can only enter the prize pool once, regardless of
        # how many players/dice could collect it.
        collected_coins.update(matching_positions)

        # Surviving players may stay or move one orthogonal square.
        next_reachable = set()

        for row, column in matching_positions:
            for row_offset, column_offset in (
                (0, 0),  # Stay
                (-1, 0),  # Up
                (1, 0),  # Down
                (0, -1),  # Left
                (0, 1),  # Right
            ):
                next_row = row + row_offset
                next_column = column + column_offset

                if 0 <= next_row < height and 0 <= next_column < width:
                    next_reachable.add((next_row, next_column))

        reachable = next_reachable
        roll_number += 1

    return collected_coins


def part_one(data: list[str]) -> int:
    return simulate_until_target(data)


def part_two(data: list[str]) -> str:
    die_ids, faces_by_die, seeds = parse_dice(data)
    track = parse_track(data)

    die_count = len(die_ids)

    # Per-die mechanism state.
    face_indices = [0] * die_count
    pulses = seeds[:]
    die_roll_numbers = [1] * die_count

    # Per-player race state.
    track_positions = [0] * die_count
    finished = [False] * die_count
    finishing_order = []

    while len(finishing_order) < die_count:
        for die_index in range(die_count):
            if finished[die_index]:
                continue

            result, face_indices[die_index], pulses[die_index] = roll_die(
                faces_by_die[die_index],
                seeds[die_index],
                face_indices[die_index],
                pulses[die_index],
                die_roll_numbers[die_index],
            )

            die_roll_numbers[die_index] += 1

            required_value = track[track_positions[die_index]]

            if result == required_value:
                track_positions[die_index] += 1

                if track_positions[die_index] == len(track):
                    finished[die_index] = True
                    finishing_order.append(die_ids[die_index])

    return ",".join(str(die_id) for die_id in finishing_order)


def part_three(data: list[str]) -> int:
    _die_ids, faces_by_die, seeds = parse_dice(data)
    grid = parse_grid(data)

    all_collectable_coins = set()

    for faces, seed in zip(faces_by_die, seeds):
        all_collectable_coins.update(reachable_coins_for_die(grid, faces, seed))

    return len(all_collectable_coins)


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data[0]))  # 637
    print("Part 2:", part_two(data[1]))  # 9,7,1,2,4,8,6,3,5
    print("Part 3:", part_three(data[2]))  # 154057
