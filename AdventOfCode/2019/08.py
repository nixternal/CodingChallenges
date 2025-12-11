#!/usr/bin/env python
from collections import Counter


def read_puzzle_input() -> str:
    with open("08.in", "r") as file:
        return file.read().strip()


def part_one(data: str) -> int:
    """Find layer with fewest 0s, return count of 1s * 2s."""
    width, height = 25, 6
    layer_size = width * height

    # Use Counter for efficient digit counting
    min_layer = min(
        (data[i : i + layer_size] for i in range(0, len(data), layer_size)),
        key=lambda layer: layer.count("0"),
    )

    counts = Counter(min_layer)
    return counts["1"] * counts["2"]


def part_two(data: str) -> str:
    """Decode the image by stacking transparent layers."""
    width, height = 25, 6
    layer_size = width * height

    # Build final image by finding first non-transparent pixel at each position
    final_image = []
    for i in range(layer_size):
        # Check layers from front to back
        for j in range(i, len(data), layer_size):
            if data[j] != "2":  # Not transparent
                final_image.append(data[j])
                break
        else:
            final_image.append("2")  # All layers transparent (shouldn't happen)

    # Format output
    rows = []
    for row in range(height):
        start = row * width
        row_pixels = final_image[start : start + width]
        row_display = "".join("█" if p == "1" else " " for p in row_pixels)
        rows.append(row_display)

    return "\n".join(rows)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 2080
    print(f"Part 2:\n{part_two(data)}")  # AURCY
