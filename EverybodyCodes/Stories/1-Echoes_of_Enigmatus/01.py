#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("01.in", "r") as file:
        return file.read().split("\n\n")


def eni(n: int, x: int, m: int, last: int = 99999) -> int:
    if last >= x:
        remainders = [str(pow(n, i, m)) for i in range(x, 0, -1)]
    else:
        remainders = [str(pow(n, i, m)) for i in range(x, x - last, -1)]
    return int("".join(remainders))


def eni3(n: int, x: int, m: int) -> int:
    scores = []
    score = 1
    seen = {}
    for i in range(x):
        score = (score * n) % m
        if score in seen:
            cycle_start = seen[score]
            cycle_len = i - cycle_start
            cycle_sum = sum(scores[cycle_start:i])
            pre_sum = sum(scores[:cycle_start])
            remaining = x - cycle_start
            full_cycles, leftover = divmod(remaining, cycle_len)
            leftover_sum = sum(scores[cycle_start:cycle_start + leftover])
            return pre_sum + full_cycles * cycle_sum + leftover_sum
        seen[score] = i
        scores.append(score)

    return sum(scores)


def part_one(data: list) -> int:
    m = 0
    for line in data[0].strip().split("\n"):
        params = {k: int(v) for pair in line.split() for k, v in [pair.split("=")]}
        m = max(
            m,
            eni(params["A"], params["X"], params["M"])
            + eni(params["B"], params["Y"], params["M"])
            + eni(params["C"], params["Z"], params["M"]),
        )
    return m


def part_two(data: list) -> int:
    m = 0
    for line in data[1].strip().split("\n"):
        params = {k: int(v) for pair in line.split() for k, v in [pair.split("=")]}
        m = max(
            m,
            eni(params["A"], params["X"], params["M"], 5)
            + eni(params["B"], params["Y"], params["M"], 5)
            + eni(params["C"], params["Z"], params["M"], 5),
        )
    return m


def part_three(data: list) -> int:
    m = 0
    for line in data[2].strip().split("\n"):
        params = {k: int(v) for pair in line.split() for k, v in [pair.split("=")]}
        m = max(
            m,
            eni3(params["A"], params["X"], params["M"])
            + eni3(params["B"], params["Y"], params["M"])
            + eni3(params["C"], params["Z"], params["M"]),
        )
    return m


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 9308152626
    print("Part 2:", part_two(data))  # 153234789454987
    print("Part 3:", part_three(data))  # 596526575202176
