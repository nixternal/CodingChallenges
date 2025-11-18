#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("11.in", "r") as file:
        return file.read().split("\n\n")


def flock_checksum(cols):
    return sum((i + 1) * c for i, c in enumerate(cols))


def simulate_round(cols, phase):
    n = len(cols)
    cols = cols[:]
    changed = False

    for i in range(n - 1):
        if phase == 1:
            if cols[i] > cols[i + 1]:
                cols[i] -= 1
                cols[i + 1] += 1
                changed = True
        else:  # Phase 2
            if cols[i] < cols[i + 1]:
                cols[i] += 1
                cols[i + 1] -= 1
                changed = True


    return changed, cols


def part_one(data: list) -> int:
    cols = [int(x) for x in data[0].splitlines()]
    target_round = 10
    round_num = 0
    checksums = [flock_checksum(cols)]

    # Phase 1
    while True:
        changed, new_cols = simulate_round(cols, phase=1)
        if not changed:
            break
        cols = new_cols
        round_num += 1
        checksums.append(flock_checksum(cols))
        if round_num == target_round:
            return checksums[-1]

    # Phase 2
    while True:
        changed, new_cols = simulate_round(cols, phase=2)
        cols = new_cols
        round_num += 1
        checksums.append(flock_checksum(cols))
        if round_num == target_round:
            return checksums[-1]
        if not changed:
            break

    return -1


def part_two(data: list) -> int:
    cols = [int(x) for x in data[1].splitlines()]
    round_num = 0

    # Phase 1
    while True:
        changed, new_cols = simulate_round(cols, phase=1)
        if not changed:
            break
        cols = new_cols
        round_num += 1

    # Phase 2
    while True:
        changed, new_cols = simulate_round(cols, phase=2)
        cols = new_cols
        round_num += 1

        # check if all equal
        if len(set(cols)) == 1:
            return round_num

        if not changed:
            return round_num


def part_three(data: list) -> int:
    cols = [int(x) for x in data[2].splitlines()]
    n = len(cols)
    total = sum(cols)

    if total % n != 0:
        return -1

    target = total // n
    max_deficit = 0
    current_sum = 0

    for i in range(n):
        current_sum += cols[i]
        # How many do we expect to have by position i if we had target everywhere?
        expected = target * (i + 1)
        # If we have less than expected, we have a deficit
        if current_sum < expected:
            deficit = expected - current_sum
            # Each round can reduce deficit by at most 1 at each position
            max_deficit = max(max_deficit, deficit)

    return max_deficit


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 253
    print("Part 2:", part_two(data))  # 2627235
    print("Part 3:", part_three(data))  # 129677879584087
