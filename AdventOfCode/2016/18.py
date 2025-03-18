#!/usr/bin/env python


def read_puzzle_input() -> str:
    with open("18.in", "r") as file:
        return file.read().strip()


def count_safe_tiles(initial_row: str, num_rows: int) -> int:
    """
    Computes the number of safe tiles after generating a given number of rows
    based on a set of transformation rules.

    Parameters:
    - initial_row (str): A string representing the first row of tiles,
                         where '.' is a safe tile and '^' is a trap tile.
    - num_rows (int): The total number of rows to generate.

    Returns:
    - int: The total count of safe tiles across all rows.

    Explanation:
    - The input row is treated as a boolean list: True for trap ('^'), False
      for safe ('.').
    - Each new row is generated based on the previous row using predefined
      transformation rules.
    - We count safe tiles while generating rows to avoid extra memory usage.
    - The algorithm only keeps track of the current and previous rows to
      optimize space usage.
    """

    # Convert initial row into a boolean list (True for trap, False for safe)
    prev_row = [char == '^' for char in initial_row]
    width = len(prev_row)  # Number of columns in each row

    # Count the number of safe tiles in the first row
    safe_count = prev_row.count(False)

    # Iterate to generate the remaining rows
    for _ in range(num_rows - 1):
        new_row = [False] * width  # Placeholder for the next row

        # Generate the next row based on the transformation rules
        for i in range(width):
            # Determine the state of the left, center, and right tiles
            left = prev_row[i - 1] if i > 0 else False  # Assume in bounds
            center = prev_row[i]
            right = prev_row[i + 1] if i < width - 1 else False

            # Apply trap generation rules
            # A tile is a trap (True) if any of these patterns exist in the
            # previous row:
            #  1. '^^.' (left and center are traps, right is safe)
            #  2. '.^^' (center and right are traps, left is safe)
            #  3. '^..' (only left is a trap)
            #  4. '..^' (only right is a trap)
            new_row[i] = (left and center and not right) or \
                (center and right and not left) or \
                (left and not center and not right) or \
                (right and not left and not center)

        # Count the safe tiles in the newly generated row
        safe_count += new_row.count(False)

        # Move to the next row by replacing prev_row with new_row
        prev_row = new_row

    # Return the total number of safe tiles
    return safe_count


def part_one(data: str) -> int:
    return count_safe_tiles(data, 40)


def part_two(data: str) -> int:
    return count_safe_tiles(data, 400000)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2035
    print("Part 2:", part_two(data))  # 20000577
