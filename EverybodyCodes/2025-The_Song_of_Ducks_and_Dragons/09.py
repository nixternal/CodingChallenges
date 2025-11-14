#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("09.in", "r") as file:
        return file.read().split("\n\n")


def parse_sequences(section: str) -> list[str]:
    """Parse sequences from a section, stripping the label."""
    return [line.split(":", 1)[1] for line in section.splitlines()]


def is_valid_child(parent1: str, parent2: str, child: str) -> bool:
    """Check if child could be offspring of parent1 and parent2."""
    return all(a == c or b == c for a, b, c in zip(parent1, parent2, child))


def calculate_similarity_product(parent1: str, parent2: str, child: str) -> int:
    """Calculate the product of similarities between parents and child."""
    sim_p1 = sum(p == c for p, c in zip(parent1, child))
    sim_p2 = sum(p == c for p, c in zip(parent2, child))
    return sim_p1 * sim_p2


def part_one(data: list) -> int:
    sequences = parse_sequences(data[0])
    parent1, parent2, child = sequences
    return calculate_similarity_product(parent1, parent2, child)


def part_two(data: list) -> int:
    sequences = parse_sequences(data[1])
    n = len(sequences)
    total = 0

    # Pre-compute all valid parent-child combinations
    for p1 in range(n):
        for p2 in range(p1 + 1, n):
            parent1, parent2 = sequences[p1], sequences[p2]

            # Check all potential children
            for c in range(n):
                if c == p1 or c == p2:
                    continue

                child = sequences[c]
                if is_valid_child(parent1, parent2, child):
                    total += calculate_similarity_product(parent1, parent2, child)

    return total


def part_three(data: list) -> int:
    sequences = parse_sequences(data[2])
    n = len(sequences)

    # Build adjacency list (1-indexed to match original logic)
    # Use sets for O(1) lookups and automatic deduplication
    connections = [set() for _ in range(n + 1)]

    # Pre-compute valid relationships
    for p1 in range(n):
        parent1 = sequences[p1]
        for p2 in range(p1 + 1, n):
            parent2 = sequences[p2]

            # Find all valid children for this parent pair
            for c in range(n):
                if c == p1 or c == p2:
                    continue

                child = sequences[c]
                if is_valid_child(parent1, parent2, child):
                    # Convert to 1-indexed
                    p1_idx, p2_idx, c_idx = p1 + 1, p2 + 1, c + 1

                    # Add bidirectional connections
                    connections[p1_idx].add(c_idx)
                    connections[p2_idx].add(c_idx)
                    connections[c_idx].add(p1_idx)
                    connections[c_idx].add(p2_idx)

    # Find largest connected component using BFS
    visited = [False] * (n + 1)
    largest_component = []

    for start in range(1, n + 1):
        if visited[start]:
            continue

        # BFS to find connected component
        component = []
        queue = [start]
        visited[start] = True

        while queue:
            node = queue.pop(0)
            component.append(node)

            for neighbor in connections[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

        if len(component) > len(largest_component):
            largest_component = component

    return sum(largest_component)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 6630
    print("Part 2:", part_two(data))  # 315244
    print("Part 3:", part_three(data))  # 46303
