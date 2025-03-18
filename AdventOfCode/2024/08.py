#!/usr/bin/env python


def read_puzzle_input() -> list:
    """
    Reads the input data from a file named `input.txt` located in the parent
    directory of the current script.

    Returns:
        list: A list of strings where each string represents a line from the
              input file.
    """

    with open("08.py", "r") as file:
        return file.read().splitlines()


def parse_antennas(data: list) -> dict:
    """
    Parses the grid and identifies all antennas and their positions.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        dict: A dictionary where keys are antenna types and values are lists
              of (row, col) coordinates.
    """

    antennas = {}
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char != ".":
                antennas.setdefault(char, []).append((r, c))
    return antennas


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle by identifying unique "antinodes" generated
    by the reflection of antennas on a grid.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: The number of unique valid antinodes within the grid.
    """

    # Original Code - https://www.youtube.com/watch?v=HI2DbMq-t-Y assisted
    # rows = len(data)
    # cols = len(data[0])

    # antennas = {}

    # for r, row in enumerate(data):
    #     for c, char in enumerate(row):
    #         if char != ".":
    #             if char not in antennas:
    #                 antennas[char] = []
    #             antennas[char].append((r, c))

    # antinodes = set()

    # for coords in antennas.values():
    #     for i in range(len(coords)):
    #         for j in range(i + 1, len(coords)):
    #             r1, c1 = coords[i]
    #             r2, c2 = coords[j]
    #             antinodes.add((2 * r1 - r2, 2 * c1 - c2))
    #             antinodes.add((2 * r2 - r1, 2 * c2 - c1))

    # return len([0 for r, c in antinodes if 0 <= r < rows and 0 <= c < cols])

    # ChatGPT Optimized version of above code (parse_antennas() function added)
    rows, cols = len(data), len(data[0])
    antennas = parse_antennas(data)
    antinodes = set()

    # Compute antinodes for each pair of antennas
    for coords in antennas.values():
        for i in range(len(coords)):
            r1, c1 = coords[i]
            for j in range(i + 1, len(coords)):
                r2, c2 = coords[j]
                # Add both reflected points
                antinodes.update({
                    (2 * r1 - r2, 2 * c1 - c2),
                    (2 * r2 - r1, 2 * c2 - c1),
                })

    # Count antinodes within grid boundaries
    return sum(0 <= r < rows and 0 <= c < cols for r, c in antinodes)


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle by tracing rays originating from antennas in
    all directions.

    Args:
        data (list): A list of strings representing the grid.

    Returns:
        int: The number of unique valid antinodes (ray intersections) within
             the grid.
    """

    # Original Code - https://www.youtube.com/watch?v=HI2DbMq-t-Y assisted
    # rows = len(data)
    # cols = len(data[0])

    # antennas = {}

    # for r, row in enumerate(data):
    #     for c, char in enumerate(row):
    #         if char != ".":
    #             if char not in antennas:
    #                 antennas[char] = []
    #             antennas[char].append((r, c))

    # antinodes = set()

    # for coords in antennas.values():
    #     for i in range(len(coords)):
    #         for j in range(len(coords)):
    #             if i == j:
    #                 continue
    #             r1, c1 = coords[i]
    #             r2, c2 = coords[j]
    #             dr = r2 - r1
    #             dc = c2 - c1
    #             r = r1
    #             c = c1
    #             while 0 <= r < rows and 0 <= c < cols:
    #                 antinodes.add((r, c))
    #                 r += dr
    #                 c += dc

    # return len([0 for r, c in antinodes if 0 <= r < rows and 0 <= c < cols])

    # ChatGPT Optimized version of above code (parse_antennas() function added)
    rows, cols = len(data), len(data[0])
    antennas = parse_antennas(data)

    antinodes = set()

    # Trace rays between each pair of antennas of the same type
    for coords in antennas.values():
        for r1, c1 in coords:
            for r2, c2 in coords:
                if (r1, c1) == (r2, c2):
                    continue
                # Deltas
                dr, dc = r2 - r1, c2 - c1
                r, c = r1, c1

                # Follow the ray while within the grid
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r += dr
                    c += dc

    # Count unique valid antinodes within grid boundaries
    return len(antinodes)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 240
    print("Part 2:", part_two(data))  # 955
