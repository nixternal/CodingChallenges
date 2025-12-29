#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("04.in", "r") as file:
        return file.read().splitlines()


def parse_card(line: str) -> int:
    """Parse a scratchcard line and return the number of matches.

    Format: "Card N: winning_nums | your_nums"
    """
    parts = line.split()
    winning = set(parts[2:12])  # Numbers after "Card N:"
    yours = set(parts[13:])  # Numbers after the "|"
    return len(winning & yours)


def part_one(data: list) -> int:
    """Calculate total points. First match = 1 point, then doubles each match."""
    total = 0
    for line in data:
        matches = parse_card(line)
        if matches > 0:
            total += 2 ** (matches - 1)
    return total


def part_two(data: list) -> int:
    """Count total scratchcards after winning copies.

    Each card with N matches wins you copies of the next N cards.
    Process cards in order, tracking how many copies of each you have.
    """
    card_counts = [1] * len(data)  # Start with 1 copy of each card

    for i, line in enumerate(data):
        matches = parse_card(line)
        # Each copy of current card wins copies of the next 'matches' cards
        for j in range(i + 1, min(i + 1 + matches, len(data))):
            card_counts[j] += card_counts[i]

    return sum(card_counts)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 22897
    print("Part 2:", part_two(data))  # 5095824
