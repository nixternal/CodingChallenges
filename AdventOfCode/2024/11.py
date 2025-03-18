#!/usr/bin/env python


from collections import defaultdict


def read_puzzle_input() -> list:
    with open("11.in", "r") as file:
        return [int(x) for x in file.read().strip().split()]


def stone_manipulator(data: list, blinks: int) -> int:
    """
    Simulates transformations of stones over a specified number of blinks and
    returns the total count of stones.

    Args:
        data (list): A list of integers (as strings) representing the initial
                     stones.
        blinks (int): The number of transformation cycles (blinks) to simulate.

    Returns:
        int: The total number of stones remaining after all blinks.

    Description:
        The function takes a list of stone representations (as strings) and a
        number of blinks. Each blink applies transformation rules to the
        stones based on their properties:

        1. Stones are grouped by their integer values, and their counts are
           tracked.
        2. During each blink:
            - Stones with a value of 0 are transformed into stones of value 1.
            - Stones with an even-length string representation are split into
              two new stones, corresponding to the left and right halves of
              the string.
            - Stones with an odd-length string representation are multiplied
              by 2024.
        3. Stones with a resulting count of zero are removed from the tracking
           dictionary.

        At the end of all blinks, the total count of stones is computed and
        returned.

        Code is borrowed from Reddit: "Way faster than mine & completes Pt 2."
        https://www.reddit.com/r/adventofcode/comments/1hbm0al/comment/m1lgvua/
    """
    input = defaultdict(int)  # Dict to track stone counts by value
    for d in data:  # Initialize ^Dict w/the counts of each unique stone value.
        input[d] += 1

    for _ in range(blinks):
        updates = defaultdict(int)  # Tmp Dict to track changes in stone counts

        for k, v in input.items():
            s = str(k)  # Convert stone value to string
            updates[k] -= v  # Decrease the count of the current stone

            if k == 0:
                updates[1] += v  # Stones with value 0 transform in to 1
            elif len(s) % 2 == 0:
                l, r = s[:len(s) // 2], s[len(s) // 2:]  # Split string in half
                updates[int(l)] += v  # Add new stones based on left half
                updates[int(r)] += v  # Add new stones based on right half
            else:
                updates[k * 2024] += v  # Multiply odd length stones by 2024

        # Apply updates to main Dict
        for k, v in updates.items():
            input[k] += v
            if input[k] == 0:
                input.pop(k)  # Remove stones with 0 count

    return sum(input.values())


def part_one(data: list) -> int:
    return stone_manipulator(data, 25)


def part_two(data: list) -> int:
    return stone_manipulator(data, 75)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 194782
    print("Part 2:", part_two(data))  # 233007586663131


# def stone_manipulator(data: list, blinks: int) -> int:
    # My original code. Completed Part 1 successfully but Part 2 bombed my
    # system.
    # for _ in range(blinks):
    #     stones = []
    #     for stone in data:
    #         if stone == 0:
    #             stones.append(1)
    #         elif len(str(stone)) % 2 == 0:
    #             stones.append(int(str(stone)[:len(str(stone))//2]))
    #             stones.append(int(str(stone)[len(str(stone))//2:]))
    #         else:
    #             stones.append(stone * 2024)
    #     data = stones

    # return len(data)
