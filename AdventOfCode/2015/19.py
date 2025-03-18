#!/usr/bin/env python

import random


def read_puzzle_input() -> list:
    with open("19.in", "r") as file:
        return file.read().splitlines()


def backtracks(s, rep):
    count = 0
    old_s = ''
    keys = list(rep.keys())
    random.shuffle(keys)
    while old_s != s:
        old_s = s
        for key in keys:
            while key in s:
                count += s.count(key)
                s = s.replace(key, rep[key])
    return int(s == 'e') * count


def shared_function(data: list) -> tuple[set, str, dict]:
    data = read_puzzle_input()
    rep = {}
    inv_rep = {}
    s = ''
    for line in data:
        if '=>' in line:
            key, val = line.rstrip().split(' => ')
            inv_rep[val] = key
            if key not in rep:
                rep[key] = []
            rep[key].append(val)
        else:
            s = line.rstrip()

    changes = set()
    for key in rep.keys():
        i = s.find(key, 0)
        while i != -1:
            for val in rep[key]:
                changes.add(s[0:i] + val + s[i+len(key):])
            i = s.find(key, i + 1)

    return (changes, s, inv_rep)


def part_one(data: list) -> int:
    changes, _, _ = shared_function(data)
    return len(changes)


def part_two(data: list) -> int:
    _, s, inv_rep = shared_function(data)
    p2 = 0
    while p2 == 0:
        p2 = backtracks(s, inv_rep)
    return p2


if __name__ == '__main__':
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 576
    print("Part 2:", part_two(data))  # 207
