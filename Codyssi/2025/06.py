#!/usr/bin/env python

"""
Character Value Puzzle Solver

This script solves a three-part puzzle involving character values:
1. Count alphabetic characters in the input
2. Sum the values of alphabetic characters (a-z: 1-26, A-Z: 27-52)
3. Repair corrupted characters and calculate the sum of all values

The character values are defined as:
- Lowercase letters (a-z): 1-26 (a=1, b=2, ..., z=26)
- Uppercase letters (A-Z): 27-52 (A=27, B=28, ..., Z=52)
- Corrupted characters: calculated using the formula 2*previous_value - 5
  (adjusted to stay within range 1-52)
"""


def read_puzzle_input() -> str:
    """
    Read the puzzle input from a file.

    Returns:
        str: The content of the file with whitespace trimmed
    """

    with open("06.in", "r") as file:
        return file.read().strip()


def get_char_value(char: str) -> int:
    """
    Calculate the value of a character based on its position in the alphabet.

    Args:
        char (str): A single character

    Returns:
        int: The value of the character (1-52) or None if not a letter

    Examples:
        >>> get_char_value('a')
        1
        >>> get_char_value('z')
        26
        >>> get_char_value('A')
        27
        >>> get_char_value('Z')
        52
        >>> get_char_value('3')
        None
    """

    if char.islower():
        return ord(char) - 96  # 'a' is ASCII 97, so a=1, b=2, etc.
    elif char.isupper():
        return ord(char) - 38  # 'A' is ASCII 65, so A=27, B=28, etc.
    return 0


def fix_corrupted_char(preceding_val) -> int:
    """
    Fix a corrupted character value using the formula: 2*previous_value - 5.
    Adjusts the result to stay within the range 1-52.

    Args:
        preceding_val (int): The value of the preceding character

    Returns:
        int: The fixed value of the corrupted character

    Examples:
        >>> fix_corrupted_char(10)  # 2*10 - 5 = 15
        15
        >>> fix_corrupted_char(2)   # 2*2 - 5 = -1, adjusted to 51
        51
        >>> fix_corrupted_char(30)  # 2*30 - 5 = 55, adjusted to 3
        3
    """

    # Apply corruption repair formula
    value = preceding_val * 2 - 5

    # Adjust value to stay within range 1-52 (wrapping around if necessary)
    while value < 1:
        value += 52

    while value > 52:
        value -= 52

    return value


def part_one(data: str) -> int:
    """
    Part 1: Count the number of alphabetic characters in the input.

    Args:
        data (str): The puzzle input

    Returns:
        int: The count of alphabetic characters
    """

    return sum(1 for char in data if char.isalpha())


def part_two(data: str) -> int:
    """
    Part 2: Calculate the sum of character values for all alphabetic characters

    Args:
        data (str): The puzzle input

    Returns:
        int: The sum of all character values
    """

    return sum(get_char_value(char) for char in data if char.isalpha())


def part_three(data: str) -> int:
    """
    Part 3: Calculate the sum of values after fixing corrupted characters.

    For each non-alphabetic character, use the formula 2*previous_value - 5
    to determine its value, adjusting to stay within range 1-52.

    Args:
        data (str): The puzzle input

    Returns:
        int: The sum of all character values after fixing corrupted characters
    """

    values = []

    for i, char in enumerate(data):
        value = get_char_value(char)

        if value > 0:
            # Regular alphabetic character
            values.append(value)
        else:
            # Corrupted character
            if i > 0 and values:
                # Fix based on the previous character's value
                preceding_value = values[i - 1]
                fixed_value = fix_corrupted_char(preceding_value)
                values.append(fixed_value)
            else:
                # If it is the 1st character & corrupted, default to 0
                values.append(0)

    return sum(values)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 1317
    print("Part 2:", part_two(data))    # 35203
    print("Part 3:", part_three(data))  # 52740
