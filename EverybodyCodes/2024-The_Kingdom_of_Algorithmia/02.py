#!/usr/bin/env python
"""
Word search puzzle solver with three parts:
1. Count word occurrences in a sentence
2. Find horizontal word matches in lines lines
3. Find vertical and horizontal (wrapped) word matches in 2D lines
"""


def read_puzzle_input() -> list[str]:
    """Read puzzle input file and split into sections."""
    with open("02.in", "r") as file:
        return file.read().split("\n\n")


def parse_words(section: str) -> list[str]:
    """Extract words from 'WORDS:word1,word2,...' format."""
    return section.split(":", 1)[1].split(",")


def add_reversed_words(words: list[str]) -> list[str]:
    """Return list with reversed words added (avoiding duplicates)."""
    word_set = set(words)
    for word in words:
        word_set.add(word[::-1])
    return list(word_set)


def part_one(data: list[str]) -> int:
    """Count total occurrences of all words in sentence."""
    words = parse_words(data[0])
    sentence = data[1]

    return sum(sentence.count(word) for word in words)


def part_two(data: list[str]) -> int:
    """
    Count unique character positions covered by horizontal word matches.
    Searches forward and backward for each word in each line.
    """
    words = add_reversed_words(parse_words(data[2]))
    lines = data[3].splitlines()

    total_positions = 0

    for line in lines:
        # Track which positions are covered by any word match
        covered = set()

        for word in words:
            word_len = len(word)
            # Find all occurrences of this word in the line
            for start_pos in range(len(line) - word_len + 1):
                if line[start_pos : start_pos + word_len] == word:
                    # Mark all positions in this match as covered
                    covered.update(range(start_pos, start_pos + word_len))

        total_positions += len(covered)

    return total_positions


def part_three(data: list[str]) -> int:
    """
    Count unique lines positions covered by word matches.
        - Vertical matches: top to bottom (no wrapping)
        - Horizontal matches: left to right (with wrapping)
    Searches both forward and backward for each word.
    """
    words = add_reversed_words(parse_words(data[4]))
    lines = data[5].splitlines()

    height = len(lines)
    width = len(lines[0])

    covered_positions = set()

    for row in range(height):
        for col in range(width):
            for word in words:
                word_len = len(word)

                # Check vertical match (top → bottom, no wrapping)
                if row + word_len <= height:
                    if all(lines[row + i][col] == word[i] for i in range(word_len)):
                        covered_positions.update(
                            (row + i, col) for i in range(word_len)
                        )

                # Check horizontal match (left → right, with wrapping)
                if all(
                    lines[row][(col + i) % width] == word[i] for i in range(word_len)
                ):
                    covered_positions.update(
                        (row, (col + i) % width) for i in range(word_len)
                    )

    return len(covered_positions)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 29
    print("Part 2:", part_two(data))  # 5220
    print("Part 3:", part_three(data))  # 12048
