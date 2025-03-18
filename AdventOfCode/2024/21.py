#!/usr/bin/env python

from functools import cache

# Global variables for storing keypad functions
NUMERIC = None
DIRECTIONAL = None


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file named '21.in' and returns a list of
    strings.

    Returns:
        list: Lines of input from the file as a list of strings.
    """

    with open("21.in", "r") as file:
        return file.read().splitlines()


def create_keypad(keys, row, col=0):
    """
    Creates a function to simulate key presses on a custom keypad layout.

    Args:
        keys (str): A string representing the keys on the keypad in row-major
                    order.
        row (int): The designated row of the keypad where row-specific rules
                   apply.
        col (int): The designated column of the keypad where column-specific
                   rules apply.

    Returns:
        function: A function that calculates the sequence of moves to press a
                  target key from a current key.
    """

    def press(cur, tgt):
        """
        Calculates the moves required to press the target key from the
        current key.

        Args:
            cur (str): The current key.
            tgt (str): The target key.

        Returns:
            str: The sequence of moves ('<', '>', '^', 'v') to navigate to
                 the target key.
        """

        cur_pos = keys.index(cur)
        tgt_pos = keys.index(tgt)
        r_diff = (tgt_pos // 3) - (cur_pos // 3)  # Row Difference
        c_diff = (tgt_pos % 3) - (cur_pos % 3)    # Column Difference

        c_move = "<>"[c_diff > 0] * abs(c_diff)   # Horizontal Moves
        r_move = "^v"[r_diff > 0] * abs(r_diff)   # Vertical Moves

        if tgt_pos // 3 == row and cur_pos % 3 == col:
            return c_move + r_move
        elif cur_pos // 3 == row and tgt_pos % 3 == col:
            return r_move + c_move
        else:
            if "<" in c_move:
                return c_move + r_move
            else:
                return r_move + c_move
    return press


def press_keypads_recursive(code, key_funcs):
    """
    Calculates the total number of presses needed to input a code recursively
    through a chain of keypads.

    Args:
        code (str): The code to input.
        key_funcs (list): A list of keypad functions to navigate through.

    Returns:
        int: The total number of presses required.
    """

    levels = len(key_funcs) - 1

    @cache
    def num_presses(cur, tgt, lvl):
        """
        Recursively calculates the presses needed to transition between keys
        at a given level of the keypad chain.

        Args:
            cur (str): The current key.
            tgt (str): The target key.
            lvl (int): The current level in the keypad chain.

        Returns:
            int: The number of presses required.
        """

        seq = key_funcs[lvl](cur, tgt) + "A"
        if lvl == levels:
            return len(seq)
        else:
            length = 0
            c = "A"
            for t in seq:
                length += num_presses(c, t, lvl + 1)
                c = t
            return length

    length = 0
    cur = "A"
    for tgt in code:
        length += num_presses(cur, tgt, 0)
        cur = tgt
    return length


def main(data: list, nchain: int) -> int:
    """
    Processes the puzzle input and calculates the total complexity based on
    the keypad chain and input codes.

    Args:
        data (list): List of input codes as strings.
        nchain (int): The number of directional keypads in the chain.

    Returns:
        int: The total complexity of the input.
    """

    keypad_chain = [NUMERIC] + [DIRECTIONAL] * nchain
    complexity = 0
    for code in data:
        seq_length = press_keypads_recursive(code, keypad_chain)
        numeric_code = int("".join(c for c in code if c.isnumeric()))
        complexity += seq_length * numeric_code
    return complexity


if __name__ == "__main__":
    # Initialize keypad functions
    NUMERIC = create_keypad("789456123_0A", 3)
    DIRECTIONAL = create_keypad("_^A<v>", 0)

    # Read puzzle input
    data = read_puzzle_input()

    # Calculate and print results for Part 1 & Part 2
    print("Part 1:", main(data, 2))   # 157892
    print("Part 2:", main(data, 25))  # 197015606336332
