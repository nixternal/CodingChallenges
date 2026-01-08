#!/usr/bin/env python3

from collections import deque


def read_puzzle_input() -> list:
    """Return the raw input as a list of strings (one per line)."""
    with open("15.in", "r") as file:
        return file.read().splitlines()


def get_value(memory: dict[int, int], pos: int, mode: int, relative_base: int) -> int:
    """Return the parameter value according to its mode."""
    if mode == 0:  # position mode
        addr = memory.get(pos, 0)
        return memory.get(addr, 0)
    elif mode == 1:  # immediate mode
        return memory.get(pos, 0)
    elif mode == 2:  # relative mode
        addr = relative_base + memory.get(pos, 0)
        return memory.get(addr, 0)
    else:
        raise ValueError(f"Unknown parameter mode {mode}")


def get_address(memory: dict[int, int], pos: int, mode: int, relative_base: int) -> int:
    """Return the address for writes according to its mode."""
    if mode == 0:  # position mode
        return memory.get(pos, 0)
    elif mode == 2:  # relative mode
        return relative_base + memory.get(pos, 0)
    else:
        raise ValueError(f"Invalid mode {mode} for write address")


def run_intcode_interactive(state: dict) -> tuple[int | None, dict]:
    """
    Run intcode until it produces output or halts.
    State dict contains: memory, ip, relative_base, input_queue, halted
    Returns: (output_value or None, updated_state)
    """
    memory = state["memory"]
    ip = state["ip"]
    relative_base = state["relative_base"]
    input_queue = state["input_queue"]

    while True:
        instr = memory.get(ip, 0)
        opcode = instr % 100
        modes = [(instr // (10**i)) % 10 for i in range(2, 5)]

        if opcode == 99:
            state["halted"] = True
            return None, state

        elif opcode in {1, 2}:  # add or multiply
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            dest = get_address(memory, ip + 3, modes[2], relative_base)
            memory[dest] = a + b if opcode == 1 else a * b
            ip += 4

        elif opcode == 3:  # input
            if not input_queue:
                raise RuntimeError("Program requested input but none available")
            value = input_queue.popleft()
            dest = get_address(memory, ip + 1, modes[0], relative_base)
            memory[dest] = value
            ip += 2

        elif opcode == 4:  # output
            val = get_value(memory, ip + 1, modes[0], relative_base)
            ip += 2
            state["ip"] = ip
            state["relative_base"] = relative_base
            return val, state

        elif opcode in {5, 6}:  # jump-if-true / jump-if-false
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                ip = b
            else:
                ip += 3

        elif opcode in {7, 8}:  # less-than / equals
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            dest = get_address(memory, ip + 3, modes[2], relative_base)
            if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                memory[dest] = 1
            else:
                memory[dest] = 0
            ip += 4

        elif opcode == 9:  # adjust relative base
            a = get_value(memory, ip + 1, modes[0], relative_base)
            relative_base += a
            ip += 2

        else:
            raise ValueError(f"Unknown opcode {opcode} at position {ip}")

        state["ip"] = ip
        state["relative_base"] = relative_base


def create_intcode_state(program: list[int]) -> dict:
    """Create initial state for the intcode computer."""
    return {
        "memory": {i: val for i, val in enumerate(program)},
        "ip": 0,
        "relative_base": 0,
        "input_queue": deque(),
        "halted": False
    }


def send_command(state: dict, command: int) -> int:
    """
    Send a movement command and get status back.
    command: 1=north, 2=south, 3=west, 4=east
    returns: 0=wall, 1=moved, 2=moved to oxygen system
    """
    state["input_queue"].append(command)
    output: int | None
    output, state = run_intcode_interactive(state)
    if output is None:
        raise RuntimeError("Program halted unexpectedly")
    return output


def part_one(data: list) -> int:
    """
    Find the shortest path from starting position to the oxygen system.
    Uses DFS to fully explore and map the maze first, then finds shortest path.
    """
    program = [int(x) for x in data[0].split(",")]

    # Direction mappings
    NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
    directions = {
        NORTH: (0, -1),
        SOUTH: (0, 1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }
    reverse = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

    # DFS to map the entire maze
    state = create_intcode_state(program)
    maze = {(0, 0): 1}  # position -> status (0=wall, 1=open, 2=oxygen)
    oxygen_pos = None

    def dfs(pos):
        nonlocal oxygen_pos
        for direction, (dx, dy) in directions.items():
            new_pos = (pos[0] + dx, pos[1] + dy)

            if new_pos in maze:
                continue

            # Try to move
            status = send_command(state, direction)
            maze[new_pos] = status

            if status == 2:  # Found oxygen!
                oxygen_pos = new_pos
                dfs(new_pos)  # Continue exploring from oxygen
                send_command(state, reverse[direction])  # Backtrack
            elif status == 1:  # Open space
                dfs(new_pos)  # Explore recursively
                send_command(state, reverse[direction])  # Backtrack
            # If status == 0 (wall), don't move, just continue

    dfs((0, 0))

    # Now BFS from start to oxygen on the mapped maze
    if oxygen_pos is None:
        return -1

    queue = deque([((0, 0), 0)])
    visited = {(0, 0)}

    while queue:
        pos, dist = queue.popleft()

        if pos == oxygen_pos:
            return dist

        for _, (dx, dy) in directions.items():
            new_pos = (pos[0] + dx, pos[1] + dy)

            if new_pos in visited or maze.get(new_pos, 0) == 0:
                continue

            visited.add(new_pos)
            queue.append((new_pos, dist + 1))

    return -1  # Not found


def part_two(data: list) -> int:
    """
    Find how many minutes it takes for oxygen to fill the entire area.
    This is the maximum distance from the oxygen system to any open space.
    """
    program = [int(x) for x in data[0].split(",")]

    # Direction mappings
    NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
    directions = {
        NORTH: (0, -1),
        SOUTH: (0, 1),
        WEST: (-1, 0),
        EAST: (1, 0)
    }
    reverse = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

    # DFS to map the entire maze
    state = create_intcode_state(program)
    maze = {(0, 0): 1}  # position -> status (0=wall, 1=open, 2=oxygen)
    oxygen_pos = None

    def dfs(pos):
        nonlocal oxygen_pos
        for direction, (dx, dy) in directions.items():
            new_pos = (pos[0] + dx, pos[1] + dy)

            if new_pos in maze:
                continue

            # Try to move
            status = send_command(state, direction)
            maze[new_pos] = status

            if status == 2:  # Found oxygen!
                oxygen_pos = new_pos
                dfs(new_pos)  # Continue exploring from oxygen
                send_command(state, reverse[direction])  # Backtrack
            elif status == 1:  # Open space
                dfs(new_pos)  # Explore recursively
                send_command(state, reverse[direction])  # Backtrack

    dfs((0, 0))

    if oxygen_pos is None:
        return -1

    # BFS from oxygen to find maximum distance to any open space
    queue = deque([(oxygen_pos, 0)])
    visited = {oxygen_pos}
    max_time = 0

    while queue:
        pos, time = queue.popleft()
        max_time = max(max_time, time)

        for _, (dx, dy) in directions.items():
            new_pos = (pos[0] + dx, pos[1] + dy)

            # Only spread to open spaces (status 1 or 2) that haven't been visited
            if new_pos in visited or maze.get(new_pos, 0) == 0:
                continue

            visited.add(new_pos)  # pyright: ignore
            queue.append((new_pos, time + 1))  # pyright: ignore

    return max_time


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 266
    print("Part 2:", part_two(data))  # 274
