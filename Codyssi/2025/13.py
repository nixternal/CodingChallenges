#!/usr/bin/env python
"""
Graph Algorithm Challenge Solution

This program solves a multi-part graph traversal challenge:
1. Find the product of the 3 longest BFS path lengths from a start node
2. Find the product of the 3 highest weighted Dijkstra path values from a
   start node
3. Find the longest cycle in the graph

Input Format:
- Each line represents a directed edge: "StartNode -> EndNode | Weight"
- The graph is stored in "13.in"

Example input line:
ABC -> XYZ | 42

Parts challenge:
- Part 1: Uses BFS to find unweighted shortest paths and computes product of
          top 3 longest path lengths
- Part 2: Uses Dijkstra to find weighted shortest paths and computes product
          of top 3 highest path values
- Part 3: Finds the longest cycle in the graph using DFS
"""

from collections import defaultdict, deque
import heapq
import math
from typing import Dict, DefaultDict, Tuple, Set, List


def read_puzzle_input() -> DefaultDict[str, List[Tuple[str, int]]]:
    """
    Read and parse the puzzle input file into a graph representation.

    Returns:
        A directed graph as an adjacency list using defaultdict where:
        - Keys are node names (strings)
        - Values are lists of (neighbor, weight) tuples
    """

    graph = defaultdict(list)
    with open("13.in", "r") as file:
        for line in file.readlines():
            parts = line.strip().split(' -> ')
            if len(parts) != 2:
                continue  # Skip malformed lines

            start = parts[0].strip()
            end_parts = parts[1].split(' | ')
            if len(end_parts) != 2:
                continue  # Skip malformed lines

            end, weight_str = end_parts
            try:
                weight = int(weight_str.strip())
                graph[start].append((end.strip(), weight))
            except ValueError:
                # Skip lines with non-integer weights
                continue

    return graph


def bfs_shortest_paths(graph: DefaultDict[str, List[Tuple[str, int]]],
                       start: str
                       ) -> Dict[str, int]:
    """
    Performs Breadth-First Search to find unweighted shortest paths from the
    start node.

    Args:
        graph: The directed graph as an adjacency list
        start: The starting node

    Returns:
        Dictionary mapping each reachable node to its shortest distance from
        start
    """

    queue = deque([(start, 0)])  # (node, distance)
    shortest_paths = {start: 0}

    while queue:
        node, dist = queue.popleft()

        # Process all neighbors
        for neighbor, _ in graph.get(node, []):
            if neighbor not in shortest_paths:
                shortest_paths[neighbor] = dist + 1
                queue.append((neighbor, dist + 1))

    return shortest_paths


def dijkstra_shortest_path(graph: DefaultDict[str, List[Tuple[str, int]]],
                           start: str
                           ) -> Dict[str, int]:
    """
    Performs Dijkstra's algorithm to find weighted shortest paths from the
    start node.

    Args:
        graph: The directed graph as an adjacency list with edge weights
        start: The starting node

    Returns:
        Dictionary mapping each reachable node to its minimum weighted
        distance from start
    """

    # Priority queue stores (distance, node) tuples
    min_heap = [(0, start)]
    shortest_paths = {}

    while min_heap:
        dist, node = heapq.heappop(min_heap)

        # Skip if we've already found a shorter path to this node
        if node in shortest_paths:
            continue

        shortest_paths[node] = dist

        # Process all neighbors
        for neighbor, weight in graph.get(node, []):
            if neighbor not in shortest_paths:
                heapq.heappush(min_heap, (dist + weight, neighbor))

    return shortest_paths


def compute_product_of_top3(paths: Dict[str, int]) -> int:
    """
    Computes the product of the 3 highest values in the paths dictionary.

    Args:
        paths: Dictionary mapping nodes to path lengths/values

    Returns:
        Product of the top 3 values, or 0 if fewer than 3 values exist
    """

    if len(paths) < 3:
        return 0

    # Get the 3 highest values without sorting the entire dictionary
    top3 = heapq.nlargest(3, paths.values())
    return math.prod(top3)


def find_longest_cycle(graph: DefaultDict[str, List[Tuple[str, int]]]) -> int:
    """
    Finds the longest cycle in the graph using depth-first search.

    A cycle is a path that starts and ends at the same node.
    The length of a cycle is the sum of weights of all edges in the cycle.

    Args:
        graph: The directed graph as an adjacency list with edge weights

    Returns:
        Length of the longest cycle, or 0 if no cycles exist
    """

    # Cache to store results of previously computed paths
    memo = {}

    def dfs(current: str,
            target: str,
            visited: Set[str],
            path_length: int
            ) -> int:
        """
        Helper function that performs DFS to find cycles.

        Args:
            current: Current node being visited
            target: Target node (where the cycle should end)
            visited: Set of already visited nodes
            path_length: Current accumulated path length

        Returns:
            Length of the longest cycle found, or 0 if no cycle exists
        """

        # Cache key combines current state
        cache_key = (current, tuple(sorted(visited)))
        if cache_key in memo:
            return memo[cache_key]

        # If we've reached the target again, we've found a cycle
        if current in visited:
            return path_length if current == target else 0

        visited.add(current)
        max_length = 0

        # Explore all neighbors
        for neighbor, weight in graph.get(current, []):
            # Create a new visited set for each branch to allow for multiple
            # visits on different paths
            new_visited = visited.copy()
            cycle_length = dfs(
                neighbor,
                target,
                new_visited,
                path_length + weight
            )
            max_length = max(max_length, cycle_length)

        # Cache and return the result
        memo[cache_key] = max_length
        return max_length

    # Try starting from each node to find the longest cycle
    longest_cycle = 0
    for node in graph:
        cycle_length = dfs(node, node, set(), 0)
        longest_cycle = max(longest_cycle, cycle_length)

    return longest_cycle


def part_one(data: DefaultDict[str, List[Tuple[str, int]]]) -> int:
    """
    Find the product of the 3 longest unweighted BFS path lengths.

    Args:
        data: The graph data

    Returns:
        Product of the 3 longest path lengths
    """

    shortest_paths = bfs_shortest_paths(data, "STT")
    return compute_product_of_top3(shortest_paths)


def part_two(data: DefaultDict[str, List[Tuple[str, int]]]) -> int:
    """
    Find the product of the 3 highest weighted Dijkstra path values.

    Args:
        data: The graph data

    Returns:
        Product of the 3 highest path values
    """

    shortest_paths = dijkstra_shortest_path(data, "STT")
    return compute_product_of_top3(shortest_paths)


def part_three(data: DefaultDict[str, List[Tuple[str, int]]]) -> int:
    """
    Find the length of the longest cycle in the graph.

    Args:
        data: The graph data

    Returns:
        Length of the longest cycle
    """

    return find_longest_cycle(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 17550
    print("Part 2:", part_two(data))    # 19722836
    print("Part 3:", part_three(data))  # 347
