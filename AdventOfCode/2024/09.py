#!/usr/bin/env python


def read_puzzle_input() -> list:
    """
    Read the file and create a list.

    :return: A list that contains stuff
    :rtype: list
    """

    with open("09.in", "r") as file:
        return list(file.read().strip())


def part_one(data: list) -> int:
    disk = []
    fid = 0
    for i, char in enumerate(data):
        x = int(char)
        if i % 2 == 0:
            disk += [fid] * x
            fid += 1
        else:
            disk += [-1] * x

    blanks = [i for i, x in enumerate(disk) if x == -1]

    for i in blanks:
        while disk[-1] == -1:
            disk.pop()
        if len(disk) < i:
            break
        disk[i] = disk.pop()

    return sum(i * x for i, x in enumerate(disk))


def part_two(data: list) -> int:
    sum = 0
    fid = 0
    pos = 0

    files = {}
    blanks = []

    for i, char in enumerate(data):
        x = int(char)
        if i % 2 == 0:
            if x == 0:
                raise ValueError("unexpected x=0 for file")
            files[fid] = (pos, x)
            fid += 1
        else:
            if x != 0:
                blanks.append((pos, x))
        pos += x

    while fid > 0:
        fid -= 1
        pos, size = files[fid]
        pos, size = files[fid]
        for i, (start, length) in enumerate(blanks):
            if start >= pos:
                blanks = blanks[:i]
                break
            if size <= length:
                files[fid] = (start, size)
                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)
                break

    for fid, (pos, size) in files.items():
        for x in range(pos, pos + size):
            sum += fid * x

    return sum


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 6360094256423
    print("Part 2:", part_two(data))  # answer
