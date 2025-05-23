#!/usr/bin/env python


from ast import parse


def read_puzzle_input() -> list:
    with open("03.in", "r") as file:
        return file.read().splitlines()


def parse_wire(path):
    """Parses a wire path string into a list of coordinates."""
    x = y = 0
    coords = []
    for step in path.split(","):
        direction, distance = step[0], int(step[1:])
        if direction == "R":
            coords += [(x + i, y) for i in range(1, distance + 1)]
            x += distance
        elif direction == "L":
            coords += [(x - i, y) for i in range(1, distance + 1)]
            x -= distance
        elif direction == "U":
            coords += [(x, y + i) for i in range(1, distance + 1)]
            y += distance
        else:  # direction == "D"
            coords += [(x, y - i) for i in range(1, distance + 1)]
            y -= distance
    return coords


def find_intersections(wire1, wire2):
    """Finds all intersection points between two wires."""
    return set(wire1) & set(wire2)


def manhattan_distance(point):
    """Calculates the Manhattan distance from point (0, 0)."""
    return abs(point[0]) + abs(point[1])


def part_one(data: list) -> int:
    wire1, wire2 = data
    intersections = find_intersections(parse_wire(wire1), parse_wire(wire2))
    return min(manhattan_distance(p) for p in intersections)


def part_two(data: list) -> int:
    wire1, wire2 = data
    wire1_coords = parse_wire(wire1)
    wire2_coords = parse_wire(wire2)
    intersections = find_intersections(wire1_coords, wire2_coords)
    return min(wire1_coords.index(p) + wire2_coords.index(p) for p in intersections) + 2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 280
    print("Part 2:", part_two(data))  # 10554
