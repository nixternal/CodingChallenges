#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("11.in", "r") as file:
        return file.read().splitlines()


def convert_to_base_10(number_str: str, base: int) -> int:
    """
    Convert a number from a given base to base-10.

    Args:
    number_str (str): The number as a string
    base (int): The base of the input number (2-62)

    Returns:
    int: The decimal (base-10) representation of the number
    """

    # Define the digit mapping for bases > 10
    digit_map = (
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^'
    )
    return sum(
        digit_map.index(digit) * (base ** power)
        for power, digit in enumerate(reversed(number_str))
    )


def convert_to_base_68(number):
    """
    Convert a base-10 number to base-68 representation.

    Args:
    number (int): The number in base-10

    Returns:
    str: The number in base-68 representation
    """

    # Extended digit mapping to include additional special characters
    digit_map = (
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^'
    )

    # Handle 0 as a special case
    if number == 0:
        return '0'

    # Convert to base-68
    base_68_digits = []

    while number > 0:
        # Get the remainder (which becomes the next digit)
        remainder = number % 68
        base_68_digits.append(digit_map[remainder])

        # Integer division to move to the next digit
        number //= 68

    # Reverse the digits to get the correct representation
    return ''.join(reversed(base_68_digits))


def convert_to_base_n(number, base):
    """
    Convert a base-10 number to a given base.

    Args:
    number (int): The number in base-10
    base (int): The target base

    Returns:
    str: The number in the target base representation
    """

    if base < 2 or base > 100_000:  # Reasonable upper limit
        raise ValueError(f"Base must be between 2 and 100_000, got {base}")

    # Dynamic digit generation for any base
    def generate_digit(value):
        """More explicit and slightly more readable digit generation."""
        digits = {
            range(0, 10): lambda v: str(v),
            range(10, 36): lambda v: chr(v - 10 + ord('A')),
            range(36, 62): lambda v: chr(v - 36 + ord('a')),
            range(62, 68): lambda v: '!@#$%^'[v - 62]
        }

        for digit_range, digit_func in digits.items():
            if value in digit_range:
                return digit_func(value)

        return chr(value)

    # Handle 0 as a special case
    if number == 0:
        return '0'

    # Convert to target base
    base_n_digits = []

    while number > 0:
        # Get the remainder (which becomes the next digit)
        remainder = number % base
        base_n_digits.append(generate_digit(remainder))

        # Integer division to move to the next digit
        number //= base

    # Reverse the digits to get the correct representation
    return ''.join(reversed(base_n_digits))


def find_smallest_base(total_sum: int) -> int:
    """
    Find the smallest base that can represent the sum in at most 4 characters.

    Args:
    total_sum (int): The sum of numbers in base-10

    Returns:
    int: The smallest base that can represent the sum in at most 4 characters
    """

    # Binary search approach is more efficient here
    left, right = 2, 100000
    while left < right:
        mid = (left + right) // 2
        base_representation = convert_to_base_n(total_sum, mid)

        if len(base_representation) <= 4:
            right = mid
        else:
            left = mid + 1

    return left


def part_one(data: list) -> int:
    largest_number = 0
    for line in data:
        number_str, base_str = line.strip().split()
        base = int(base_str)

        # Convert o base-10
        largest_number = max(largest_number,
                             convert_to_base_10(number_str, base))

    return largest_number


def part_two(data: list) -> str:
    total_sum = 0
    for line in data:
        # Split the line into number and base
        number_str, base_str = line.strip().split()
        base = int(base_str)

        # Convert to base-10 and add total sum
        total_sum += convert_to_base_10(number_str, base)

    # Convert the sum to base-68
    return convert_to_base_68(total_sum)


def part_three(data: list) -> int:
    total_sum = 0
    for line in data:
        number_str, base_str = line.strip().split()
        base = int(base_str)

        # Convert to base-10 and to total_sum
        total_sum += convert_to_base_10(number_str, base)

    return find_smallest_base(total_sum)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 9982496560111
    print("Part 2:", part_two(data))    # 5#OvFQMnT
    print("Part 3:", part_three(data))  # 7221
