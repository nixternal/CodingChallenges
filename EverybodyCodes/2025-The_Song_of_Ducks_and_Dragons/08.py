#!/usr/bin/env python
"""
Solves a puzzle involving chords connecting numbered nails on a circle.
Part 1: Count diametrically opposite connections
Part 2: Count chord intersections using Fenwick tree
Part 3: Find maximum overlapping chord count using 2D difference array
"""


def read_puzzle_input(filename: str = "08.in") -> list[str]:
    """Read and split puzzle input by double newlines."""
    with open(filename, "r") as f:
        return f.read().strip().split("\n\n")


def normalize_chords(numbers: list[int]) -> list[tuple[int, int]]:
    """
    Convert consecutive number pairs to normalized chords (a, b) where a < b.
    Skips pairs where both numbers are equal.
    """
    chords = []
    for a, b in zip(numbers, numbers[1:]):
        if a != b:
            chords.append((min(a, b), max(a, b)))
    return chords


def count_chord_intersections(chords: list[tuple[int, int]], max_nail: int) -> int:
    """
    Count intersections between chords using a sweep line algorithm with Fenwick tree.
    Two chords (a1,b1) and (a2,b2) intersect iff a1 < a2 < b1 < b2.

    Time: O(n log n), Space: O(max_nail)
    """
    if len(chords) <= 1:
        return 0

    chords.sort()

    # Fenwick tree (Binary Indexed Tree) for efficient prefix sums
    tree = [0] * (max_nail + 1)

    def update(idx: int) -> None:
        """Add 1 to position idx in the Fenwick tree."""
        while idx <= max_nail:
            tree[idx] += 1
            idx += idx & -idx

    def query(idx: int) -> int:
        """Get sum of elements from 1 to idx."""
        total = 0
        while idx > 0:
            total += tree[idx]
            idx -= idx & -idx
        return total

    intersections = 0
    i = 0

    # Process chords grouped by left endpoint
    while i < len(chords):
        left_endpoint = chords[i][0]
        batch = []

        # Collect all chords with same left endpoint
        while i < len(chords) and chords[i][0] == left_endpoint:
            a, b = chords[i]
            # Count chords that intersect: those ending between a and b
            intersections += query(b - 1) - query(a)
            batch.append(b)
            i += 1

        # Add all right endpoints from this batch to the tree
        for b in batch:
            update(b)

    return intersections


def part_one(data: list[str]) -> int:
    """Count connections between diametrically opposite nails (distance = N/2)."""
    numbers = list(map(int, data[0].split(",")))
    max_nail = max(numbers)
    half_distance = max_nail // 2

    return sum(abs(a - b) == half_distance for a, b in zip(numbers, numbers[1:]))


def part_two(data: list[str]) -> int:
    """Count total number of chord intersections."""
    numbers = list(map(int, data[1].split(",")))
    chords = normalize_chords(numbers)
    return count_chord_intersections(chords, max(numbers))


def part_three(data: list[str]) -> int:
    """
    Find the maximum number of chords that pass through any single chord.
    Uses a 2D difference array to efficiently count overlaps.
    """
    numbers = list(map(int, data[2].split(",")))
    chords = normalize_chords(numbers)

    if not chords:
        return 0

    N = max(numbers)
    # Use difference array for efficient 2D range updates
    diff = [[0] * (N + 2) for _ in range(N + 2)]

    def add_rectangle(r1: int, c1: int, r2: int, c2: int) -> None:
        """Mark rectangle in difference array."""
        diff[r1][c1] += 1
        diff[r1][c2 + 1] -= 1
        diff[r2 + 1][c1] -= 1
        diff[r2 + 1][c2 + 1] += 1

    # For each chord (a,b), mark all chords (i,j) that would intersect it
    for a, b in chords:
        # The chord itself
        add_rectangle(a, b, a, b)

        # Chords starting inside (a,b) and ending after b
        if a + 1 <= b - 1 and b + 1 <= N:
            add_rectangle(a + 1, b + 1, b - 1, N)

        # Chords starting before a and ending inside (a,b)
        if 1 <= a - 1 and a + 1 <= b - 1:
            add_rectangle(1, a + 1, a - 1, b - 1)

    # Compute prefix sums to get actual counts
    counts = [[0] * (N + 2) for _ in range(N + 2)]
    for i in range(1, N + 1):
        row_sum = 0
        for j in range(1, N + 1):
            row_sum += diff[i][j]
            counts[i][j] = counts[i - 1][j] + row_sum

    # Find maximum count for valid chords (i < j)
    return max(counts[i][j] for i in range(1, N + 1) for j in range(i + 1, N + 1))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 57
    print("Part 2:", part_two(data))  # 2926171
    print("Part 3:", part_three(data))  # 2797
