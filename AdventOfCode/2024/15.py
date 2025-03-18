#!/usr/bin/env python

"""
https://www.reddit.com/r/adventofcode/comments/1hele8m/comment/m24yt7h/
"""


def read_puzzle_input() -> str:
    with open("15.in", "r") as file:
        return file.read()


def move(grid: dict, p: complex, d: complex) -> bool:
    """
    Attempts to move an entity in the grid based on the provided direction.

    This function checks various constraints to ensure valid movement. If the
    movement is valid, it updates the grid by swapping the current position
    with the previous one. Uses recursion for specific conditions.

    Args:
        grid (dict): A dictionary representing the grid. Keys are positions
                     (complex numbers) & values are grid elements (characters).
        p (complex): The current POSITION in the grid.
        d (complex): The DIRECTION of movement as a complex number.

    Returns:
        bool: True if the move was successful, False otherwise.
    """

    p += d  # Update current Position w/ the movement Direction

    if all([  # Check all movement constraints & recursively resolve conditions
            grid[p] != '[' or move(grid, p+1, d) and move(grid, p, d),
            grid[p] != ']' or move(grid, p-1, d) and move(grid, p, d),
            grid[p] != 'O' or move(grid, p, d),
            grid[p] != '#']):
        # Swap the current Position with previous Position
        grid[p], grid[p-d] = grid[p-d], grid[p]
        return True

    return False


def main(data: str) -> None:
    """
    Main function to process the puzzle input, simulate movements, & calculate
    results.

    Args:
        data (str): The input data containing the grid & movement instructions,
                    separated by a blank line.

    Returns:
        None
    """

    part = 1  # For printing out Part 1 & Part 2 answers only

    # Split input into the grid layout and movement instructions
    grid, movements = data.split('\n\n')

    # Process the grid for 2 scenarios: original & modified
    for grid in grid, grid.translate(
            str.maketrans({'#': '##', '.': '..', 'O': '[]', '@': '@.'})):
        # Convert grid into a dictionary where keys are positions (complex
        # numbers)
        grid = {i+j*1j: c for j, r in enumerate(
            grid.split()) for i, c in enumerate(r)}

        # Find the initial position of the player ('@')
        pos, = [p for p in grid if grid[p] == '@']

        # Process each movement instruction
        for m in movements.replace('\n', ''):
            # Map movement characters to directions represented as complex
            # numbers
            dir = {'<': -1, '>': +1, '^': -1j, 'v': +1j}[m]

            # Create a backup of the grid to revert invalid moves
            C = grid.copy()

            # Attempt to move; if unsuccessful, revert to the backup grid
            if move(grid, pos, dir):
                pos += dir  # Update position if the move succeeds
            else:
                grid = C  # Revert to the backup grid if the move fails

        # Calculate the result: sum of positions with specific elements
        ans = sum(pos for pos in grid if grid[pos] in 'O[')

        # Print the result for the current part
        print(f"Part {part}:", int(ans.real + ans.imag*100))
        part += 1  # Increment part so it prints Part 2 next iteration


if __name__ == "__main__":
    main(read_puzzle_input())
    # Part 1: 1421727
    # Part 2: 1463160
