#!/usr/bin/env python
import re
from collections import defaultdict, deque

# ---------------------------------------------------------------------------
# Type alias for a BST node dict
# ---------------------------------------------------------------------------
# Node = {"id": str, "rank": int, "symbol": str, "left": Node|None, "right": Node|None}
ADD_PAT = re.compile(r"ADD id=(\d+) left=\[(\d+),(\S)\] right=\[(\d+),(\S)\]")
SWAP_PAT = re.compile(r"SWAP (\d+)")


def read_puzzle_input() -> list[str]:
    """Read 02.in and split into three sections on double-newlines."""
    with open("02.in") as file:
        return file.read().strip().split("\n\n")


def insert_node(root: dict | None, new_node: dict) -> dict:
    """
    Insert *new_node* into the BST rooted at *root* using standard rank-based
    BST ordering (left < rank, right >= rank). Returns the (possibly new) root.
    Iterative to avoid recursion-depth issues on large inputs.
    """
    if root is None:
        return new_node
    curr = root
    while True:
        if new_node["rank"] < curr["rank"]:
            if curr["left"] is None:
                curr["left"] = new_node
                break
            curr = curr["left"]
        else:
            if curr["right"] is None:
                curr["right"] = new_node
                break
            curr = curr["right"]
    return root


def make_node(nid: str, rank: int, symbol: str) -> dict:
    """Convenience constructor for a BST node dict."""
    return {"id": nid, "rank": rank, "symbol": symbol, "left": None, "right": None}


def level_symbol_counts(root: dict) -> dict[int, int]:
    """
    BFS over the tree to count nodes per level.
    Returns {level: count} (1-indexed, root = level 1).
    """
    counts: dict[int, int] = defaultdict(int)
    queue = deque([(root, 1)])
    while queue:
        node, lvl = queue.popleft()
        counts[lvl] += 1
        if node["left"]:
            queue.append((node["left"], lvl + 1))
        if node["right"]:
            queue.append((node["right"], lvl + 1))
    return counts


def symbols_at_level(node: dict | None, target: int, current: int = 1) -> list[str]:
    """
    Collect symbols at *target* depth in left-to-right order via pre-order DFS.
    Recursive; depth is bounded by tree height (typically log n for balanced trees).
    """
    if node is None:
        return []
    if current == target:
        return [node["symbol"]]
    left = symbols_at_level(node["left"], target, current + 1)
    right = symbols_at_level(node["right"], target, current + 1)
    return left + right


def get_tree_message(root: dict | None) -> str:
    """
    Decode the message hidden in *root*:
      1. Find the level with the most nodes (most-populated).
      2. Break ties by picking the level closest to the root.
      3. Return its symbols concatenated left-to-right.
    """
    if not root:
        return ""
    counts = level_symbol_counts(root)
    max_pop = max(counts.values())
    best = min(lvl for lvl, cnt in counts.items() if cnt == max_pop)
    return "".join(symbols_at_level(root, best))


def find_all_by_id(roots: list[dict | None], target_id: str) -> list[dict]:
    """
    BFS over every tree in *roots* to locate all nodes whose id == *target_id*.
    Returns a list of location dicts:
        {"tree_idx": int, "parent": node|None, "dir": "root"|"left"|"right"}

    Part 3 SWAPs move entire subtrees, so we need parent references.
    """
    found = []
    for tree_idx, root in enumerate(roots):
        if root is None:
            continue
        if root["id"] == target_id:
            found.append({"tree_idx": tree_idx, "parent": None, "dir": "root"})

        queue = deque([root])
        while queue:
            curr = queue.popleft()
            for direction in ("left", "right"):
                child = curr[direction]
                if child is None:
                    continue
                if child["id"] == target_id:
                    found.append(
                        {"tree_idx": tree_idx, "parent": curr, "dir": direction}
                    )
                queue.append(child)
    return found


