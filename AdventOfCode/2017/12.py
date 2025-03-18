#!/usr/bin/env python

from collections import deque


def read_puzzle_input() -> dict:
    """
    Parses the input text into a dictionary where each key is a program ID
    and the value is a set of directly connected program IDs.
    """

    data = {}
    with open("12.in", "r") as file:
        for line in file.read().splitlines():
            program, connections = line.split(' <-> ')
            data[int(program)] = set(map(int, connections.split(', ')))
        return data


def bfs(data: dict, start: int) -> set:
    """
    Performs a breadth-first search (BFS) starting from a given node
    and returns all nodes that are reachable from that starting node.
    """

    queue = deque([start])
    visited = set()
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(data[node] - visited)  # Add unvisited neighbors
    return visited


def part_one(data: dict) -> int:
    return len(bfs(data, 0))


def part_two(data: dict) -> int:
    visited = set()
    groups = 0

    for node in data:
        if node not in visited:
            group = bfs(data, node)
            visited.update(group)
            groups += 1

    return groups


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 115
    print("Part 2:", part_two(data))  # 221
