#!/usr/bin/env python

"""
Solution for Advent of Code 2017 - Day 20: Particle Swarm

This script simulates a system of particles moving in 3D space under
acceleration, velocity, and position constraints. The goal is to:
    - Find the particle that stays closest to the origin in the long run.
    - Detect and remove colliding particles.
"""

import copy
import re


class Particle:
    """
    Represents a particle with position, velocity, and acceleration in a 3D
    space. Each particle follows basic kinematics where acceleration affects
    velocity, and velocity affects position.
    """

    def __init__(self, index, position, velocity, acceleration):
        self.index = index                  # Unique ID for the particle
        self.position = position            # Current position (x, y, z)
        self.velocity = velocity            # Current velocity (x, y, z)
        self.acceleration = acceleration    # Current acceleration (x, y, z)

    def update(self):
        """
        Updates the particle's velocity and position based on acceleration.
        """

        self.velocity = tuple(v + a for v, a in zip(self.velocity,
                                                    self.acceleration))
        self.position = tuple(p + v for p, v in zip(self.position,
                                                    self.velocity))

    def manhattan_distance(self):
        """Computes the Manhattan distance from the origin (0,0,0)."""

        return sum(abs(x) for x in self.position)


def read_puzzle_input() -> list:
    """
    Reads and parses the input file, creating a list of Particle objects.
    Input format: p=<x,y,z>, v=<x,y,z>, a=<x,y,z>
    """

    particles = []
    pattern = re.compile(r'<(-?\d+),(-?\d+),(-?\d+)>')
    with open("20.in", "r") as file:
        for i, line in enumerate(file.read().splitlines()):
            values = list(map(int,
                              pattern.findall(line)[0] +
                              pattern.findall(line)[1] +
                              pattern.findall(line)[2]))
            p, v, a = values[:3], values[3:6], values[6:]
            particles.append(Particle(i, tuple(p), tuple(v), tuple(a)))
    return particles


def part_one(data: list) -> int:
    """
    Determines which particle will stay closest to the origin in the long run.
    We assume that acceleration dominates over time, so we find the particle
    with the smallest acceleration magnitude first, and in case of ties,
    we compare velocity and initial position.
    """

    particles = copy.deepcopy(data)  # Prevent modifying original data

    # Simulate for a long time to allow acceleration to dominate
    for _ in range(1000):
        for p in particles:
            p.update()
    return min(particles, key=lambda p: p.manhattan_distance()).index


def part_two(data: list) -> int:
    """
    Simulates particle movement while removing particles that collide.
    Runs until no more collisions occur or a sufficient number of iterations
    has passed.
    """

    particles = copy.deepcopy(data)  # Prevent modifying original data

    for _ in range(1000):  # Simulate long enough to resolve most collisions
        positions = {}
        to_remove = set()

        # Move particles and track positions
        for p in particles:
            p.update()
            if p.position in positions:
                to_remove.add(p.position)  # Mark this position for removal
            positions.setdefault(p.position, []).append(p)

        # Remove all particles that occupy a position marked for collision
        particles = [p for p in particles if p.position not in to_remove]

    return len(particles)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 308
    print("Part 2:", part_two(data))  # 504
