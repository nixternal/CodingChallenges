#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("17.in", "r") as file:
        return [int(x) for x in file.read().strip().split(",")]


def run_intcode(memory, inputs):
    mem = {i: v for i, v in enumerate(memory)}
    ip = rb = 0
    outputs = []
    inputs = list(inputs)

    def get_addr(i, mode):
        if mode == 0:
            return mem.get(i, 0)
        if mode == 1:
            return i
        return mem.get(i, 0) + rb

    while True:
        instr = str(mem.get(ip, 0)).zfill(5)
        opcode = int(instr[-2:])
        m1, m2, m3 = int(instr[2]), int(instr[1]), int(instr[0])
        if opcode == 99:
            break
        if opcode == 1:
            mem[get_addr(ip + 3, m3)] = mem.get(get_addr(ip + 1, m1), 0) + mem.get(
                get_addr(ip + 2, m2), 0
            )
            ip += 4
        elif opcode == 2:
            mem[get_addr(ip + 3, m3)] = mem.get(get_addr(ip + 1, m1), 0) * mem.get(
                get_addr(ip + 2, m2), 0
            )
            ip += 4
        elif opcode == 3:
            if not inputs:
                break
            mem[get_addr(ip + 1, m1)] = inputs.pop(0)
            ip += 2
        elif opcode == 4:
            outputs.append(mem.get(get_addr(ip + 1, m1), 0))
            ip += 2
        elif opcode == 5:
            ip = (
                mem.get(get_addr(ip + 2, m2), 0)
                if mem.get(get_addr(ip + 1, m1), 0) != 0
                else ip + 3
            )
        elif opcode == 6:
            ip = (
                mem.get(get_addr(ip + 2, m2), 0)
                if mem.get(get_addr(ip + 1, m1), 0) == 0
                else ip + 3
            )
        elif opcode == 7:
            mem[get_addr(ip + 3, m3)] = (
                1
                if mem.get(get_addr(ip + 1, m1), 0) < mem.get(get_addr(ip + 2, m2), 0)
                else 0
            )
            ip += 4
        elif opcode == 8:
            mem[get_addr(ip + 3, m3)] = (
                1
                if mem.get(get_addr(ip + 1, m1), 0) == mem.get(get_addr(ip + 2, m2), 0)
                else 0
            )
            ip += 4
        elif opcode == 9:
            rb += mem.get(get_addr(ip + 1, m1), 0)
            ip += 2
    return outputs


def get_grid(data):
    output = run_intcode(data, [])
    grid_str = "".join(chr(x) for x in output).strip()
    return [list(line) for line in grid_str.split("\n")]


def get_full_path(grid):
    # Directions: 0:N, 1:E, 2:S, 3:W
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    r, c = next(
        (r, c)
        for r, row in enumerate(grid)
        for c, val in enumerate(row)
        if val in "^v<>"
    )
    d = {"^": 0, ">": 1, "v": 2, "<": 3}[grid[r][c]]

    path = []
    while True:
        steps = 0
        dr, dc = dirs[d]
        # Move forward
        while (
            0 <= r + dr < len(grid)
            and 0 <= c + dc < len(grid[0])
            and grid[r + dr][c + dc] == "#"
        ):
            r, c = r + dr, c + dc
            steps += 1
        if steps > 0:
            path.append(str(steps))

        # Turn
        left = (d - 1) % 4
        right = (d + 1) % 4
        if (
            0 <= r + dirs[left][0] < len(grid)
            and 0 <= c + dirs[left][1] < len(grid[0])
            and grid[r + dirs[left][0]][c + dirs[left][1]] == "#"
        ):
            path.append("L")
            d = left
        elif (
            0 <= r + dirs[right][0] < len(grid)
            and 0 <= c + dirs[right][1] < len(grid[0])
            and grid[r + dirs[right][0]][c + dirs[right][1]] == "#"
        ):
            path.append("R")
            d = right
        else:
            break
    return path


def solve_compression(path_tokens):
    """Brute force the possible subroutine lengths."""
    path_str = ",".join(path_tokens)

    for i in range(1, 11):  # Try lengths for A
        a_sub = ",".join(path_tokens[:i])
        if len(a_sub) > 20:
            break

        # Replace all A in path
        path_after_a = path_str.replace(a_sub, "A").strip(",")

        # Find first non-A/B/C part to define B
        remaining_tokens = [t for t in path_after_a.split(",") if t not in "ABC"]
        if not remaining_tokens:
            continue

        # We need to find where the first "non-A" chunk starts in the sequence
        # to properly pick the next subroutine.
        temp_path = path_str.replace(a_sub, "A")

        for j in range(1, 11):  # Try lengths for B
            # B must start at the first point that isn't A
            current_tokens = temp_path.split(",")
            start_idx = next(
                idx for idx, val in enumerate(current_tokens) if val != "A"
            )
            b_sub = ",".join(current_tokens[start_idx : start_idx + j])
            if "A" in b_sub or len(b_sub) > 20:
                break

            temp_path_b = temp_path.replace(b_sub, "B")

            for k in range(1, 11):  # Try lengths for C
                parts_c = [p for p in temp_path_b.split(",") if p not in "AB"]
                if not parts_c:
                    continue

                start_idx_c = next(
                    idx
                    for idx, val in enumerate(temp_path_b.split(","))
                    if val not in "AB"
                )
                c_sub = ",".join(temp_path_b.split(",")[start_idx_c : start_idx_c + k])
                if "A" in c_sub or "B" in c_sub or len(c_sub) > 20:
                    break

                final_main = temp_path_b.replace(c_sub, "C")
                # Check if this configuration covers the whole path
                if all(t in "ABC," for t in final_main) and len(final_main) <= 20:
                    return final_main, a_sub, b_sub, c_sub
    return None


def part_one(data: list) -> int:
    grid = get_grid(data)
    total = 0
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] == "#" and all(
                grid[r + dr][c + dc] == "#"
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            ):
                total += r * c
    return total


def part_two(data: list) -> int:
    grid = get_grid(data)
    path_tokens = get_full_path(grid)

    compression = solve_compression(path_tokens)
    if not compression:
        return -2  # Failed to compress

    main, a, b, c = compression

    # Format for Intcode
    input_str = f"{main}\n{a}\n{b}\n{c}\nn\n"
    ascii_input = [ord(char) for char in input_str]

    # Create a fresh copy of data and set address 0
    program = list(data)
    program[0] = 2

    output = run_intcode(program, ascii_input)
    return output[-1]


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 14332
    print("Part 2:", part_two(data))  # 1034009
