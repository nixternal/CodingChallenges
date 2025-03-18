#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("16.in", "r") as file:
        return file.read().split(',')


def dance(programs: list, moves: list) -> list:
    for move in moves:
        if move[0] == 's':  # Spin
            x = int(move[1:])
            programs = programs[-x:] + programs[:-x]
        elif move[0] == 'x':  # Exchange
            a, b = map(int, move[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif move[0] == 'p':  # Partner
            a, b = programs.index(move[1]), programs.index(move[3])
            programs[a], programs[b], = programs[b], programs[a]
    return programs


def find_cycle_length(initial: list, moves: list) -> tuple:
    seen = {}
    programs = initial.copy()
    for i in range(1, 1_000_000):
        programs = dance(programs, moves)
        state = ''.join(programs)
        if state in seen:
            return i - seen[state], seen[state]
        seen[state] = i

    return None, None


def part_one(data: list) -> str:
    programs = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    ]
    return ''.join(dance(programs, data))


def part_two(data: list) -> str:
    programs = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'
    ]

    cycle_length, offset = find_cycle_length(programs, data)
    remaining_dances = (1_000_000_000 - offset) % cycle_length

    for _ in range(offset + remaining_dances):
        programs = dance(programs, data)

    return ''.join(programs)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # ehdpincaogkblmfj
    print("Part 2:", part_two(data))  # bpcekomfgjdlinha
