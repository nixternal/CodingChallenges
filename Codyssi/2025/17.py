#!/usr/bin/env python
"""
Staircase Path Solver

This program solves a path-finding problem on interconnected staircases.
It calculates:
1. The number of possible paths from start to end without using branches
2. The number of possible paths from start to end using all available branches
3. The specific path that has a given rank among all possible paths

Each staircase has a specific number of steps. At certain steps, there may be
branches that connect to other staircases. The movement is restricted to a
predefined set of step sizes.
"""

from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple, DefaultDict


def read_input() -> str:
    """Read and return the puzzle input from the specified file."""

    with open("17.in", "r") as file:
        return file.read().strip()


def find_reachable_positions(
    current_pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    steps_remaining: int,
    branch_connections: DefaultDict[int, DefaultDict[int, List[int]]],
    steps_in_staircase: Dict[int, int],
    reachable_positions_set: Set[Tuple[int, int]]
) -> None:
    """
    Find all positions reachable from current_pos using exactly
    steps_remaining steps.

    Args:
        current_pos: Starting position tuple (staircase_id, step_number)
        target_pos: Final target position
        steps_remaining: Exact number of steps that must be used
        branch_connections: Dictionary mapping staircase positions to
                            possible branches
        steps_in_staircase: Dictionary mapping staircase IDs to their total
                            steps
        reachable_positions_set: Set to store discovered reachable positions
    """

    # Base case: used all steps
    if steps_remaining == 0:
        reachable_positions_set.add(current_pos)
        return

    # Don't overshoot target
    if current_pos == target_pos:
        return

    staircase_id, step_number = current_pos

    # Option 1: Take a branch if available at current step
    if step_number in branch_connections[staircase_id]:
        for destination_staircase in \
                branch_connections[staircase_id][step_number]:
            find_reachable_positions(
                (destination_staircase, step_number),
                target_pos,
                steps_remaining - 1,  # Taking a branch uses one step
                branch_connections,
                steps_in_staircase,
                reachable_positions_set
            )

    # Option 2: Move up current staircase if not at top
    if step_number < steps_in_staircase[staircase_id]:
        find_reachable_positions(
            (staircase_id, step_number + 1),
            target_pos,
            steps_remaining - 1,
            branch_connections,
            steps_in_staircase,
            reachable_positions_set
        )


def count_path_combinations(
    current_pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    allowed_step_sizes: List[int],
    branch_connections: DefaultDict[int, DefaultDict[int, List[int]]],
    steps_in_staircase: Dict[int, int],
    memoization_cache: Dict[Tuple[int, int], int]
) -> int:
    """Count all possible ways to reach target_pos from current_pos.

    Uses dynamic programming (memoization) to avoid recalculating paths.

    Args:
        current_pos: Starting position tuple (staircase_id, step_number)
        target_pos: Final target position
        allowed_step_sizes: List of valid step sizes that can be used
        branch_connections: Dictionary mapping staircase positions to possible
                            branches
        steps_in_staircase: Dictionary mapping staircase IDs to their total
                            steps
        memoization_cache: Dictionary to store already computed results

    Returns:
        The total number of distinct paths from current_pos to target_pos
    """

    # Base case: already at target
    if current_pos == target_pos:
        return 1

    # Check memoization cache
    if current_pos in memoization_cache:
        return memoization_cache[current_pos]

    total_paths = 0
    reachable_positions = set()

    # For each allowed step size, find positions we can reach
    for step_size in allowed_step_sizes:
        find_reachable_positions(
            current_pos,
            target_pos,
            step_size,
            branch_connections,
            steps_in_staircase,
            reachable_positions
        )

    # Recursively count paths from each reachable position
    for next_pos in reachable_positions:
        total_paths += count_path_combinations(
            next_pos,
            target_pos,
            allowed_step_sizes,
            branch_connections,
            steps_in_staircase,
            memoization_cache
        )

    # Store result in cache
    memoization_cache[current_pos] = total_paths
    return total_paths


def parse_puzzle_data(
    data: str
) -> Tuple[
        DefaultDict[int, DefaultDict[int, List[int]]],
        Tuple[int, int], Tuple[int, int], List[int], Dict[int, int]]:
    """Parse the input data into data structures needed for solving the puzzle.

    Args:
        data: Raw input string

    Returns:
        A tuple containing:
        - branch_connections: Dictionary of branch connections between
                              staircases
        - start_position: The starting position
        - end_position: The target position
        - allowed_step_sizes: List of allowed movement step sizes
        - steps_in_staircase: Dictionary mapping staircase IDs to their total
                              steps
    """

    staircase_info, moves_info = data.split("\n\n")

    # Parse staircase info
    staircase_lines = staircase_info.strip().split("\n")
    steps_in_staircase = {}
    branch_connections = defaultdict(lambda: defaultdict(list))

    for line in staircase_lines:
        parts = line.split()
        staircase_id = int(parts[0][1:])  # Remove 'S' prefix
        connection_step = int(parts[2])
        total_steps = int(parts[4])

        if parts[7] == 'START':
            # This is the starting staircase
            steps_in_staircase[1] = total_steps
        else:
            # This is a branch connection
            source_staircase = int(parts[7][1:])
            destination_staircase = int(parts[9][1:])

            # Add bidirectional branch connections
            branch_connections[source_staircase][connection_step].append(
                                                                  staircase_id)
            branch_connections[staircase_id][total_steps].append(
                                                         destination_staircase)

            # Record total steps for this staircase
            steps_in_staircase[staircase_id] = total_steps

    # Parse allowed move sizes
    _, moves_values = moves_info.split(": ")
    allowed_step_sizes = [int(move) for move in moves_values.split(", ")]

    # Define start and end positions
    start_position = (1, 0)  # Always start at first step of staircase 1
    end_position = (1, steps_in_staircase[1])  # End is the top of staircase 1

    return (branch_connections, start_position, end_position,
            allowed_step_sizes, steps_in_staircase)


