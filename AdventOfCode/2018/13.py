#!/usr/bin/env python
"""
Advent of Code 2018 - Day 13: Mine Cart Madness
https://adventofcode.com/2018/day/13

Problem Summary:
- There's a network of train tracks with carts moving along them
- Carts move according to track direction, turning at curves and intersections
- Part 1: Find the location of the first cart collision
- Part 2: After all collisions, find the location of the last remaining cart

This solution simulates the movement of carts along tracks, handling
intersections, curves, and detecting collisions.
"""

import copy


def read_puzzle_input() -> tuple:
    """
    Reads the puzzle input and parses it into a track map and list of carts.

    Args:
        file_path: Path to the input file

    Returns:
        A tuple containing:
        - tracks: Dictionary mapping (x, y) coordinates to track pieces
                  ('|', '-', '/', '\\', '+')
        - carts: List of dictionaries containing cart information
                 (position, direction, etc.)
    """

    with open("13.in", "r") as file:
        input_data = file.read()

    tracks = {}  # Maps (x, y) coordinates to track pieces
    carts = []   # List of cart information dictionaries

    for y, line in enumerate(input_data.strip('\n').split('\n')):
        for x, char in enumerate(line):
            if char in '^v<>':
                # Found a cart, determine its direction & the track beneath it
                # Direction: 0=up, 1=right, 2=down, 3=left
                direction = {'^': 0, '>': 1, 'v': 2, '<': 3}[char]

                # Determine the track piece beneath the cart
                if char in '^v':
                    track_piece = '|'
                else:  # char in '<>'
                    track_piece = '-'

                # Add the cart and its information
                carts.append({
                    'x': x,
                    'y': y,
                    'direction': direction,  # Current direction of the cart
                    'turn': 0,               # Intersection turn state
                                             #   (0=left, 1=straight, 2=right)
                    'crashed': False         # Whether the cart has crashed
                })

                # Add the track piece to the tracks dictionary
                tracks[(x, y)] = track_piece
            elif char in '|-/\\+':
                # Add a track piece to the tracks dictionary
                tracks[(x, y)] = char

    return tracks, carts


def move_cart(cart: dict, tracks: dict) -> None:
    """
    Moves a cart according to track rules and updates its direction.

    Args:
        cart: Dictionary containing cart information
        tracks: Dictionary mapping coordinates to track pieces

    The function modifies the cart dictionary in-place, updating its position
    and direction.
    """

    # Movement vectors for each direction (up, right, down, left)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dx, dy = directions[cart['direction']]

    # Move the cart in its current direction
    cart['x'] += dx
    cart['y'] += dy

    # Get the current track piece at the cart's new position
    current_track = tracks.get((cart['x'], cart['y']), ' ')

    # Update the cart's direction based on the track piece
    if current_track == '+':
        # At an intersection, turn based on the cart's turn state
        if cart['turn'] == 0:
            # Turn left (counter-clockwise)
            cart['direction'] = (cart['direction'] - 1) % 4
        elif cart['turn'] == 2:
            # Turn right (clockwise)
            cart['direction'] = (cart['direction'] + 1) % 4
        # If turn state is 1, go straight (no direction change)

        # Update the turn state for the next intersection
        # (left -> straight -> right -> left...)
        cart['turn'] = (cart['turn'] + 1) % 3
    elif current_track == '/':
        # Different behavior depending on approach direction
        if cart['direction'] in [0, 2]:  # Up or Down
            cart['direction'] = (cart['direction'] + 1) % 4
        else:  # Left or Right
            cart['direction'] = (cart['direction'] - 1) % 4
    elif current_track == '\\':
        # Different behavior depending on approach direction
        if cart['direction'] in [0, 2]:  # Up or Down
            cart['direction'] = (cart['direction'] - 1) % 4
        else:  # Left or Right
            cart['direction'] = (cart['direction'] + 1) % 4
    # For straight tracks ('|' and '-'), no direction change is needed


def part_one(data: tuple) -> tuple:
    """
    Solves part 1 of the puzzle: find the location of the first cart collision.

    Args:
        file_path: Path to the input file

    Returns:
        The (x, y) coordinates of the first collision
    """

    tracks, carts = data

    # Continue until a collision is found
    while True:
        # Sort carts by position (top-to-bottom, left-to-right)
        # This ensures carts move in the correct order per the problem spec
        carts.sort(key=lambda c: (c['y'], c['x']))

        for cart in carts:
            # Move the cart
            move_cart(cart, tracks)

            # Check for collisions by examining if any two carts are at the
            # same position
            positions = [(c['x'], c['y']) for c in carts]
            for pos in positions:
                if positions.count(pos) > 1:
                    # Found a collision - return its coordinates
                    return pos


def part_two(data: tuple) -> tuple:
    """
    Solves part 2 of the puzzle: find the location of the last remaining cart
    after all collisions have occurred.

    Args:
        file_path: Path to the input file

    Returns:
        The (x, y) coordinates of the last remaining cart
    """

    tracks, carts = data

    # Continue until only one cart remains
    while sum(1 for cart in carts if not cart['crashed']) > 1:
        # Sort carts by position (top-to-bottom, left-to-right)
        carts.sort(key=lambda c: (c['y'], c['x']))

        for cart in carts:
            # Skip crashed carts
            if cart['crashed']:
                continue

            # Move the cart
            move_cart(cart, tracks)

            # Check for collisions with a dictionary for better efficiency
            positions = {}  # Maps positions to cart indices
            for i, c in enumerate(carts):
                if not c['crashed']:
                    pos = (c['x'], c['y'])
                    if pos in positions:
                        # Collision detected - mark both carts as crashed
                        carts[positions[pos]]['crashed'] = True
                        c['crashed'] = True
                    else:
                        positions[pos] = i

    # Find the last remaining cart that hasn't crashed
    remaining_cart = next(cart for cart in carts if not cart['crashed'])
    return (remaining_cart['x'], remaining_cart['y'])


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(copy.deepcopy(data)))  # 8,3
    print("Part 2:", part_two(copy.deepcopy(data)))  # 73,121
