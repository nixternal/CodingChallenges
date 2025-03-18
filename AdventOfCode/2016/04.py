#!/usr/bin/env python

import re
from collections import Counter


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns it as a list of strings.

    Returns:
        list: A list of strings, where each string represents a line from the
              input file.
    """
    with open("04.in", "r") as file:
        return file.read().splitlines()


def is_valid_room(name: str, checksum: str) -> bool:
    """
    Validates a room name based on its checksum.

    The room name is valid if the checksum matches the five most common
    letters in the name, with ties broken by alphabetical order.

    Args:
        name (str): The room name, including dashes.
        checksum (str): The checksum to validate against.

    Returns:
        bool: True if the room is valid, False otherwise.
    """
    # Remove the dashes and count the letter frequencies
    letters = name.replace('-', '')
    counter = Counter(letters)

    # Sort by frequency (descending) and then alphabetically
    sorted_letters = sorted(counter.keys(), key=lambda x: (-counter[x], x))

    # Generate the expected checksum
    expected_checksum = ''.join(sorted_letters[:5])

    # Compare with the given checksum & return true or false
    return expected_checksum == checksum


def decrypt_room_info(data: list) -> list:
    """
    Parses the input data into a structured format for room information.

    Each line of input is expected to contain a room name, sector ID, and
    checksum. This function extracts these components using a regular
    expression.

    Args:
        data (list): A list of strings, where each string represents a line
                     from the input file.

    Returns:
        list: A list of lists, where each inner list contains
              [name, sector_id, checksum].
    """
    room_info = []
    for line in data:
        # Use regex to extract name, sector ID, and checksum
        match = re.match(r'([a-z-]+)-(\d+)\[([a-z]+)\]', line)
        if not match:
            continue

        name, sector_id, checksum = match.groups()
        room_info.append([name, sector_id, checksum])

    return room_info


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle: Sums the sector IDs of all valid rooms.

    A room is valid if its checksum matches the five most common letters in
    its name, with ties broken by alphabetical order.

    Args:
        data (list): A list of strings, where each string represents a line
                     from the input file.

    Returns:
        int: The sum of sector IDs for all valid rooms.
    """
    total = 0
    room_info = decrypt_room_info(data)
    for i in range(len(room_info)):
        if is_valid_room(room_info[i][0], room_info[i][2]):
            total += int(room_info[i][1])

    return total


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle: Finds the sector ID of the room containing
    "northpole" in its decrypted name.

    The room name is decrypted using a Caesar cipher (shift cipher), where
    each letter is shifted forward in the alphabet by the sector ID number.
    Dashes are replaced with spaces.

    Args:
        data (list): A list of strings, where each string represents a line
                     from the input file.

    Returns:
        int: The sector ID of the room containing "northpole" in its
             decrypted name, or 0 if not found.
    """
    room_info = decrypt_room_info(data)
    for i in range(len(room_info)):
        if is_valid_room(room_info[i][0], room_info[i][2]):
            decrypted = ''
            for char in room_info[i][0]:
                if char == '-':
                    decrypted += ' '
                else:
                    # Shift char by sector_id positions using Caesar cipher
                    shifted_char = chr(
                        ((ord(char) - ord('a') + int(room_info[i][1])) % 26)
                        + ord('a')
                    )
                    decrypted += shifted_char

            # Check if the decrypted name contains "northpole"
            if 'northpole' in decrypted:
                return int(room_info[i][1])
    return 0


if __name__ == "__main__":
    # Read the puzzle input
    data = read_puzzle_input()

    # Solve and print Part 1
    print("Part 1:", part_one(data))  # Expected output: 137896

    # Solve and print Part 2
    print("Part 2:", part_two(data))  # Expected output: 501