def structural_swap(roots: list[dict | None], sid: str) -> None:
    """
    Swap the two subtrees identified by *sid* in-place within *roots*.
    If fewer than two locations are found the swap is silently skipped.
    """
    found = find_all_by_id(roots, sid)
    if len(found) < 2:
        return

    loc1, loc2 = found[0], found[1]

    # Fetch the actual node objects currently sitting at each location
    node1 = (
        roots[loc1["tree_idx"]]
        if loc1["dir"] == "root"
        else loc1["parent"][loc1["dir"]]
    )
    node2 = (
        roots[loc2["tree_idx"]]
        if loc2["dir"] == "root"
        else loc2["parent"][loc2["dir"]]
    )

    # Reattach node2 at loc1's position and node1 at loc2's position
    for loc, replacement in ((loc1, node2), (loc2, node1)):
        if loc["dir"] == "root":
            roots[loc["tree_idx"]] = replacement
        else:
            loc["parent"][loc["dir"]] = replacement


def part_one(data: list[str]) -> str:
    """
    Part 1 — Plain BST construction.

    Parse ADD instructions to build two independent BSTs (left & right),
    then decode and concatenate their messages.
    """
    left_root = right_root = None
    for line in data[0].splitlines():
        m = ADD_PAT.search(line)
        if m:
            nid, l_r, l_s, r_r, r_s = m.groups()
            left_root = insert_node(left_root, make_node(nid, int(l_r), l_s))
            right_root = insert_node(right_root, make_node(nid, int(r_r), r_s))

    return get_tree_message(left_root) + get_tree_message(right_root)


def part_two(data: list[str]) -> str:
    """
    Part 2 — BST with *label* swaps.

    SWAP exchanges the rank and symbol of the named node between the left and
    right trees — the nodes stay in their current structural positions, only
    their payload (rank + symbol) is swapped. A lookup dict gives O(1) access.
    """
    left_root = right_root = None
    left_lookup: dict[str, dict] = {}
    right_lookup: dict[str, dict] = {}

    for line in data[1].splitlines():
        add_m = ADD_PAT.search(line)
        if add_m:
            nid, l_r, l_s, r_r, r_s = add_m.groups()
            l_node = make_node(nid, int(l_r), l_s)
            r_node = make_node(nid, int(r_r), r_s)
            left_lookup[nid], right_lookup[nid] = l_node, r_node
            left_root = insert_node(left_root, l_node)
            right_root = insert_node(right_root, r_node)

        swap_m = SWAP_PAT.search(line)
        if swap_m:
            sid = swap_m.group(1)
            ln, rn = left_lookup[sid], right_lookup[sid]
            # Swap payloads only; pointers (left/right children) are untouched
            ln["rank"], rn["rank"] = rn["rank"], ln["rank"]
            ln["symbol"], rn["symbol"] = rn["symbol"], ln["symbol"]

    return get_tree_message(left_root) + get_tree_message(right_root)


def part_three(data: list[str]) -> str:
    """
    Part 3 — BST with *structural* swaps.

    SWAP physically relocates entire subtrees: the node (and all its descendants)
    from the left tree trades places with the corresponding subtree in the right
    tree.  Both trees are kept in a shared 'roots' list so find_all_by_id can
    search across the whole forest in one pass.
    """
    roots: list[dict | None] = [None, None]  # [left_root, right_root]

    for line in data[2].splitlines():
        add_m = ADD_PAT.search(line)
        if add_m:
            nid, l_r, l_s, r_r, r_s = add_m.groups()
            roots[0] = insert_node(roots[0], make_node(nid, int(l_r), l_s))
            roots[1] = insert_node(roots[1], make_node(nid, int(r_r), r_s))

        swap_m = SWAP_PAT.search(line)
        if swap_m:
            structural_swap(roots, swap_m.group(1))

    return get_tree_message(roots[0]) + get_tree_message(roots[1])


if __name__ == "__main__":
    puzzle_data = read_puzzle_input()
    print("Part 1:", part_one(puzzle_data))  # QUACK!NMRXBSWN
    print("Part 2:", part_two(puzzle_data))  # QUACK!WRMYSGRFGVSYTY
    print("Part 3:", part_three(puzzle_data))  # QUACK!NWLBBSVVNLTGFXMTTLYFJBSNGSPH
