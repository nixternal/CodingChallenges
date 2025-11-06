#!/usr/bin/env python
"""Advent of Code Day 4: Giant Squid (Bingo)"""


def read_puzzle_input() -> tuple[list[int], list[list[list[int]]]]:
    """Read draws and bingo boards from input file."""
    with open("04.in", "r") as file:
        sections = file.read().strip().split("\n\n")

    draws = [int(x) for x in sections[0].split(",")]
    boards = [
        [[int(n) for n in line.split()] for line in block.splitlines()]
        for block in sections[1:]
    ]

    return draws, boards


def mark_number(board: list[list[int | None]], num: int) -> None:
    """Mark a number on the board by replacing it with None."""
    for row in board:
        for i, val in enumerate(row):
            if val == num:
                row[i] = None


def is_winner(board: list[list[int | None]]) -> bool:
    """Check if board has a winning row or column."""
    # Check rows
    if any(all(cell is None for cell in row) for row in board):
        return True

    # Check columns
    if any(all(board[r][c] is None for r in range(5)) for c in range(5)):
        return True

    return False


def unmarked_sum(board: list[list[int | None]]) -> int:
    """Calculate sum of all unmarked numbers on the board."""
    return sum(cell for row in board for cell in row if cell is not None)


def play_bingo(draws: list[int], boards: list[list[list[int | None]]], find_last: bool = False) -> int:
    """
    Play bingo and return the winning score.

    Args:
        draws: List of numbers to draw
        boards: List of bingo boards
        find_last: If True, return score of last winning board; if False, return first winner

    Returns:
        Winning score (unmarked sum * winning number)
    """
    won_boards = set()
    last_score = 0

    for num in draws:
        for board_idx, board in enumerate(boards):
            if board_idx in won_boards:
                continue

            mark_number(board, num)

            if is_winner(board):
                score = unmarked_sum(board) * num
                won_boards.add(board_idx)
                last_score = score

                if not find_last:
                    return score

    return last_score


def deep_copy_boards(boards: list[list[list[int]]]) -> list[list[list[int | None]]]:
    """Create a deep copy of all boards."""
    return [[[cell for cell in row] for row in board] for board in boards]


def part_one(draws: list[int], boards: list[list[list[int]]]) -> int:
    """Find the score of the first winning board."""
    return play_bingo(draws, deep_copy_boards(boards), find_last=False)


def part_two(draws: list[int], boards: list[list[list[int]]]) -> int:
    """Find the score of the last winning board."""
    return play_bingo(draws, deep_copy_boards(boards), find_last=True)


if __name__ == "__main__":
    draws, boards = read_puzzle_input()
    print("Part 1:", part_one(draws, boards))  # 25410
    print("Part 2:", part_two(draws, boards))  # 2730
