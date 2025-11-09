#!/usr/bin/env python
"""
Advent of Code 2018 - Day 20: A Regular Map

This solution solves a maze navigation problem where the input is a regex-like
string describing a complex network of rooms connected by doors. The regex uses:
- N, S, E, W: Move one room in that direction (creating a door)
- (ABC|DEF): Branch - choose either path ABC or DEF
- Nested branches: ((A|B)C|D) are supported

The goal is to find:
1. The furthest room from the starting position (0,0)
2. How many rooms require passing through at least 1000 doors to reach

Time Complexity: O(n) where n is the regex length + O(v) for BFS where v is rooms
Space Complexity: O(v) for the graph and distance map
"""

from collections import defaultdict, deque


def read_puzzle_input() -> list[str]:
    """
    Read the puzzle input file containing a single line regex.

    Returns:
        List containing the regex string(s)
    """
    with open("20.in", "r") as file:
        return file.read().splitlines()


def build_door_graph(regex: str) -> dict[tuple[int, int], set[tuple[int, int]]]:
    """
    Parse a regex-like maze description and construct a bidirectional graph.

    The regex describes paths through a 2D grid of rooms. This function interprets
    the regex by simulating all possible paths and recording which rooms are
    connected by doors.

    Algorithm:
    - Maintain a set of "current positions" representing all rooms we could
      currently be in after following the regex so far
    - For each direction character (N/S/E/W), move all current positions in
      that direction, creating bidirectional door connections
    - For branches '(', '|', ')':
      * '(' pushes current state onto a stack
      * '|' saves current endpoints and resets to the branch start
      * ')' combines all branch endpoints as the new current positions

    Example: "^N(E|W)S$"
    - Start at (0,0)
    - N: move to (0,-1), door between (0,0) and (0,-1)
    - (: save (0,-1) on stack
    - E: branch 1 ends at (1,-1)
    - |: save (1,-1), reset to (0,-1)
    - W: branch 2 ends at (-1,-1)
    - ): current positions = {(1,-1), (-1,-1)}
    - S: both positions move south, creating two more doors

    Args:
        regex: The regex string (with or without ^ and $ markers)

    Returns:
        A dictionary mapping each room coordinate to a set of adjacent rooms.
        Doors are bidirectional, so if A->B exists, B->A also exists.
    """
    # Remove start/end markers if present
    regex = regex.strip("^$")

    # Direction mappings: N=north (y-1), S=south (y+1), E=east (x+1), W=west (x-1)
    DIRECTIONS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

    # Graph of bidirectional doors between rooms
    doors = defaultdict(set)

    # Stack for handling nested branches
    # Each entry: (start_positions, accumulated_end_positions)
    # - start_positions: where we were when we entered this branch group
    # - accumulated_end_positions: all positions we've reached from any branch
    stack = []

    # Set of current positions we're tracking (all possible locations)
    current_positions = {(0, 0)}

    for char in regex:
        if char in DIRECTIONS:
            # Move all current positions in the specified direction
            dx, dy = DIRECTIONS[char]
            new_positions = set()

            for x, y in current_positions:
                # Calculate new position
                new_pos = (x + dx, y + dy)

                # Create bidirectional door between current and new position
                doors[(x, y)].add(new_pos)
                doors[new_pos].add((x, y))

                new_positions.add(new_pos)

            current_positions = new_positions

        elif char == "(":
            # Start of a branch group - save current state
            # The set() calls create copies so we don't modify saved state
            stack.append((set(current_positions), set()))

        elif char == "|":
            # Branch separator - save current branch endpoints and reset
            start_positions, end_positions = stack[-1]

            # Add current positions to accumulated endpoints
            end_positions.update(current_positions)

            # Reset to branch start for next alternative
            current_positions = set(start_positions)

            # Update stack with accumulated endpoints
            stack[-1] = (start_positions, end_positions)

        elif char == ")":
            # End of branch group - combine all branch results
            start_positions, end_positions = stack.pop()

            # Add final branch endpoints
            end_positions.update(current_positions)

            # All branch endpoints become our current positions
            current_positions = end_positions

    return doors


def compute_shortest_distances(
    doors: dict[tuple[int, int], set[tuple[int, int]]],
) -> dict[tuple[int, int], int]:
    """
    Use BFS to find the shortest path (minimum doors) from origin to all rooms.

    Breadth-First Search guarantees we find the shortest path in an unweighted
    graph. Each door counts as 1 edge, so BFS naturally gives us the minimum
    number of doors to pass through.

    Args:
        doors: The bidirectional door graph from build_door_graph()

    Returns:
        Dictionary mapping each reachable room to its minimum door count from (0,0)
    """
    # Distance from origin to each room
    distances = {(0, 0): 0}

    # BFS queue
    queue = deque([(0, 0)])

    while queue:
        current_pos = queue.popleft()
        current_dist = distances[current_pos]

        # Explore all adjacent rooms
        for next_pos in doors[current_pos]:
            if next_pos not in distances:
                # First time reaching this room - record distance
                distances[next_pos] = current_dist + 1
                queue.append(next_pos)

    return distances


def part_one(data: list[str]) -> int:
    """
    Find the largest minimum distance to any room.

    This represents the furthest room from the starting position, where
    "furthest" means requiring the most doors to reach via the shortest path.

    Args:
        data: List containing the regex string

    Returns:
        Maximum number of doors required to reach any room
    """
    regex = data[0]
    doors = build_door_graph(regex)
    distances = compute_shortest_distances(doors)
    return max(distances.values())


def part_two(data: list[str]) -> int:
    """
    Count how many rooms require passing through at least 1000 doors.

    Args:
        data: List containing the regex string

    Returns:
        Number of rooms with distance >= 1000
    """
    regex = data[0]
    doors = build_door_graph(regex)
    distances = compute_shortest_distances(doors)
    return sum(distance >= 1000 for distance in distances.values())


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 3675
    print("Part 2:", part_two(data))  # 7953
