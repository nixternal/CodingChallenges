#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    with open("12.in", "r") as file:
        return file.read().splitlines()


def parse_moons(data: list) -> list:
    """Parse moon positions from input lines like '<x=-1, y=0, z=2>'"""
    moons = []
    for line in data:
        # Extract all integers (including negative)
        nums = list(map(int, re.findall(r'-?\d+', line)))
        # Position [x, y, z] and velocity [0, 0, 0]
        moons.append({'pos': nums, 'vel': [0, 0, 0]})
    return moons


def apply_gravity(moons: list) -> None:
    """Update velocities by applying gravity between all pairs of moons"""
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            for axis in range(3):
                if moons[i]['pos'][axis] < moons[j]['pos'][axis]:
                    moons[i]['vel'][axis] += 1
                    moons[j]['vel'][axis] -= 1
                elif moons[i]['pos'][axis] > moons[j]['pos'][axis]:
                    moons[i]['vel'][axis] -= 1
                    moons[j]['vel'][axis] += 1


def apply_velocity(moons: list) -> None:
    """Update positions by applying velocity"""
    for moon in moons:
        for axis in range(3):
            moon['pos'][axis] += moon['vel'][axis]


def simulate_step(moons: list) -> None:
    """Run one time step of the simulation"""
    apply_gravity(moons)
    apply_velocity(moons)


def calculate_energy(moons: list) -> int:
    """Calculate total energy of the system"""
    total = 0
    for moon in moons:
        potential = sum(abs(p) for p in moon['pos'])
        kinetic = sum(abs(v) for v in moon['vel'])
        total += potential * kinetic
    return total


def get_axis_state(moons: list, axis: int) -> tuple:
    """Get the state of a single axis (position and velocity)"""
    return tuple((moon['pos'][axis], moon['vel'][axis]) for moon in moons)


def gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Calculate least common multiple"""
    return abs(a * b) // gcd(a, b)


def part_one(data: list) -> int:
    """Simulate for 1000 steps and calculate total energy"""
    moons = parse_moons(data)

    for _ in range(1000):
        simulate_step(moons)

    return calculate_energy(moons)


def part_two(data: list) -> int:
    """Find when the system returns to its initial state"""
    moons = parse_moons(data)

    # Store initial state for each axis
    initial_states = [get_axis_state(moons, axis) for axis in range(3)]

    # Find cycle length for each axis independently
    cycles = [0, 0, 0]
    steps = 0

    while not all(cycles):
        simulate_step(moons)
        steps += 1

        # Check each axis that hasn't found its cycle yet
        for axis in range(3):
            if cycles[axis] == 0:
                if get_axis_state(moons, axis) == initial_states[axis]:
                    cycles[axis] = steps

    # The full cycle is the LCM of all three axis cycles
    result = cycles[0]
    for cycle in cycles[1:]:
        result = lcm(result, cycle)
    return result


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 13500
    print("Part 2:", part_two(data))  # 278013787106916
