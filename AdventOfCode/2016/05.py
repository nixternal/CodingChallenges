#!/usr/bin/env python

import hashlib

DOOR_ID = b'abbhdwsy'


def part_one() -> str:
    """
    Solves Part 1 of the problem:
    Finds an 8-character password by generating MD5 hashes of the form
    `DOOR_ID + i` and checking if the hash starts with five zeros ('00000').
    The 6th character of such a hash is appended to the password.

    Returns:
        str: The 8-character password.
    """

    # Use a list to collect password characters
    passwd = []

    # Start with 0 and increment until the password is complete
    i = 0

    while len(passwd) < 8:
        # Create the input string by concatenating DOOR_ID and the current
        # integer i
        input_str = DOOR_ID + str(i).encode('utf-8')

        # Compute the MD5 hash of the input string and get its hexadecimal
        # representation
        md5sum = hashlib.md5(input_str).hexdigest()

        # Check if the hash starts with '00000' (5 zeros)
        if md5sum.startswith('00000'):
            passwd.append(md5sum[5])  # Append the 6th character of the hash
        i += 1

    return ''.join(passwd)


def part_two() -> str:
    """
    Solves Part 2 of the problem:
    Finds an 8-character password by generating MD5 hashes of the form
    `DOOR_ID + i` and checking if the hash starts with five zeros ('00000').
    The 6th character of the hash represents the position in the password, and
    the 7th character is the character to place at that position. The password
    is complete when all positions are filled.

    Returns:
        str: The 8-character password.
    """

    passwd = ['.'] * 8
    i = 0

    while '.' in passwd:
        input_str = DOOR_ID + str(i).encode('utf-8')
        md5sum = hashlib.md5(input_str).hexdigest()

        if md5sum.startswith('00000'):
            pos = md5sum[5]
            if pos.isdigit() and 0 <= int(pos) < 8 and passwd[int(pos)] == '.':
                passwd[int(pos)] = md5sum[6]
        i += 1

    return ''.join(passwd)


if __name__ == "__main__":
    print("Part 1:", part_one())  # 801b56a7
    print("Part 2:", part_two())  # 424a0197
