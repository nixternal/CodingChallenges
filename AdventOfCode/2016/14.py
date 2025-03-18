#!/usr/bin/env python

import hashlib
from typing import Dict, List, Optional


def generate_hash(salt: str, index: int, stretch: int = 0, cache: Optional[Dict[int, str]] = None) -> str:
    """
    Generates an MD5 hash for the given salt and index, optionally with key
    stretching.

    Args:
        salt (str): The salt used to generate the hash.
        index (int): The index to append to the salt before hashing.
        stretch (int, optional): The number of additional hash iterations
                                 (key stretching). Defaults to 0.
        cache (Optional[Dict[int, str]], optional): A dictionary to cache
                                                    previously computed hashes.
                                                    Defaults to None.

    Returns:
        str: The computed MD5 hash as a hexadecimal string.

    Description:
        This function computes the MD5 hash of the string formed by
        concatenating the salt and the index. If key stretching is enabled
        (stretch > 0), the hash is rehashed multiple times. The result is
        cached in the provided dictionary to avoid redundant computations.
    """

    if cache is not None and index in cache:
        return cache[index]

    # Concatenate the salt and index, then compute the hash
    hash_str = salt + str(index)
    for _ in range(stretch + 1):
        hash_str = hashlib.md5(hash_str.encode()).hexdigest()

    # Cache the computed hash for future use
    if cache is not None:
        cache[index] = hash_str

    return hash_str


def find_triplet(hash_str: str) -> Optional[str]:
    """
    Finds the first triplet (three of the same character in a row) in the hash.

    Args:
        hash_str (str): The hash string to search for a triplet.

    Returns:
        Optional[str]: The character that forms the triplet, or None if no
                       triplet is found.

    Description:
        This function scans the hash string for the first occurrence of three
        identical consecutive characters. If found, it returns the character;
        otherwise, it returns None.
    """

    for i in range(len(hash_str) - 2):
        if hash_str[i] == hash_str[i + 1] == hash_str[i + 2]:
            return hash_str[i]
    return None


def has_quintuplet(hash_str: str, char: str) -> bool:
    """
    Checks if the hash contains a quintuplet (five of the same character in a
    row) for the given character.

    Args:
        hash_str (str): The hash string to search for a quintuplet.
        char (str): The character to check for a quintuplet.

    Returns:
        bool: True if the hash contains a quintuplet of the given character,
              otherwise False.

    Description:
        This function checks if the hash string contains five consecutive
        occurrences of the specified character.
    """

    return char * 5 in hash_str


def find_keys(salt: str, stretch: int = 0) -> int:
    """
    Finds the indices of the first 64 keys that meet the criteria.

    Args:
        salt (str): The salt used to generate the hashes.
        stretch (int, optional): The number of additional hash iterations
                                 (key stretching). Defaults to 0.

    Returns:
        List[int]: A list of indices that correspond to valid keys.

    Description:
        This function identifies the first 64 keys by:
        1. Generating MD5 hashes for the salt and successive indices.
        2. Checking each hash for a triplet (three identical consecutive
           characters).
        3. If a triplet is found, checking the next 1000 hashes for a
           quintuplet of the same character.
        4. If a quintuplet is found, the index is added to the list of keys.
        5. The process continues until 64 keys are found.

        A cache is used to store computed hashes, avoiding redundant
        computations and improving performance.
    """

    keys: List[int] = []  # List to store the indices of valid keys
    index = 0  # Current index being checked
    has_cache: Dict[int, str] = {}  # Cache to store computed hashes

    while len(keys) < 64:
        # Generate the hash for the current index, using the cache to avoid
        # recomputation
        hash_str = generate_hash(salt, index, stretch, has_cache)

        # Check if the hash contains a triplet
        triplet_char = find_triplet(hash_str)
        if triplet_char:
            # If a triplet is found, check the next 1000 hashes for a
            # quintuplet of the same character
            for i in range(1, 1001):
                next_hash = generate_hash(salt, index + i, stretch, has_cache)
                if has_quintuplet(next_hash, triplet_char):
                    # If a quintuplet is found, add the index to list of keys
                    keys.append(index)
                    break

        # Move to the next index
        index += 1

    return keys[63]


def part_one(salt: str) -> int:
    return find_keys(salt)


def part_two(salt: str) -> int:
    return find_keys(salt, stretch=2016)


if __name__ == "__main__":
    salt = 'zpqevtbw'
    print("Part 1:", part_one(salt))  # 16106
    print("Part 2:", part_two(salt))  # 22423
