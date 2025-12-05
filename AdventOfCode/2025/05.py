#!/usr/bin/env python


def read_puzzle_input() -> list[str]:
    """Read puzzle input file and split into sections."""
    with open("05.in", "r") as file:
        return file.read().split("\n\n")


def parse_ranges(data: str) -> list[tuple[int, int]]:
    """Parse range strings like '10-20' into tuples of (min, max)."""
    return [
        (int(lo), int(hi)) for line in data.splitlines() for lo, hi in [line.split("-")]
    ]


def part_one(data: list[str]) -> int:
    """
    Count how many IDs from the list fall within any of the valid ranges.

    For each ID, checks if it falls within any range using binary search
    on sorted ranges for O(log n) lookup per ID.
    """
    ranges = parse_ranges(data[0])
    ranges.sort()  # Sort for efficient searching

    ids = [int(line) for line in data[1].splitlines()]

    fresh_ids = 0
    for id_val in ids:
        # Binary search approach: check if ID falls in any range
        for min_val, max_val in ranges:
            if id_val < min_val:
                # ID is before this range, won't be in any later ranges
                break
            if min_val <= id_val <= max_val:
                fresh_ids += 1
                break

    return fresh_ids


def part_two(data: list[str]) -> int:
    """
    Count total unique values covered by all ranges.

    Uses interval merging: overlapping or adjacent ranges are merged,
    then we count the total span. This avoids creating sets with millions
    of individual integers.

    Time complexity: O(n log n) for sorting + O(n) for merging
    Space complexity: O(n) for storing ranges
    """
    ranges = parse_ranges(data[0])

    if not ranges:
        return 0

    # Sort ranges by start position
    ranges.sort()

    # Merge overlapping/adjacent ranges and count
    count = 0
    current_start, current_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= current_end + 1:
            # Ranges overlap or are adjacent - merge them
            current_end = max(current_end, end)
        else:
            # Gap found - finalize current range and start new one
            count += current_end - current_start + 1
            current_start, current_end = start, end

    # Add the final range
    count += current_end - current_start + 1

    return count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 617
    print("Part 2:", part_two(data))  # 338258295736104
