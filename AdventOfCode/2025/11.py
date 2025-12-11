#!/usr/bin/env python

from typing import Optional


def read_puzzle_input() -> list:
    with open("11.in", "r") as file:
        return file.read().splitlines()


def parse_graph(data: list) -> dict[str, list[str]]:
    """Parse input into adjacency list representation of directed graph."""
    graph = {}
    for line in data:
        parts = line.split(":")
        device = parts[0].strip()
        outputs = [name.strip() for name in parts[1].split()] if len(parts) > 1 else []
        graph[device] = outputs
    return graph


def count_paths(
    graph: dict[str, list[str]],
    start: str,
    end: str,
    memo: Optional[dict[tuple[str, str], int]] = None,
) -> int:
    """Count all paths from start node to end node using memoization."""
    if memo is None:
        memo = {}

    if start == end:
        return 1

    if start not in graph:
        return 0

    cache_key = (start, end)
    if cache_key in memo:
        return memo[cache_key]

    total = sum(count_paths(graph, neighbor, end, memo) for neighbor in graph[start])
    memo[cache_key] = total
    return total


def part_one(data: list) -> int:
    """Count all paths from 'you' to 'out'."""
    graph = parse_graph(data)
    return count_paths(graph, "you", "out")


def part_two(data: list) -> int:
    """
    Count paths from 'svr' to 'out' that pass through both 'dac' and 'fft'.

    Uses multiplication principle: if all paths must go through both nodes,
    then total paths = (paths svr→dac) × (paths dac→fft) × (paths fft→out)
                     + (paths svr→fft) × (paths fft→dac) × (paths dac→out)
    """
    graph = parse_graph(data)
    memo = {}

    # Scenario 1: svr → dac → fft → out
    scenario_1 = (
        count_paths(graph, "svr", "dac", memo)
        * count_paths(graph, "dac", "fft", memo)
        * count_paths(graph, "fft", "out", memo)
    )

    # Scenario 2: svr → fft → dac → out
    scenario_2 = (
        count_paths(graph, "svr", "fft", memo)
        * count_paths(graph, "fft", "dac", memo)
        * count_paths(graph, "dac", "out", memo)
    )

    return scenario_1 + scenario_2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 466
    print("Part 2:", part_two(data))  # 549705036748518
