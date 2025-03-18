#!/usr/bin/env python

import re

# The alphabet for generating patterns and performing string operations
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# Generate a list of all consecutive triples in the alphabet
# (e.g., "abc", "bcd", etc.)
TRIPLES = [''.join(triple) for triple in zip(ALPHABET, ALPHABET[1:],
                                             ALPHABET[2:])]

# Compile a regular expression to match any of these triples
TRIPLES_REGEX = re.compile('|'.join(TRIPLES))


def increment_string(s: str) -> str:
    """
    Increment a string to its next lexicographical value, treating it as a
    base-26 number where 'a' to 'z' are the digits.

    Args:
        s (str): The input string to increment.

    Returns:
        str: The incremented string.
    """

    s_list = list(s)  # Convert string to a list of characters for mutation
    i = len(s_list) - 1  # Start from the last character

    while i >= 0:
        if s_list[i] == 'z':  # Handle rollover: 'z' becomes 'a'
            s_list[i] = 'a'
            i -= 1  # Move to the next character to the left
        else:
            s_list[i] = chr(ord(s_list[i]) + 1)  # Increment the character
            break  # Exit the loop once incremented

    return ''.join(s_list)  # Convert back to a string


def new_password(password: str) -> str:
    """
    Generate the next valid password according to the following rules:
        1. Must include at least one increasing straight of three consecutive
           letters (e.g., "abc", "bcd").
        2. Must not contain the letters 'i', 'o', or 'l'.
        3. Must contain at least two different, non-overlapping pairs of
           characters (e.g., "aa" and "bb").

    Args:
        password (str): The current password.

    Returns:
        str: The next valid password.
    """

    while True:
        password = increment_string(password)  # Increment the password
        if (TRIPLES_REGEX.search(password) and  # Check for a valid triple
                not re.search(r'[iol]', password) and  # Exclude 'i, o, and l'
                len(re.findall(r'(.)\1', password)) > 1):  # Check for 2 pairs
            break  # Exit loop once a valid password is found

    return password


if __name__ == '__main__':
    print("Part 1:", new_password('vzbxkghb'))  # vzbxxyzz
    print("Part 2:", new_password('vzbxxyzz'))  # vzcaabcc
