#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("05.in", "r") as file:
        return file.read().split("\n\n")


def parse_data(data: list) -> tuple[list, list]:
    """Parse the input data into seeds and mapping rules"""
    seeds = list(map(int, data[0].split(":")[1].split()))
    mappings = []
    for section in data[1:]:
        lines = section.split("\n")[1:]  # Skip the title line
        ranges = []
        for line in lines:
            if line.strip():
                dest, src, length = map(int, line.split())
                ranges.append((dest, src, length))
        mappings.append(ranges)
    return seeds, mappings


def apply_mapping(value: int, mapping: list) -> int:
    """Parse the input into seeds and mapping rules"""
    for dest_start, src_start, length in mapping:
        if src_start <= value < src_start + length:
            offset = value - src_start
            return dest_start + offset
    return value


def split_range(range_start: int, range_end: int, mapping: list) -> list:
    """
    Split a range through a mapping, yielding transformed ranges.
    This is the key function for Part 2!
    """
    # List to hold ranges that still need processing
    pending = [(range_start, range_end)]
    # List to hold transformed ranges
    result = []

    for dest_start, src_start, length in mapping:
        src_end = src_start + length
        next_pending = []

        for start, end in pending:
            # Find overlapping section
            overlap_start = max(start, src_start)
            overlap_end = min(end, src_end)

            if overlap_start < overlap_end:
                # There is an overlap - transform it
                offset = dest_start - src_start
                result.append((overlap_start + offset, overlap_end + offset))

                # Add non-overlapping parts back to pending
                if start < overlap_start:
                    next_pending.append((start, overlap_start))
                if overlap_end < end:
                    next_pending.append((overlap_end, end))
            else:
                # No overlap - keep for next mapping rule
                next_pending.append((start, end))

        pending = next_pending

    # Any remaining ranges pass through unchanged
    result.extend(pending)
    return result


def part_one(data: list) -> int:
    seeds, mappings = parse_data(data)
    min_location = float("inf")
    for seed in seeds:
        value = seed
        for mapping in mappings:
            value = apply_mapping(value, mapping)
        min_location = min(min_location, value)
    return int(min_location)


def part_two(data: list) -> int:
    seeds, mappings = parse_data(data)
    # Convert seed pairs to ranges
    ranges = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        length = seeds[i + 1]
        ranges.append((start, start + length))

    # Apply each mapping to all ranges
    for mapping in mappings:
        new_ranges = []
        for range_start, range_end in ranges:
            new_ranges.extend(split_range(range_start, range_end, mapping))
        ranges = new_ranges

    # Find minimum location (start of smallest range)
    return min(r[0] for r in ranges)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 265018614
    print("Part 2:", part_two(data))  # 63179500
