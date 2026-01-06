#!/usr/bin/env python3


def read_puzzle_input() -> list:
    with open("11.in", "r") as file:
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


class IntcodeComputer:
    """Intcode computer that can pause for I/O."""

    def __init__(self, program: list[int]):
        self.memory = {i: val for i, val in enumerate(program)}
        self.ip = 0
        self.relative_base = 0
        self.halted = False
        self.input_queue = []
        self.output_queue = []

    def add_input(self, value: int):
        """Add a value to the input queue."""
        self.input_queue.append(value)

    def get_output(self) -> int | None:
        """Get the next output value, or None if empty."""
        return self.output_queue.pop(0) if self.output_queue else None

    def run_until_output_or_halt(self):
        """Run until we produce an output or halt."""
        while not self.halted:
            instr = self.memory.get(self.ip, 0)
            opcode = instr % 100
            modes = [(instr // (10**i)) % 10 for i in range(2, 5)]

            if opcode == 99:
                self.halted = True
                break

            elif opcode in {1, 2}:  # add or multiply
                a = get_value(self.memory, self.ip + 1, modes[0], self.relative_base)
                b = get_value(self.memory, self.ip + 2, modes[1], self.relative_base)
                dest = get_address(
                    self.memory, self.ip + 3, modes[2], self.relative_base
                )
                self.memory[dest] = a + b if opcode == 1 else a * b
                self.ip += 4

            elif opcode == 3:  # input
                if not self.input_queue:
                    return  # Pause until input is provided
                value = self.input_queue.pop(0)
                dest = get_address(
                    self.memory, self.ip + 1, modes[0], self.relative_base
                )
                self.memory[dest] = value
                self.ip += 2

            elif opcode == 4:  # output
                val = get_value(self.memory, self.ip + 1, modes[0], self.relative_base)
                self.output_queue.append(val)
                self.ip += 2
                return  # Pause after output

            elif opcode in {5, 6}:  # jump-if-true / jump-if-false
                a = get_value(self.memory, self.ip + 1, modes[0], self.relative_base)
                b = get_value(self.memory, self.ip + 2, modes[1], self.relative_base)
                if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                    self.ip = b
                else:
                    self.ip += 3

            elif opcode in {7, 8}:  # less-than / equals
                a = get_value(self.memory, self.ip + 1, modes[0], self.relative_base)
                b = get_value(self.memory, self.ip + 2, modes[1], self.relative_base)
                dest = get_address(
                    self.memory, self.ip + 3, modes[2], self.relative_base
                )
                if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                    self.memory[dest] = 1
                else:
                    self.memory[dest] = 0
                self.ip += 4

            elif opcode == 9:  # adjust relative base
                a = get_value(self.memory, self.ip + 1, modes[0], self.relative_base)
                self.relative_base += a
                self.ip += 2

            else:
                raise ValueError(f"Unknown opcode {opcode} at position {self.ip}")


def run_robot(program: list[int], start_color: int = 0) -> dict[tuple[int, int], int]:
    """Run the painting robot and return the painted panels."""
    computer = IntcodeComputer(program)

    # Track painted panels and robot state
    panels = {}  # (x, y) -> color (0=black, 1=white)
    x, y = 0, 0
    direction = 0  # 0=up, 1=right, 2=down, 3=left
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]

    panels[(x, y)] = start_color

    while not computer.halted:
        # Provide current panel color as input
        current_color = panels.get((x, y), 0)
        computer.add_input(current_color)

        # Run until we get two outputs (paint color and turn direction)
        computer.run_until_output_or_halt()
        if computer.halted:
            break
        paint_color = computer.get_output()

        computer.run_until_output_or_halt()
        if computer.halted:
            break
        turn = computer.get_output()

        # Paint the current panel
        panels[(x, y)] = paint_color

        # Turn and move
        if turn == 0:  # turn left
            direction = (direction - 1) % 4
        else:  # turn right
            direction = (direction + 1) % 4

        x += dx[direction]
        y += dy[direction]

    return panels


def part_one(data: list) -> int:
    """Count how many panels get painted at least once."""
    program = [int(x) for x in data[0].split(",")]
    panels = run_robot(program, start_color=0)
    return len(panels)


def part_two(data: list) -> None:
    """Paint the registration identifier and display it."""
    program = [int(x) for x in data[0].split(",")]
    panels = run_robot(program, start_color=1)

    # Find bounds
    xs = [x for x, _ in panels.keys()]
    ys = [y for _, y in panels.keys()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # Print the registration identifier
    print("Part 2:")
    for y in range(max_y, min_y - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "█" if panels.get((x, y), 0) == 1 else " "
        print(line)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2226
    part_two(data)  # HBGLZKLF
