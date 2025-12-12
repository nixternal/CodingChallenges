#!/usr/bin/env python


def read_puzzle_input() -> list:
    with open("12.in", "r") as file:
        return file.read().splitlines()


def parse_input(lines):
    shapes = {}
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()
        if line == "":
            i += 1
            continue

        if line.endswith(":") and line[:-1].isdigit():
            idx = int(line[:-1])
            i += 1
            shape_lines = []
            while i < n and lines[i].strip() != "":
                shape_lines.append(lines[i].rstrip("\n"))
                i += 1

            cells = []
            for y, row in enumerate(shape_lines):
                for x, ch in enumerate(row):
                    if ch == "#":
                        cells.append((x, y))
            shapes[idx] = tuple(cells)
        else:
            break
        i += 1

    while i < n and lines[i].strip() == "":
        i += 1

    regions = []
    for j in range(i, n):
        line = lines[j].strip()
        if not line or ":" not in line:
            continue

        dims, rest = line.split(":", 1)
        dims = dims.strip()
        if "x" not in dims:
            continue

        w_str, h_str = dims.split("x")
        w, h = int(w_str), int(h_str)
        counts = [int(x) for x in rest.strip().split()]
        regions.append((w, h, counts))

    return shapes, regions


def canonical_orientations(cells):
    res = set()

    def normalize(pts):
        if not pts:
            return ()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        minx, miny = min(xs), min(ys)
        return tuple(sorted((x - minx, y - miny) for x, y in pts))

    for flipx in (0, 1):
        for rot in range(4):
            transformed = []
            for x, y in cells:
                x0 = -x if flipx else x
                xr, yr = x0, y
                for _ in range(rot):
                    xr, yr = -yr, xr
                transformed.append((xr, yr))
            res.add(normalize(transformed))

    return [tuple(t) for t in res]


def placements_for_shape_in_region(shape_cells, w, h):
    orients = canonical_orientations(shape_cells)
    placements = []
    seen = set()

    for o in orients:
        xs = [p[0] for p in o]
        ys = [p[1] for p in o]
        shape_w = max(xs) - min(xs) + 1
        shape_h = max(ys) - min(ys) + 1

        if shape_w > w or shape_h > h:
            continue

        for dx in range(w - shape_w + 1):
            for dy in range(h - shape_h + 1):
                placed = tuple((x + dx, y + dy) for x, y in o)
                if placed not in seen:
                    seen.add(placed)
                    placements.append(placed)

    return placements


def can_fit_region(shapes, w, h, counts):
    total_cells = 0
    active_shapes = []

    for idx, cnt in enumerate(counts):
        if cnt == 0:
            continue
        if idx not in shapes:
            return False
        total_cells += len(shapes[idx]) * cnt
        active_shapes.append((idx, cnt))

    if total_cells > w * h or total_cells == 0:
        return total_cells == 0

    # Precompute placements as bitsets
    placements_bits = {}
    shape_sizes = {}

    for idx, _ in active_shapes:
        placements = placements_for_shape_in_region(shapes[idx], w, h)
        if not placements:
            return False

        bits_list = []
        for p in placements:
            bits = 0
            for x, y in p:
                bits |= 1 << (y * w + x)
            bits_list.append(bits)
        placements_bits[idx] = bits_list
        shape_sizes[idx] = len(shapes[idx])

    # Build pieces list - try largest pieces first for better pruning
    pieces = []
    piece_sizes = []
    for idx, cnt in sorted(
        active_shapes, key=lambda x: (-len(shapes[x[0]]), len(placements_bits[x[0]]))
    ):
        for _ in range(cnt):
            pieces.append(placements_bits[idx])
            piece_sizes.append(shape_sizes[idx])

    n_pieces = len(pieces)
    total_area = w * h

    # Backtrack with improved pruning
    def backtrack(idx, occupied, cells_used):
        if idx == n_pieces:
            return True

        # Prune: check if remaining pieces can fit in remaining space
        cells_left = total_area - cells_used
        cells_needed = sum(piece_sizes[i] for i in range(idx, n_pieces))
        if cells_needed > cells_left:
            return False

        bits_list = pieces[idx]
        piece_size = piece_sizes[idx]

        for bits in bits_list:
            if occupied & bits == 0:
                if backtrack(idx + 1, occupied | bits, cells_used + piece_size):
                    return True

        return False

    return backtrack(0, 0, 0)


def part_one(data: list) -> int:
    shapes, regions = parse_input(data)
    fit_count = 0
    for w, h, counts in regions:
        if can_fit_region(shapes, w, h, counts):
            fit_count += 1
    return fit_count


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))
