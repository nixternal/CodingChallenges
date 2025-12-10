#!/usr/bin/env python
# Advent of Code 2019 – Day 6 (Orbital Transfers)
# -------------------------------------------------
# The input file `06.in` contains lines like:
#   COM)B
#   B)C
# meaning "object C orbits object B".
#
# The goal:
#   * Part 1: Count the total number of direct + indirect orbits.
#   * Part 2: Find the minimum number of orbital transfers required
#              to move from YOU's parent to SAN's parent.


def read_puzzle_input() -> list[str]:
    """Return a list of orbit pair strings (e.g. 'COM)B')."""
    with open("06.in", "r") as file:
        return file.read().splitlines()


def build_orbit_map(data: list[str]) -> dict[str, str]:
    """
    Build a mapping from child → parent.

    Example:
        data = ['COM)B', 'B)C']
        returns {'B': 'COM', 'C': 'B'}
    """
    orbits: dict[str, str] = {}
    for line in data:
        parent, child = line.split(")")
        orbits[child] = parent
    return orbits


def part_one(data: list[str]) -> int:
    """Count total direct + indirect orbits."""
    orbits = build_orbit_map(data)

    total_orbits = 0
    # For every object, walk up to COM counting steps.
    for node in orbits:
        current = node
        while current in orbits:  # until we reach the root (COM)
            total_orbits += 1
            current = orbits[current]
    return total_orbits


def part_two(data: list[str]) -> int:
    """Find minimum orbital transfers between YOU and SAN."""
    orbits = build_orbit_map(data)

    # ------------------------------------------------------------------
    # Helper: return a list of ancestors from *node* up to COM,
    #          excluding the starting node itself.
    # ------------------------------------------------------------------
    def get_ancestors(node: str) -> list[str]:
        ancestors: list[str] = []
        while node in orbits:
            node = orbits[node]
            ancestors.append(node)
        return ancestors

    you_ancestors = get_ancestors("YOU")  # e.g. ['K', 'J', ... , 'COM']
    san_ancestors = get_ancestors("SAN")  # e.g. ['I', 'D', ... , 'COM']

    # Convert SAN's list to a set for O(1) look‑ups.
    san_set = set(san_ancestors)

    # Find the first common ancestor (closest to YOU).
    common = next(a for a in you_ancestors if a in san_set)

    # Distance from YOU to common + distance from SAN to common
    return you_ancestors.index(common) + san_ancestors.index(common)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 110190
    print("Part 2:", part_two(data))  # 343
