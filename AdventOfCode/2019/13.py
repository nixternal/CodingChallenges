#!/usr/bin/env python3


def read_puzzle_input() -> list:
    """Return the raw input as a list of strings (one per line)."""
    with open("13.in", "r") as file:
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


def run_intcode_generator(program: list[int]):
    """
    Generator version that yields outputs and accepts inputs via send().
    Yields outputs as they're produced.
    When input is needed, yields None - caller should then send() the input value.
    """
    memory = {i: val for i, val in enumerate(program)}
    ip = 0
    relative_base = 0

    while True:
        instr = memory.get(ip, 0)
        opcode = instr % 100
        modes = [(instr // (10**i)) % 10 for i in range(2, 5)]

        if opcode == 99:
            break

        elif opcode in {1, 2}:  # add or multiply
            a = get_value(memory, ip + 1, modes[0], relative_base)
            b = get_value(memory, ip + 2, modes[1], relative_base)
            dest = get_address(memory, ip + 3, modes[2], relative_base)
            memory[dest] = a + b if opcode == 1 else a * b
            ip += 4

        elif opcode == 3:  # input
            value = yield None  # Signal that input is needed
            dest = get_address(memory, ip + 1, modes[0], relative_base)
            memory[dest] = value
            ip += 2

        elif opcode == 4:  # output
            val = get_value(memory, ip + 1, modes[0], relative_base)
            ip += 2
            yield val

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


def part_one(data: list) -> int:
    """
    Part 1: Count the number of block tiles on the screen when the game exits.
    Tile types: 0=empty, 1=wall, 2=block, 3=paddle, 4=ball
    """
    program = [int(x) for x in data[0].split(",")]
    gen = run_intcode_generator(program)

    grid = {}
    outputs = []

    output = None
    try:
        while True:
            output = gen.send(output)
            if output is None:
                # Input needed (shouldn't happen in part 1)
                output = 0
            else:
                outputs.append(output)
                if len(outputs) == 3:
                    x, y, tile_id = outputs
                    grid[(x, y)] = tile_id
                    outputs = []
                output = None
    except StopIteration:
        pass

    # Count block tiles (tile_id == 2)
    return sum(1 for tile in grid.values() if tile == 2)


def part_two(data: list) -> int:
    """
    Part 2: Beat the game by breaking all blocks. Return the final score.
    Set memory[0] = 2 to play for free.
    Score is displayed at x=-1, y=0.
    Input: -1 (left), 0 (neutral), 1 (right) to move paddle.
    """
    program = [int(x) for x in data[0].split(",")]
    program[0] = 2  # Play for free

    gen = run_intcode_generator(program)

    grid = {}
    score = 0
    ball_x = 0
    paddle_x = 0
    outputs = []

    output = None
    try:
        while True:
            output = gen.send(output)
            if output is None:
                # Input needed - move paddle toward ball
                if ball_x < paddle_x:
                    output = -1
                elif ball_x > paddle_x:
                    output = 1
                else:
                    output = 0
            else:
                outputs.append(output)
                if len(outputs) == 3:
                    x, y, tile_id = outputs

                    if x == -1 and y == 0:
                        # Special position for score
                        score = tile_id
                    else:
                        grid[(x, y)] = tile_id

                        # Track ball and paddle positions
                        if tile_id == 4:  # ball
                            ball_x = x
                        elif tile_id == 3:  # paddle
                            paddle_x = x

                    outputs = []
                output = None
    except StopIteration:
        pass

    return score


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 280
    print("Part 2:", part_two(data))  # 13298
