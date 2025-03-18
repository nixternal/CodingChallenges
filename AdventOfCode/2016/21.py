#!/usr/bin/env python

import re


def read_puzzle_input() -> list:
    with open("21.in", "r") as file:
        return file.read().splitlines()


def swap_position(s, x, y):
    """
    Swaps the characters at positions x and y in the string s.

    Args:
        s (str): The input string.
        x (int): The first position.
        y (int): The second position.

    Returns:
        str: The string after swapping the characters.
    """

    s = list(s)
    s[x], s[y] = s[y], s[x]
    return ''.join(s)


def swap_letter(s, x, y):
    """
    Swaps all occurrences of letter x with letter y in the string s.

    Args:
        s (str): The input string.
        x (str): The first letter.
        y (str): The second letter.

    Returns:
        str: The modified string with letters swapped.
    """

    return s.replace(x, '#').replace(y, x).replace('#', y)


def rotate_left(s, x):
    """
    Rotates the string left by x positions.

    Args:
        s (str): The input string.
        x (int): The number of positions to rotate.

    Returns:
        str: The rotated string.
    """

    x %= len(s)
    return s[x:] + s[:x]


def rotate_right(s, x):
    """
    Rotates the string right by x positions.

    Args:
        s (str): The input string.
        x (int): The number of positions to rotate.

    Returns:
        str: The rotated string.
    """

    x %= len(s)
    return s[-x:] + s[:-x]


def rotate_based_on_position(s, x):
    """
    Rotates the string right based on the position of letter x.

    The rotation amount is determined as:
        1 + index of x + (1 if index >= 4 else 0).

    Args:
        s (str): The input string.
        x (str): The letter whose position is used for rotation.

    Returns:
        str: The rotated string.
    """

    idx = s.index(x)
    rotations = 1 + idx + (1 if idx >= 4 else 0)
    return rotate_right(s, rotations)


def reverse_positions(s, x, y):
    """
    Reverses the substring between positions x and y (inclusive).

    Args:
        s (str): The input string.
        x (int): The start position.
        y (int): The end position.

    Returns:
        str: The modified string with the specified substring reversed.
    """

    return s[:x] + s[x:y+1][::-1] + s[y+1:]


def move_position(s, x, y):
    """
    Moves the character at position x to position y.

    Args:
        s (str): The input string.
        x (int): The original position.
        y (int): The new position.

    Returns:
        str: The modified string after the move.
    """

    s = list(s)
    char = s.pop(x)
    s.insert(y, char)
    return ''.join(s)


def scramble(s, instructions):
    """
    Scrambles the input string based on the given set of instructions.

    Args:
        s (str): The initial string.
        instructions (list): A list of string instructions.

    Returns:
        str: The scrambled string.
    """

    for instr in instructions:
        if m := re.match(r"swap position (\d+) with position (\d+)", instr):
            x, y = map(int, m.groups())
            s = swap_position(s, x, y)
        elif m := re.match(r"swap letter (\w) with letter (\w)", instr):
            x, y = m.groups()
            s = swap_letter(s, x, y)
        elif m := re.match(r"rotate left (\d+) steps?", instr):
            x = int(m.group(1))
            s = rotate_left(s, x)
        elif m := re.match(r"rotate right (\d+) steps?", instr):
            x = int(m.group(1))
            s = rotate_right(s, x)
        elif m := re.match(r"rotate based on position of letter (\w)", instr):
            x = m.group(1)
            s = rotate_based_on_position(s, x)
        elif m := re.match(r"reverse positions (\d+) through (\d+)", instr):
            x, y = map(int, m.groups())
            s = reverse_positions(s, x, y)
        elif m := re.match(r"move position (\d+) to position (\d+)", instr):
            x, y = map(int, m.groups())
            s = move_position(s, x, y)
    return s


def rotate_based_on_position_reverse(s, x):
    """
    Reverses the 'rotate based on position of letter' operation.

    Since the original operation is complex, this function brute-forces all
    possible original positions and finds which one would lead to the given
    scrambled string.

    Args:
        s (str): The scrambled string.
        x (str): The letter that was used for the rotation.

    Returns:
        str: The original string before the rotation.
    """

    for i in range(len(s)):
        test = rotate_left(s, i)
        if rotate_based_on_position(test, x) == s:
            return test
    raise ValueError("Rotation reversal failed!")


def unscramble(s, instructions):
    """
    Unscrambles the input string by reversing each operation in reverse order.

    Args:
        s (str): The scrambled string.
        instructions (list): A list of string instructions.

    Returns:
        str: The original unscrambled string.
    """

    for instr in reversed(instructions):
        if m := re.match(r"swap position (\d+) with position (\d+)", instr):
            x, y = map(int, m.groups())
            s = swap_position(s, x, y)
        elif m := re.match(r"swap letter (\w) with letter (\w)", instr):
            x, y = m.groups()
            s = swap_letter(s, x, y)
        elif m := re.match(r"rotate left (\d+) steps?", instr):
            x = int(m.group(1))
            s = rotate_right(s, x)
        elif m := re.match(r"rotate right (\d+) steps?", instr):
            x = int(m.group(1))
            s = rotate_left(s, x)
        elif m := re.match(r"rotate based on position of letter (\w)", instr):
            x = m.group(1)
            s = rotate_based_on_position_reverse(s, x)
        elif m := re.match(r"reverse positions (\d+) through (\d+)", instr):
            x, y = map(int, m.groups())
            s = reverse_positions(s, x, y)
        elif m := re.match(r"move position (\d+) to position (\d+)", instr):
            x, y = map(int, m.groups())
            s = move_position(s, y, x)
    return s


def part_one(data: list) -> str:
    return scramble('abcdefgh', data)


def part_two(data: list) -> str:
    return unscramble('fbgdceah', data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # bdfhgeca
    print("Part 2:", part_two(data))  # gdfcabeh
