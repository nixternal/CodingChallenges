#!/usr/bin/env python
import heapq

def read_puzzle_input() -> list:
    with open("18.in", "r") as file:
        return file.read().splitlines()

def get_distances(grid, start_pos):
    """BFS to find distances from a point to all reachable keys and required doors."""
    dists = {}
    queue = [(start_pos, 0, 0)] # pos, distance, doors_mask
    visited = {start_pos}

    while queue:
        (r, c), d, doors = queue.pop(0)
        char = grid[r][c]

        # If we hit a key (and it's not the starting point)
        if char.islower() and (r, c) != start_pos:
            dists[char] = (d, doors)

        # Update doors mask if we hit a door
        new_doors = doors
        if char.isupper():
            new_doors |= (1 << (ord(char.lower()) - ord('a')))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and \
               grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), d + 1, new_doors))
    return dists

def solve(grid, entrances, all_keys_mask):
    # key_graph[start_node] = { target_key: (distance, required_doors_mask) }
    key_graph = {}
    key_positions = {grid[r][c]: (r, c) for r in range(len(grid)) for c in range(len(grid[0]))
                     if grid[r][c].islower()}

    # Add entrances to graph
    for i, pos in enumerate(entrances):
        key_graph[str(i)] = get_distances(grid, pos)

    # Add all keys to graph
    for key, pos in key_positions.items():
        key_graph[key] = get_distances(grid, pos)

    # Dijkstra state: (distance, current_nodes_tuple, collected_mask)
    pq = [(0, tuple(str(i) for i in range(len(entrances))), 0)]
    visited = {}

    while pq:
        dist, current_nodes, mask = heapq.heappop(pq)

        if mask == all_keys_mask:
            return dist

        state = (current_nodes, mask)
        if visited.get(state, float('inf')) <= dist:
            continue
        visited[state] = dist

        # Try moving each robot
        for robot_idx, node in enumerate(current_nodes):
            for next_key, (d, doors) in key_graph[node].items():
                # Check if we already have the key
                key_bit = 1 << (ord(next_key) - ord('a'))
                if mask & key_bit:
                    continue

                # Check if we have all doors required for this path
                if (doors & mask) == doors:
                    new_mask = mask | key_bit
                    new_nodes = list(current_nodes)
                    new_nodes[robot_idx] = next_key
                    heapq.heappush(pq, (dist + d, tuple(new_nodes), new_mask))
    return -1

def part_one(data: list) -> int:
    grid = [list(line) for line in data]
    start = next((r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == '@')
    all_keys_mask = sum(1 << (ord(c) - ord('a')) for r in grid for c in r if c.islower())
    return solve(grid, [start], all_keys_mask)

def part_two(data: list) -> int:
    grid = [list(line) for line in data]
    r, c = next((r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == '@')

    # Modify grid for Part 2
    grid[r-1][c-1:c+2] = ['@', '#', '@']
    grid[r][c-1:c+2]   = ['#', '#', '#']
    grid[r+1][c-1:c+2] = ['@', '#', '@']

    entrances = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
    all_keys_mask = sum(1 << (ord(c) - ord('a')) for row in grid for c in row if c.islower())
    return solve(grid, entrances, all_keys_mask)

if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 4204
    print("Part 2:", part_two(data))  # 1682
