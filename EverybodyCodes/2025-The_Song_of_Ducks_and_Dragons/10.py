#!/usr/bin/env python3

from functools import lru_cache

# Knight moves for dragon
MOVES = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))


def read_puzzle_input() -> list:
    with open("10.in", "r") as f:
        return f.read().split("\n\n")


def get_reachable(positions, rows, cols):
    """Return all squares reachable in one knight move."""
    reachable = set()
    for r, c in positions:
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                reachable.add((nr, nc))
    return reachable


def part_one(data: list) -> int:
    """Count sheep reachable by dragon in exactly 4 moves."""
    board = data[0].splitlines()
    rows, cols = len(board), len(board[0])

    # Find dragon starting position
    start = next((r, c) for r in range(rows) for c in range(cols) if board[r][c] == "D")

    # BFS to find all reachable positions in exactly 4 moves
    visited = {start}
    current = {start}

    for _ in range(4):
        current = get_reachable(current, rows, cols)
        visited.update(current)

    # Count sheep in visited positions (excluding start)
    return sum(1 for r, c in visited if board[r][c] == "S" and (r, c) != start)


def part_two(data: list) -> int:
    """Simulate 20 rounds of dragon chasing sheep."""
    board = data[1].splitlines()
    rows, cols = len(board), len(board[0])

    # Parse board
    dragon = set()
    sheep = set()
    hideouts = set()

    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch == "D":
                dragon.add((r, c))
            elif ch == "S":
                sheep.add((r, c))
            elif ch == "#":
                hideouts.add((r, c))

    eaten = 0

    for _ in range(20):
        # Dragon moves and eats exposed sheep
        dragon = get_reachable(dragon, rows, cols)
        vulnerable = dragon & sheep - hideouts
        eaten += len(vulnerable)
        sheep -= vulnerable

        # Sheep move down; eaten if they land on dragon (not in hideout)
        next_sheep = set()
        for r, c in sheep:
            if r < rows - 1:  # Not at bottom
                nr = r + 1
                if (nr, c) not in dragon or (nr, c) in hideouts:
                    next_sheep.add((nr, c))
                else:
                    eaten += 1
            # Sheep at bottom row escape (don't add to next_sheep)

        sheep = next_sheep

    return eaten


def part_three(data: list) -> int:
    """Count valid sequences where dragon eats all sheep."""
    board = data[2].splitlines()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Parse board
    sheep = set()
    hideouts = set()
    dragon = None

    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch == "S":
                sheep.add((r, c))
            elif ch == "#":
                hideouts.add((r, c))
            elif ch == "D":
                dragon = (r, c)

    @lru_cache(maxsize=None)
    def count_sequences(sheep_tuple, dragon_pos, is_sheep_turn):
        if not sheep_tuple:
            return 1  # All sheep eaten - success!

        sheep_set = set(sheep_tuple)

        if is_sheep_turn:
            # Find all legal non-escape moves
            legal_moves = []
            can_escape = False

            for r, c in sheep_set:
                if r == rows - 1:
                    can_escape = True
                    continue

                nr, nc = r + 1, c
                # Sheep won't move into dragon unless on hideout
                if (nr, nc) == dragon_pos and (nr, nc) not in hideouts:
                    continue

                # Legal move found
                new_sheep = sheep_set - {(r, c)} | {(nr, nc)}
                legal_moves.append(tuple(sorted(new_sheep)))

            if legal_moves:
                return sum(count_sequences(s, dragon_pos, False) for s in legal_moves)

            # No legal moves - if sheep can escape, sequence fails
            if can_escape:
                return 0

            # No moves possible - skip to dragon turn
            return count_sequences(sheep_tuple, dragon_pos, False)

        else:  # Dragon turn
            total = 0
            dr, dc = dragon_pos

            for ddr, ddc in MOVES:
                nr, nc = dr + ddr, dc + ddc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue

                new_pos = (nr, nc)

                # Check if dragon eats a sheep
                if new_pos in sheep_set and new_pos not in hideouts:
                    new_sheep = sheep_set - {new_pos}
                    if not new_sheep:
                        total += 1  # Last sheep eaten!
                    else:
                        total += count_sequences(
                            tuple(sorted(new_sheep)), new_pos, True
                        )
                else:
                    total += count_sequences(sheep_tuple, new_pos, True)

            return total

    return count_sequences(tuple(sorted(sheep)), dragon, True)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 160
    print("Part 2:", part_two(data))  # 1739
    print("Part 3:", part_three(data))  # 4370454399967
