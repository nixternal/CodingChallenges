#!/usr/bin/env python

"""
Marble Game Simulator

This program simulates an elf marble game where:
- Players arrange themselves in a circle
- Each player gets a turn in sequence, starting with player 1
- Initially, there's one marble (labeled 0) in the circle
- On each turn, a player:
  a) Adds a new marble with the next sequential number
  b) Places it according to specific rules:
     - If the marble number is a multiple of 23:
       * The player keeps this marble
       * The player also removes the marble 7 positions counterclockwise
       * The player adds both marble values to their score
     - Otherwise:
       * Places the new marble 2 positions clockwise from the current position
- The game ends after the last marble is played

The program calculates the winning score (highest score among all players).
"""

from collections import deque


def play_marble_game(num_players: int, last_marble: int) -> int:
    """
    Simulate the marble game and return the highest score.

    Args:
        num_players: Number of players in the game
        last_marble: Number of the last marble to be played

    Returns:
        The highest score achieved by any player
    """

    # Optimization: Pre-allocate scores array with zeros
    scores = [0] * num_players
    # Use deque for O(1) rotations and append/pop operations
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            # Special rule for multiples of 23
            # Rotate 7 positions counterclockwise
            #    (equivalent to moving 7 positions left)
            circle.rotate(7)
            # Current player gets the special marble + the marble 7 positions
            # counterclockwise
            current_player = marble % num_players
            scores[current_player] += marble + circle.popleft()
        else:
            # Regular rule: place marble 2 positions clockwise
            # Rotate -2 is equivalent to moving 2 positions right
            circle.rotate(-2)
            circle.appendleft(marble)

    return max(scores)


def part_one(num_players: int, last_marble: int) -> int:
    """
    Solve part one of the problem.

    Args:
        num_players: Number of players in the game
        last_marble: Number of the last marble to be played

    Returns:
        The highest score with the standard rules
    """

    return play_marble_game(num_players, last_marble)


def part_two(num_players: int, last_marble: int) -> int:
    """
    Solve part two of the problem with 100x more marbles.

    Args:
        num_players: Number of players in the game
        last_marble: Base number of marbles before multiplying by 100

    Returns:
        The highest score with 100 times more marbles
    """

    return play_marble_game(num_players, last_marble * 100)


if __name__ == "__main__":
    players = 452
    last_marble = 71250
    print("Part 1:", part_one(players, last_marble))  # 388844
    print("Part 2:", part_two(players, last_marble))  # 3212081616
