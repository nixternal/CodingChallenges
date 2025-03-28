#!/usr/bin/env python3

from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


def read_puzzle_input(filepath: str = "07.in") -> List[str]:
    """
    Read the puzzle input from a file.

    Args:
        filepath (str, optional): Path to the input file. Defaults to "07.in".

    Returns:
        List[str]: A list of instruction strings from the input file.
    """
    with open(filepath, "r") as file:
        return file.read().splitlines()


def parse_dependency_graph(data: List[str]
                           ) -> Tuple[Dict[str, Set[str]], Set[str]]:
    """
    Parse input instructions to create a dependency graph.

    Args:
        data (List[str]): List of instruction strings.

    Returns:
        Dict[str, Set[str]]: A dictionary mapping steps to their prerequisite
                             steps.
    """

    dependencies = defaultdict(set)
    all_steps = set()

    for instruction in data:
        # Extract prerequisite and dependent steps
        prereq, step = instruction.split()[1], instruction.split()[7]
        dependencies[step].add(prereq)
        all_steps.update([prereq, step])

    return dict(dependencies), all_steps


def part_one(data: List[str]) -> str:
    """
    Solve Part 1: Determine the order of steps to complete all tasks.

    This function finds the order of steps by processing steps with no
    dependencies first, always choosing the alphabetically first available
    step.

    Args:
        data (List[str]): List of instruction strings defining step
                          dependencies.

    Returns:
        str: A string representing the order of steps to complete all tasks.
    """

    dependencies, all_steps = parse_dependency_graph(data)

    # Find steps with no dependencies
    available_steps = {
        step for step in all_steps
        if step not in dependencies or len(dependencies[step]) == 0
    }

    completed_steps = []

    while available_steps:
        # Always choose the alphabetically first available step
        next_step = min(available_steps)
        completed_steps.append(next_step)
        available_steps.remove(next_step)

        # Find newly available steps
        for step in all_steps:
            if (step not in completed_steps and
                    step not in available_steps and
                    all(dep in completed_steps for
                        dep in dependencies[step])):
                available_steps.add(step)

    return ''.join(completed_steps)


def part_two(data: List[str],
             num_workers: int = 5,
             base_time: int = 60) -> int:
    """
    Solve Part 2: Calculate total time to complete tasks with multiple workers.

    This function simulates parallel task processing with the following
    constraints:
    - Multiple workers can work simultaneously
    - Each step takes time based on its letter (A=1, B=2, etc) plus a base time
    - A step can only start when all its prerequisites are completed

    Args:
        data (List[str]): List of instruction strings defining step
                          dependencies.
        num_workers (int, optional): Number of workers. Defaults to 5.
        base_time (int, optional): Base time for each step. Defaults to 60.

    Returns:
        int: Total time taken to complete all tasks.
    """

    dependencies, all_steps = parse_dependency_graph(data)

    def step_time(step: str) -> int:
        """Calculate the time required to complete a specific step."""
        return base_time + (ord(step) - ord('A') + 1)

    # Track available and completed steps
    available_steps = {
        step for step in all_steps
        if step not in dependencies or len(dependencies[step]) == 0
    }
    completed_steps = set()

    # Worker management
    workers: List[Optional[str]] = [None] * num_workers
    worker_finish_times = [0] * num_workers
    total_time = 0

    while len(completed_steps) < len(all_steps):
        # Process completed steps
        for i in range(num_workers):
            if workers[i] and total_time >= worker_finish_times[i]:
                completed_step = workers[i]
                completed_steps.add(completed_step)
                workers[i] = None

                # Find newly available steps
                for step in all_steps:
                    if (step not in completed_steps and
                            step not in workers and
                            all(dep in completed_steps for
                                dep in dependencies[step])):
                        available_steps.add(step)

        # Assign work to idle workers
        for i in range(num_workers):
            if not workers[i] and available_steps:
                next_step = min(available_steps)
                workers[i] = next_step
                available_steps.remove(next_step)
                worker_finish_times[i] = total_time + step_time(next_step)

        # Advance time
        if any(workers):
            total_time = min(t for t in worker_finish_times if t > total_time)

    return total_time


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # Expected: OVXCKZBDEHINPFSTJLUYRWGAMQ
    print("Part 2:", part_two(data))  # Expected: 955
