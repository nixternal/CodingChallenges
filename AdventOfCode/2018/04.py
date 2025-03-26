#!/usr/bin/env python3

from typing import List, Dict, Tuple
import re
from collections import defaultdict


def read_puzzle_input(filename: str = "04.in") -> List[str]:
    """
    Read and sort the input file containing guard shift records.

    This function reads the input file and returns a sorted list of records,
    ensuring the guard records are in chronological order for proper analysis.

    Args:
        filename (str, optional): Path to the input file. Defaults to "04.in".

    Returns:
        List[str]: Sorted list of guard shift records.
    """

    with open(filename, "r") as file:
        return sorted(file.readlines())


def parse_guard_records(
        data: List[str]) -> Tuple[Dict[int, int], Dict[int, List[int]]]:
    """
    Parse and analyze guard sleep records.

    This function processes the input records to track:
    1. Total sleep time for each guard
    2. Minute-by-minute sleep frequency for each guard

    Args:
        data (List[str]): Sorted list of guard shift records.

    Returns:
        Tuple containing:
        - sleep_tracker: Dict mapping guard IDs to total sleep time
        - minute_tracker: Dict mapping guard IDs to sleep frequency per minute
    """

    sleep_tracker: Dict[int, int] = defaultdict(int)
    minute_tracker: Dict[int, List[int]] = defaultdict(lambda: [0] * 60)

    current_guard_id: int | None = None
    sleep_start: int | None = None

    for record in data:
        # Regex to parse timestamp and action
        match = re.match(
            r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)",
            record.strip()
        )

        if not match:
            continue

        _, _, _, _, minute, action = match.groups()
        minute = int(minute)

        # Identify guard or track sleep periods
        if "Guard" in action:
            match_guard = re.search(r"#(\d+)", action)
            if match_guard:
                current_guard_id = int(match_guard.group(1))
        elif "falls asleep" in action:
            sleep_start = minute
        elif ("wakes up" in action and
                current_guard_id is not None and
                sleep_start is not None):
            # Track sleep time and minute-by-minute sleep frequency
            for m in range(sleep_start, minute):
                minute_tracker[current_guard_id][m] += 1
            sleep_tracker[current_guard_id] += minute - sleep_start

    return sleep_tracker, minute_tracker


def part_one(data: List[str]) -> int:
    """
    Solve Part 1 of the Guard Sleep Analysis puzzle.

    Strategy: Find the guard who sleeps the most and their most frequently
              slept minute.

    Args:
        data (List[str]): Sorted list of guard shift records.

    Returns:
        int: Product of the sleepiest guard's ID and their most slept minute.
    """

    sleep_tracker, minute_tracker = parse_guard_records(data)

    # Find the guard who slept the most total time
    def get_sleep_time(guard_id: int) -> int:
        return sleep_tracker.get(guard_id, 0)

    sleepiest_guard = max(sleep_tracker, key=get_sleep_time)

    # The following lambda version is the same as the previous 3 lines
    # sleepiest_guard = max(
    #     sleep_tracker,
    #     key=lambda guard: sleep_tracker.get(guard, 0)
    # )

    # Find the minute this guard slept most frequently
    most_sleep_minute = minute_tracker[sleepiest_guard].index(
        max(minute_tracker[sleepiest_guard])
    )

    return sleepiest_guard * most_sleep_minute


def part_two(data: List[str]) -> int:
    """
    Solve Part 2 of the Guard Sleep Analysis puzzle.

    Strategy: Find the guard with the highest frequency of sleeping
    at a specific minute across all nights.

    Args:
        data (List[str]): Sorted list of guard shift records.

    Returns:
        int: Product of the guard ID and the minute they most frequently sleep.
    """

    _, minute_tracker = parse_guard_records(data)

    # Find the guard and minute with the highest sleep frequency
    max_guard: int | None = None
    max_minute: int | None = None
    max_count: int = 0

    for guard, minutes in minute_tracker.items():
        for minute, count in enumerate(minutes):
            if count > max_count:
                max_guard = guard
                max_minute = minute
                max_count = count

    return (
        max_guard * max_minute
        if max_guard is not None and max_minute is not None
        else 0
    )


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 8950
    print("Part 2:", part_two(data))  # 78452
