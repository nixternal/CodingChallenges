#!/usr/bin/env python


def has_adjacent_duplicates(n: int) -> bool:
    """Check if number has any adjacent duplicate digits."""

    s = str(n)
    return any(s[i] == s[i + 1] for i in range(len(s) - 1))


def has_exactly_two_adjacent(n: int) -> bool:
    """Check if number has at least one group of exactly 2 adjacent digits."""

    s = str(n)
    i = 0
    while i < len(s):
        current_digit = s[i]
        count = 1

        # Count consecutive occurrences
        while i + count < len(s) and s[i + count] == current_digit:
            count += 1

        if count == 2:  # Found exactly a pair
            return True

        i += count  # Move to next different digit

    return False


def is_non_decreasing(n: int) -> bool:
    """Check if digits never decrease from left to right."""

    s = str(n)
    return all(s[i] <= s[i + 1] for i in range(len(s) - 1))


def count_valid_passwords(start: int, end: int, *, exact_pairs: bool = False) -> int:
    """
    Count valid passwords in range [start, end].

    Args:
        start: Lower bound (inclusive)
        end: Upper bound (inclusive)
        exact_pairs: If True, require exactly 2 adjacent digits (not more)
    """

    adjacent_check = (
        has_exactly_two_adjacent if exact_pairs else has_adjacent_duplicates
    )

    return sum(
        1 for i in range(start, end + 1) if adjacent_check(i) and is_non_decreasing(i)
    )


def part_one(start: int, end: int) -> int:
    """Part 1: Any adjacent duplicates + non-decreasing."""

    return count_valid_passwords(start, end, exact_pairs=False)


def part_two(start: int, end: int) -> int:

    """Part 2: Exactly two adjacent duplicates + non-decreasing."""
    return count_valid_passwords(start, end, exact_pairs=True)


if __name__ == "__main__":
    START, END = 136760, 595730
    print("Part 1:", part_one(START, END))  # 1873
    print("Part 2:", part_two(START, END))  # 1264