def part_one(data: str) -> int:
    """Solve part 1: Count paths without using branch connections.

    Returns:
        Number of possible paths without branches
    """

    (_, start_pos, end_pos,
        allowed_moves, steps_in_staircase) = parse_puzzle_data(data)
    # Use empty branch connections (no branches allowed)
    empty_branches = defaultdict(lambda: defaultdict(list))
    return count_path_combinations(
        start_pos,
        end_pos,
        allowed_moves,
        empty_branches,
        steps_in_staircase,
        {}
    )


def part_two(
    data: str,
    memoization_cache: Optional[Dict[Tuple[int, int], int]] = None
) -> int:
    """Solve part 2: Count paths using all branch connections.

    Args:
        puzzle_data: The raw puzzle input
        memoization_cache: Optional cache to reuse calculations

    Returns:
        Number of possible paths using branches
    """
    if memoization_cache is None:
        memoization_cache = {}

    (branch_connections, start_pos, end_pos,
        allowed_moves, steps_in_staircase) = parse_puzzle_data(data)
    return count_path_combinations(
        start_pos,
        end_pos,
        allowed_moves,
        branch_connections,
        steps_in_staircase,
        memoization_cache
    )


def part_three(
    data: str,
    target_rank: int,
    memoization_cache: Optional[Dict[Tuple[int, int], int]] = None
) -> str:
    """Solve part 3: Find the specific path with the given rank.

    Args:
        puzzle_data: The raw puzzle input
        target_rank: The desired rank of the path to find
        memoization_cache: Optional cache to reuse calculations

    Returns:
        String representation of the path with the target rank
    """
    if memoization_cache is None:
        memoization_cache = {}

    (branch_connections, start_pos, end_pos,
        allowed_moves, steps_in_staircase) = parse_puzzle_data(data)

    current_rank = 1
    current_pos = start_pos
    path_representation = []

    # Keep moving until we reach the end position
    while current_pos != end_pos:
        staircase_id, step_number = current_pos
        path_representation.append(f"S{staircase_id}_{step_number}")

        # Find all positions reachable in one move
        reachable_positions = set()
        for step_size in allowed_moves:
            find_reachable_positions(
                current_pos,
                end_pos,
                step_size,
                branch_connections,
                steps_in_staircase,
                reachable_positions
            )

        # Calculate paths from each reachable position
        position_rankings = []
        for next_pos in reachable_positions:
            paths_from_position = count_path_combinations(
                next_pos,
                end_pos,
                allowed_moves,
                branch_connections,
                steps_in_staircase,
                memoization_cache
            )
            position_rankings.append((next_pos, paths_from_position))

        # Sort positions by their natural order (not by path count)
        position_rankings.sort()

        # Find which position gets us to the target rank
        cumulative_rank = current_rank
        position_index = 0

        # Skip positions that have too few paths
        while (position_index < len(position_rankings) - 1 and
               cumulative_rank + position_rankings[position_index][1]
               <= target_rank):
            cumulative_rank += position_rankings[position_index][1]
            position_index += 1

        # Move to the selected position
        current_pos = position_rankings[position_index][0]
        current_rank = cumulative_rank

    # Add final position
    staircase_id, step_number = current_pos
    path_representation.append(f"S{staircase_id}_{step_number}")

    # Format result as a hyphen-separated path
    return "-".join(path_representation)


if __name__ == "__main__":
    puzzle_data = read_input()

    # Shared memoization cache for parts 2 and 3
    path_cache = {}

    # P1 Answer: 87539891925831589854091029
    print("Part 1:", part_one(puzzle_data))

    # P2 Answer: 82671145639165026772735141020945
    print("Part 2:", part_two(puzzle_data, path_cache))

    # P3 Answer:
    # S1_0-S1_1-S1_2-S1_3-S1_4-S1_5-S1_6-S1_7-S1_8-S1_10-S1_12-S1_13-S1_14-
    # S1_15-S1_17-S1_18-S1_19-S1_22-S1_24-S1_25-S1_28-S5_30-S5_32-S5_33-
    # S5_34-S5_36-S21_36-S21_39-S21_42-S27_42-S27_43-S27_44-S27_45-S27_46-
    # S27_47-S27_48-S27_49-S11_54-S11_55-S12_57-S4_59-S4_61-S89_62-S89_65-
    # S89_68-S89_71-S89_73-S89_74-S89_75-S89_76-S89_78-S89_79-S89_80-S129_82-
    # S7_84-S8_86-S57_88-S86_89-S86_91-S31_91-S31_92-S31_94-S1_94-S1_95-S1_96
    print("Part 3:", part_three(
        puzzle_data,
        100000000000000000000000000000,
        path_cache
        )
    )
