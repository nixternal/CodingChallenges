#!/usr/bin/env python


def read_puzzle_input() -> tuple:
    with open("24.in", "r") as file:
        data = file.read().split('\n\n')
    gates = {
        line.split(':')[0]: int(line.split(':')[1].strip())
        for line in data[0].split('\n')
    }
    formulas = {
        z: (op, x, y)
        for line in data[1].strip().split('\n')
        for x, op, y, z in [line.replace(' -> ', ' ').split(' ')]
    }
    return gates, formulas


def part_one(data: tuple) -> int:
    gates, formulas = data

    operators = {
        "OR": lambda x, y: x | y,
        "AND": lambda x, y: x & y,
        "XOR": lambda x, y: x ^ y
    }

    def calc(wire):
        if wire in gates:
            return gates[wire]
        op, x, y = formulas[wire]
        gates[wire] = operators[op](calc(x), calc(y))
        return gates[wire]

    z = []
    i = 0

    while True:
        key = "z" + str(i).rjust(2, "0")
        if key not in formulas:
            break
        z.append(calc(key))
        i += 1

    return int("".join(map(str, z[::-1])), 2)


def part_two(data: tuple) -> str:
    _, formulas = data

    def make_wire(char, num):
        return char + str(num).rjust(2, "0")

    def verify_z(wire, num):
        # print("vz", wire, num)
        if wire not in formulas:
            return False
        op, x, y = formulas[wire]
        if op != "XOR":
            return False
        if num == 0:
            return sorted([x, y]) == ["x00", "y00"]
        return (
            verify_intermediate_xor(x, num) and
            verify_carry_bit(y, num) or
            verify_intermediate_xor(y, num) and
            verify_carry_bit(x, num)
        )

    def verify_intermediate_xor(wire, num):
        # print("vx", wire, num)
        if wire not in formulas:
            return False
        op, x, y = formulas[wire]
        if op != "XOR":
            return False
        return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]

    def verify_carry_bit(wire, num):
        # print("vc", wire, num)
        if wire not in formulas:
            return False
        op, x, y = formulas[wire]
        if num == 1:
            if op != "AND":
                return False
            return sorted([x, y]) == ["x00", "y00"]
        if op != "OR":
            return False
        return (
            verify_direct_carry(x, num - 1) and
            verify_recarry(y, num - 1) or
            verify_direct_carry(y, num - 1) and
            verify_recarry(x, num - 1)
        )

    def verify_direct_carry(wire, num):
        # print("vd", wire, num)
        if wire not in formulas:
            return False
        op, x, y = formulas[wire]
        if op != "AND":
            return False
        return sorted([x, y]) == [make_wire("x", num), make_wire("y", num)]

    def verify_recarry(wire, num):
        # print("vr", wire, num)
        if wire not in formulas:
            return False
        op, x, y = formulas[wire]
        if op != "AND":
            return False
        return (
            verify_intermediate_xor(x, num) and
            verify_carry_bit(y, num) or
            verify_intermediate_xor(y, num) and
            verify_carry_bit(x, num)
        )

    def verify(num):
        return verify_z(make_wire("z", num), num)

    def progress():
        i = 0

        while True:
            if not verify(i):
                break
            i += 1

        return i

    swaps = []

    for _ in range(4):
        baseline = progress()
        for x in formulas:
            for y in formulas:
                if x == y:
                    continue
                formulas[x], formulas[y] = formulas[y], formulas[x]
                if progress() > baseline:
                    break
                formulas[x], formulas[y] = formulas[y], formulas[x]
            else:
                continue
            break
        swaps += [x, y]
    return ",".join(sorted(swaps))


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 45121475050728
    print("Part 2:", part_two(data))  # gqp,hsw,jmh,mwk,qgd,z10,z18,z33
