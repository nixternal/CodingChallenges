#!/usr/bin/env python

from bisect import bisect_left, bisect_right
from collections import defaultdict


def read_puzzle_input() -> list:
    """
    Read puzzle input from file.

    Returns:
        list: List of input sections separated by blank lines
    """
    with open("06.in", "r") as file:
        return file.read().split("\n\n")


def count_mentors(notes: str, profession: str) -> int:
    """
    Count mentor-novice pairs using simple left-to-right assignment.

    For each novice (lowercase), count how many mentors (uppercase) of the same
    letter have appeared to their left in the sequence.

    Args:
        notes: String containing mentor (uppercase) and novice (lowercase) letters
        profession: Single letter profession to analyze (e.g., 'A', 'B', 'C')

    Returns:
        int: Total number of possible mentor-novice pairs

    Example:
        >>> count_mentors("AABCBABCa", "A")
        2  # The 'a' has 2 'A' mentors to its left
    """
    mentor = profession.upper()
    novice = profession.lower()
    mentors_seen = 0
    counts = []

    for ch in notes:
        if ch == mentor:
            mentors_seen += 1
        elif ch == novice:
            counts.append(mentors_seen)

    return sum(counts)


def count_mentor_pairs(pattern: str, repeats: int, max_distance: int) -> int:
    """
    Count mentor-novice pairs with distance constraints (OPTIMIZED).

    A novice can be paired with a mentor if:
    1. They share the same letter (lowercase novice with uppercase mentor)
    2. The mentor is within max_distance positions (left or right)
    3. They are not at the same position

    The algorithm uses binary search for O(n log n) complexity instead of O(n*m).

    Args:
        pattern: Base tent arrangement pattern
        repeats: Number of times to repeat the pattern
        max_distance: Maximum distance between novice and mentor positions

    Returns:
        int: Total number of valid mentor-novice pairs

    Algorithm:
        1. Repeat the pattern to create full arrangement
        2. Group mentor positions by letter (for faster lookup)
        3. For each novice, use binary search to find matching mentors in range
        4. Sum all valid pairs

    Time Complexity: O(n log n) where n is the length of full arrangement
    Space Complexity: O(n) for storing positions

    Example:
        >>> pattern = "AABCBABCABCabcabcABCCBAACBCa"
        >>> count_mentor_pairs(pattern, 1, 10)
        34
    """
    # Create the full tent arrangement by repeating the pattern
    full_arrangement = pattern * repeats

    # Group mentor positions by letter for O(log n) lookup
    # Key: uppercase letter, Value: sorted list of positions
    mentors_by_letter = defaultdict(list)
    novice_positions = []

    # Parse the arrangement and categorize positions
    for i, char in enumerate(full_arrangement):
        if char.isupper():
            mentors_by_letter[char].append(i)
        elif char.islower():
            novice_positions.append((i, char))

    total_pairs = 0

    # For each novice, use binary search to find mentors in range
    for novice_pos, novice_char in novice_positions:
        matching_mentor_char = novice_char.upper()
        mentor_list = mentors_by_letter[matching_mentor_char]

        if not mentor_list:
            continue

        # Define the search range: [novice_pos - max_distance, novice_pos + max_distance]
        left_bound = novice_pos - max_distance
        right_bound = novice_pos + max_distance

        # Use binary search to find the range of valid mentors
        # bisect_left: leftmost position >= left_bound
        # bisect_right: rightmost position <= right_bound
        left_idx = bisect_left(mentor_list, left_bound)
        right_idx = bisect_right(mentor_list, right_bound)

        # Count mentors in range
        count = right_idx - left_idx

        # Edge case: Check if novice position itself is in the mentor list
        # (shouldn't happen with valid input, but handle defensively)
        if left_idx < right_idx:
            check_idx = bisect_left(mentor_list, novice_pos, left_idx, right_idx)
            if check_idx < right_idx and mentor_list[check_idx] == novice_pos:
                count -= 1

        total_pairs += count

    return total_pairs


def part_one(data: list) -> int:
    """
    Solve Part 1: Simple mentor counting for profession 'A'.

    Args:
        data: Puzzle input sections

    Returns:
        int: Answer for part 1
    """
    return count_mentors(data[0].strip(), "A")


def part_two(data: list) -> int:
    """
    Solve Part 2: Sum of mentor counting for professions 'A', 'B', and 'C'.

    Args:
        data: Puzzle input sections

    Returns:
        int: Answer for part 2
    """
    notes = data[1].strip()
    return (
        count_mentors(notes, "A")
        + count_mentors(notes, "B")
        + count_mentors(notes, "C")
    )


def part_three(data: list) -> int:
    """
    Solve Part 3: Distance-constrained pairing with pattern repetition.

    The pattern is repeated 1000 times, and mentors can be up to 1000
    positions away from their novices.

    Args:
        data: Puzzle input sections

    Returns:
        int: Answer for part 3
    """
    notes = data[2].strip()
    return count_mentor_pairs(notes, 1000, 1000)


if __name__ == "__main__":
    data = read_puzzle_input()

    print("Part 1:", part_one(data))  # 166
    print("Part 2:", part_two(data))  # 3382
    print("Part 3:", part_three(data))  # 1663986556
