#!/usr/bin/env python3
"""
Balloon-popping circle puzzle.

Each balloon is colored Red, Green, or Blue. A "shooter" repeatedly fires,
cycling through colors in the fixed order R -> G -> B -> R -> ... On each
shot:

  - Every balloon matching the current color, starting from the current
    position, is popped ("the fluffbolt flies through consecutive matching
    balloons").
  - The next balloon that does NOT match (if any remain) is also popped,
    ending that shot.

Part 1 runs this once, left-to-right, over a single row of balloons
(no wraparound).

Parts 2 and 3 instead treat the balloons as arranged in a *circle* (the
puzzle input line is repeated many times to build a large ring) and ask
how many shots it takes to pop every balloon, where each shot may also
pop the balloon directly opposite the first one in the remaining circle.
Because the ring can be huge, both parts need better-than-O(n) per-shot
bookkeeping:

  - Part 2 uses a Fenwick tree (Binary Indexed Tree) to do O(log n)
    "find the k-th surviving balloon" and "remove a balloon" operations.
  - Part 3 uses two deques representing the two halves of the circle,
    which turns out to be simpler and faster still for that variant.
"""

from array import array
from collections import deque

COLOR_ORDER = "RGB"  # shot color cycles through this, wrapping with modulo


def read_puzzle_input() -> list[str]:
    """Read non-blank, stripped lines from the puzzle input file."""
    with open("02.in", "r") as file:
        return [line.strip() for line in file if line.strip()]


def part_one(data: list[str]) -> int:
    """
    Single left-to-right pass (no wraparound) over data[0].

    Each shot pops a run of consecutive balloons matching the current
    color, then pops the following non-matching balloon too (if one
    exists). Returns the total number of shots needed to consume the row.
    """
    balloons = data[0]
    n = len(balloons)
    i = 0
    shots = 0

    while i < n:
        color = COLOR_ORDER[shots % 3]

        # The fluffbolt flies through every consecutive matching balloon...
        while i < n and balloons[i] == color:
            i += 1

        # ...then pops the first non-matching balloon too, and disappears.
        if i < n:
            i += 1

        shots += 1

    return shots


def part_two(data: list[str]) -> int:
    """
    Circular version using a Fenwick tree (BIT) over "alive" balloons.

    The input row is repeated 100x to form one large circle. On each shot:
      - `first` = the balloon currently at the front of the circle.
      - If the circle has an even number of balloons left AND `first`
        matches the current shot color, the balloon diametrically
        opposite `first` is popped too (two removals this shot).
      - Otherwise only `first` is popped (one removal this shot).

    A Fenwick tree lets us do both operations we need in O(log n) each:
      - kth_alive(k): find the original index of the k-th surviving
        balloon (0-indexed), via binary search over prefix sums.
      - remove(position): mark a balloon as popped by decrementing the
        tree's counts from that position onward.

    Returns the total number of shots to empty the circle.
    """
    balloons = data[1] * 100
    n = len(balloons)

    if n == 0:
        return 0

    # bit[i] initially holds the number of set low bits in i (i & -i),
    # which is the standard Fenwick-tree initialization for "every
    # position starts alive": each node's stored value is the count of
    # alive balloons in the range it covers.
    bit = array("I", (i & -i for i in range(n + 1)))
    highest_power = 1 << (n.bit_length() - 1)

    def kth_alive(k: int) -> int:
        """Return the original zero-based position of the k-th alive balloon."""
        target = k + 1
        index = 0
        step = highest_power

        while step:
            candidate = index + step
            if candidate <= n and bit[candidate] < target:
                index = candidate
                target -= bit[candidate]
            step >>= 1

        return index

    def remove(position: int) -> None:
        """Mark an original position as popped (Fenwick-tree point update)."""
        i = position + 1
        while i <= n:
            bit[i] -= 1
            i += i & -i

    remaining = n
    shots = 0

    while remaining:
        shot_color = COLOR_ORDER[shots % 3]
        first = kth_alive(0)

        # A second balloon is hit only when:
        # 1. the first balloon matches the shot color, and
        # 2. the circle had an even number of balloons before this shot
        #    (so an "opposite" balloon is well-defined).
        if remaining % 2 == 0 and balloons[first] == shot_color:
            opposite = kth_alive(remaining // 2)
            remove(first)
            remove(opposite)
            remaining -= 2
        else:
            remove(first)
            remaining -= 1

        shots += 1

    return shots


def part_three(data: list[str]) -> int:
    """
    Circular version using two deques as the two halves of the ring.

    The input fragment is validated, encoded to bytes, and repeated
    100,000 times to build the circle, then split into a `left` half and
    a `right` half of (near-)equal size. `left[0]` and `right[0]` are
    always each other's "opposite" balloon while the two halves stay
    balanced, which lets each shot run in amortized O(1) instead of the
    O(log n) needed for the Fenwick-tree approach in part 2.

    Returns the total number of shots to empty the circle.
    """
    fragment = "".join(data[2].split())

    if not fragment:
        return 0

    if not set(fragment) <= {"R", "G", "B"}:
        raise ValueError(f"Invalid balloon sequence: {fragment!r}")

    # Bytes so deque items are small ints, not one-character strings.
    sequence = fragment.encode() * 100_000
    remaining = len(sequence)

    # For odd `remaining`: left holds floor(remaining/2), right holds the rest.
    midpoint = remaining // 2
    left = deque(sequence[:midpoint])
    right = deque(sequence[midpoint:])
    del sequence  # free the big temporary copy; deques hold what we need

    colors = b"RGB"
    shots = 0

    while remaining:
        shot_color = colors[shots % 3]
        was_odd = remaining % 2 == 1

        # When remaining is even, left[0] is the front balloon and
        # right[0] is directly opposite it in the circle.
        if not was_odd and left[0] == shot_color:
            left.popleft()
            right.popleft()
            remaining -= 2
        else:
            # Pop the front balloon of the circle. `left` is only empty
            # in the final one-balloon case.
            if left:
                left.popleft()
            else:
                right.popleft()
            remaining -= 1

            # An odd-sized circle just became even-sized. Re-balance by
            # moving right's front balloon onto the end of left.
            if was_odd and remaining:
                left.append(right.popleft())

        shots += 1

    return shots


def main() -> None:
    data = read_puzzle_input()
    print("Part 1:", part_one(data))    # 131
    print("Part 2:", part_two(data))    # 21359
    print("Part 3:", part_three(data))  # 21484432


if __name__ == "__main__":
    main()
