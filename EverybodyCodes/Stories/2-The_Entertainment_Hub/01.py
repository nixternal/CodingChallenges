#!/usr/bin/env python
"""
Solves a pachinko/plinko-style puzzle in three parts.

Tokens are dropped into a "machine" (a grid of nail positions marked
with '*') and deflect left or right off each nail they hit according
to a per-token behavior string, until they land in a final slot.
Landing in a higher-numbered slot than the token was dropped in earns
coins; landing lower (or in the same slot) earns nothing.

Part 1: sum of coins from dropping each token in a fixed, given slot.
Part 2: sum of the best possible coin result per token, trying every slot.
Part 3: assign each token to a distinct slot (no slot reused) to find
        both the minimum and maximum total coins achievable — solved
        as a linear assignment problem via the Hungarian algorithm.
"""

from scipy.optimize import linear_sum_assignment


def read_puzzle_input() -> list[tuple[list[str], list[str]]]:
    """
    Read and parse the puzzle input file.

    The file is expected to contain blocks of text separated by blank
    lines, alternating between a machine layout and a list of token
    behavior strings: [machine1, tokens1, machine2, tokens2, ...].

    Returns:
        A list of (machine, tokens) tuples, one per puzzle part, where
        `machine` is the grid as a list of row strings and `tokens`
        is a list of behavior strings (one per token).
    """
    with open("01.in", "r") as file:
        blocks = file.read().strip().split("\n\n")

    return [
        (blocks[i].splitlines(), blocks[i + 1].splitlines())
        for i in range(0, len(blocks), 2)
    ]


def slot_count(machine: list[str]) -> int:
    """
    Compute the number of drop slots along the top of the machine.

    Slots are spaced two characters apart across the width of the
    machine's top row (e.g. a row of width 7 has slots at columns
    0, 2, 4, 6 -> 4 slots).

    Args:
        machine: The machine grid as a list of row strings.

    Returns:
        The number of available toss slots.
    """
    return (len(machine[0]) + 1) // 2


def drop_token(machine: list[str], behavior: str, toss_slot: int) -> int:
    """
    Simulate a single token falling through the machine.

    The token starts in `toss_slot` and falls row by row. Whenever it
    hits a nail ('*' at its current column), it deflects according to
    the next character in `behavior` ('L' or 'R'), except:
      - At the left wall (column 0), it always bounces right (inward).
      - At the right wall (last column), it always bounces left (inward).

    Args:
        machine: The machine grid as a list of row strings, each row
            using every other character position ('*' or space) for
            nails, so that column = 2 * (slot - 1).
        behavior: A string of 'L'/'R' characters consumed in order,
            one per nail the token actually hits.
        toss_slot: The 1-indexed slot the token is dropped into.

    Returns:
        The 1-indexed slot the token lands in after falling through
        every row of the machine.
    """
    width = len(machine[0])
    col = 2 * (toss_slot - 1)
    behavior_index = 0

    for row in machine:
        if row[col] != "*":
            continue

        direction = behavior[behavior_index]
        behavior_index += 1

        # A nail at either wall always sends the token inward.
        if col == 0:
            col += 1
        elif col == width - 1 or direction == "L":
            col -= 1
        else:  # direction == "R"
            col += 1

    return col // 2 + 1


def coins_won(machine: list[str], behavior: str, toss_slot: int) -> int:
    """
    Compute the coin payout for dropping one token in one slot.

    Payout is 2x the (final slot - starting slot) distance gained,
    floored at zero — landing at or below the starting slot pays
    nothing.

    Args:
        machine: The machine grid as a list of row strings.
        behavior: The token's L/R deflection behavior string.
        toss_slot: The 1-indexed slot the token is dropped into.

    Returns:
        The number of coins won (0 or more).
    """
    final_slot = drop_token(machine, behavior, toss_slot)
    return max(0, 2 * final_slot - toss_slot)


def part_one(puzzle: tuple[list[str], list[str]]) -> int:
    """
    Sum the coins won when each token is dropped in the slot matching
    its position in the input (token 1 -> slot 1, token 2 -> slot 2, ...).

    Args:
        puzzle: A (machine, tokens) tuple.

    Returns:
        Total coins won across all tokens.
    """
    machine, tokens = puzzle

    return sum(
        coins_won(machine, behavior, toss_slot)
        for toss_slot, behavior in enumerate(tokens, start=1)
    )


def part_two(puzzle: tuple[list[str], list[str]]) -> int:
    """
    Sum, for each token independently, the best coin result achievable
    by trying every available slot (slots may be reused across tokens).

    Args:
        puzzle: A (machine, tokens) tuple.

    Returns:
        Total coins won, taking each token's best slot choice.
    """
    machine, tokens = puzzle

    total = 0
    for behavior in tokens:
        best_coins = max(
            coins_won(machine, behavior, toss_slot)
            for toss_slot in range(1, slot_count(machine) + 1)
        )
        total += best_coins

    return total


def part_three(puzzle: tuple[list[str], list[str]]) -> str:
    """
    Find the minimum and maximum total coins achievable when every
    token must be assigned to its own distinct slot (no two tokens
    share a slot).

    This is a linear assignment problem: build a tokens x slots score
    matrix, then use the Hungarian algorithm (via
    scipy.optimize.linear_sum_assignment) to find the optimal
    one-to-one assignment for both the minimum and maximum cases.

    If there are more slots than tokens, the score matrix is padded
    with zero-score dummy token rows so every slot can still be
    assigned in the square matrix `linear_sum_assignment` expects.
    Unused/dummy assignments contribute 0 to the total and don't
    affect the result.

    Args:
        puzzle: A (machine, tokens) tuple.

    Returns:
        A string "MIN MAX" giving the minimum and maximum total coins
        achievable across all valid one-to-one token-slot assignments.
    """
    machine, tokens = puzzle
    n_slots = slot_count(machine)

    # scores[i][j] = coins won if token i is dropped in slot j+1
    scores = [
        [coins_won(machine, behavior, toss_slot) for toss_slot in range(1, n_slots + 1)]
        for behavior in tokens
    ]

    # Pad to square if there are more slots than tokens, since
    # linear_sum_assignment requires assigning every row.
    n_tokens = len(tokens)
    if n_slots > n_tokens:
        pad_rows = [[0] * n_slots for _ in range(n_slots - n_tokens)]
        scores = scores + pad_rows

    row_ind, col_min = linear_sum_assignment(scores)
    _, col_max = linear_sum_assignment(scores, maximize=True)

    minimum_score = sum(scores[r][c] for r, c in zip(row_ind, col_min))
    maximum_score = sum(scores[r][c] for r, c in zip(row_ind, col_max))

    return f"{minimum_score} {maximum_score}"


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data[0]))  # 48
    print("Part 2:", part_two(data[1]))  # 1154
    print("Part 3:", part_three(data[2]))  # 40 120
