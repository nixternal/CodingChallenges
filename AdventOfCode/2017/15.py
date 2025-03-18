#!/usr/bin/env python


def generator(previous: int, factor: int, multiple: int = 1) -> int:
    """
    Generate the next value that's a multiple of the given number.

    Args:
        previous: The previous value in the sequence
        factor: The generator-specific factor to multiply by
        multiple: The value must be divisible by this number (default=1)

    Returns:
        The next value in the sequence
    """

    value = previous
    while True:
        value = (value * factor) % 2147483647  # modulus from puzzle text
        if value % multiple == 0:
            return value


def count_matches(gen_a_start: int, gen_b_start: int, pairs: int,
                  multiple_a: int = 1, multiple_b: int = 1) -> int:
    """
    Count matching pairs with configurable criteria for both parts.

    Args:
        gen_a_start: Starting value for generator A
        gen_b_start: Starting value for generator B
        pairs: Number of pairs to check
        multiple_a: Generator A values must be divisible by this (default=1)
        multiple_b: Generator B values must be divisible by this (default=1)

    Returns:
        Number of pairs with matching lowest 16 bits
    """

    gen_a = gen_a_start
    gen_b = gen_b_start

    factor_a = 16807  # factor provided in puzzle's text
    factor_b = 48271  # factor provided in puzzle's text

    mask = 0xFFFF  # Mask for lowest 16 bits
    matches = 0

    for _ in range(pairs):
        gen_a = generator(gen_a, factor_a, multiple_a)
        gen_b = generator(gen_b, factor_b, multiple_b)

        if (gen_a & mask) == (gen_b & mask):
            matches += 1

    return matches


def part_one(data: list) -> int:
    return count_matches(data[0], data[1], 40_000_000)


def part_two(data: list) -> int:
    return count_matches(data[0], data[1], 5_000_000, 4, 8)


if __name__ == "__main__":
    data = [679, 771]
    print("Part 1:", part_one(data))  # 626
    print("Part 2:", part_two(data))  # 306
