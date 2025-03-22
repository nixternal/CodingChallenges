#!/usr/bin/env python

from typing import Dict, Tuple, List


def read_puzzle_input() -> List[str]:
    with open("21.in", "r") as file:
        return file.read().splitlines()


def parse_input(data: List) -> Dict[Tuple[str, ...], Tuple[str, ...]]:
    """Parse the input text into a dictionary of rules"""
    rules = {}
    for line in data:
        pattern, result = line.split(' => ')
        pattern = tuple(pattern.split('/'))
        result = tuple(result.split('/'))
        rules[pattern] = result

        # Add all possible rotations and flips
        for i in range(3):
            pattern = rotate(pattern)
            rules[pattern] = result
            flipped = flip(pattern)
            rules[flipped] = result

    return rules


def flip(pattern: Tuple[str, ...]) -> Tuple[str, ...]:
    """Flip a pattern horizontally"""
    return tuple(row[::-1] for row in pattern)


def rotate(pattern: Tuple[str, ...]) -> Tuple[str, ...]:
    """Rotate a pattern 90 degrees clockwise"""
    size = len(pattern)
    return tuple(
        ''.join(
            pattern[size-1-j][i] for j in range(size)
        ) for i in range(size)
    )


def split_grid(grid: Tuple[str, ...]) -> List[List[Tuple[str, ...]]]:
    """Split the grid into 2x2 or 3x3 blocks"""
    size = len(grid)
    if size % 2 == 0:  # Split in to 2x2 blocks
        block_size = 2
    else:  # Split in to 3x3 blocks
        block_size = 3

    blocks = []
    for y in range(0, size, block_size):
        row_blocks = []
        for x in range(0, size, block_size):
            block = tuple(grid[y+i][x:x+block_size] for i in range(block_size))
            row_blocks.append(block)
        blocks.append(row_blocks)

    return blocks


def enhance_blocks(blocks: List[List[Tuple[str, ...]]],
                   rules: Dict[Tuple[str, ...], Tuple[str, ...]]
                   ) -> List[List[Tuple[str, ...]]]:
    """Enhance each block according to the rules"""
    enhanced = []
    for row in blocks:
        enhanced_row = []
        for block in row:
            enhanced_row.append(rules[block])
        enhanced.append(enhanced_row)

    return enhanced


def merge_blocks(blocks: List[List[Tuple[str, ...]]]) -> Tuple[str, ...]:
    """Merge blocks back into a single grid"""
    result = []
    for row_blocks in blocks:
        block_height = len(row_blocks[0])
        for i in range(block_height):
            result.append(''.join(block[i] for block in row_blocks))

    return tuple(result)


def count_on_pixels(grid: Tuple[str, ...]) -> int:
    """Count the number of '#' characters in the grid."""
    return sum(row.count('#') for row in grid)


def part_one(data: List, iterations: int = 5) -> int:
    rules = parse_input(data)
    grid: Tuple[str, ...] = ('.#.', '..#', '###')  # Initial pattern

    for _ in range(iterations):
        blocks = split_grid(grid)
        enhanced_blocks = enhance_blocks(blocks, rules)
        grid = merge_blocks(enhanced_blocks)

    return count_on_pixels(grid)


def part_two(data: list) -> int:
    return part_one(data, iterations=18)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 160
    print("Part 2:", part_two(data))  # 2271537
