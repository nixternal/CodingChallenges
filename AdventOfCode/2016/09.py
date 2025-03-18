#!/usr/bin/env python


def read_puzzle_input() -> str:
    with open("09.in", "r") as file:
        return file.read().strip()


def decompress(compressed: str) -> int:
    """
    Decompresses a string using the compression format defined in the puzzle.

    This version handles recursive markers, meaning markers can appear within
    segments that are being repeated. Instead of building the decompressed
    string, it calculates the length of the fully decompressed string.

    Args:
        compressed (str): The compressed input string.

    Returns:
        int: The length of the fully decompressed string.
    """

    length = 0  # Tracks the total length of the decompressed string
    i = 0  # Index to traverse the compressed string

    while i < len(compressed):
        if compressed[i] == '(':
            # Marker found: extract the marker content
            marker_end = compressed.find(')', i)  # Find the end of the marker
            # Extract the marker (e.g., 'AxB')
            marker = compressed[i+1:marker_end]
            # Split into length and repeat values
            segment_length, repeat = map(int, marker.split('x'))

            # Move the index to the start of the segment to repeat
            i = marker_end + 1

            # Extract the segment and recursively decompress it
            segment = compressed[i:i+segment_length]
            # Add the decompressed length to the segment
            length += decompress(segment) * repeat

            # Move the index past the segment
            i += segment_length
        else:
            # Regular character: add 1 to the total length
            length += 1
            i += 1
    return length


def part_one(data: str) -> int:
    """
    Decompresses a string using the compression format defined in the puzzle.

    The compression format uses markers like (AxB), where:
    - A is the number of characters to repeat.
    - B is the number of times to repeat those characters.

    Args:
        compressed (str): The compressed input string.

    Returns:
        str: The fully decompressed string.
    """

    decompressed = []  # List to store decompressed characters.
    i = 0  # Index to traverse the compressed string

    while i < len(data):
        if data[i] == '(':
            # Marker found: extract the marker content (AxB)
            marker_end = data.find(')', i)  # Find the end of the marker
            marker = data[i+1:marker_end]  # Extract the marker (e.g., 'AxB')
            # Split into length and repeat values
            length, repeat = map(int, marker.split('x'))

            # Move the index to the start of the segment to repeat
            i = marker_end + 1

            # Extract the segment and repeat it
            segment = data[i:i+length]
            decompressed.append(segment * repeat)

            # Move the index past the segment
            i += length
        else:
            # Regular character: add it to the decompressed result
            decompressed.append(data[i])
            i += 1

    # Return the length of the combined list of characters
    return len(''.join(decompressed))


def part_two(data: str) -> int:
    return decompress(data)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 152851
    print("Part 2:", part_two(data))  # 11797310782
