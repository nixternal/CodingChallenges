#!/usr/bin/env python
"""
Artifact Collection Management System

This program solves three problems related to artifacts in a binary search
tree (BST):
1. Find the product of the maximum level sum and the number of occupied levels
2. Determine the insertion path for a new artifact with ID 500,000
3. Find the Lowest Common Ancestor (LCA) of two specified artifacts

Input Format:
- Each line contains an artifact name and ID separated by " | "
- The last two lines contain the artifacts for the LCA calculation

Output:
- Part 1: Product of maximum level sum and number of occupied levels
- Part 2: Path of artifact codes traversed for insertion of ID 500,000
- Part 3: Code of the Lowest Common Ancestor of two specified artifacts
"""

from collections import deque
from typing import Dict, List, Optional, Tuple, Any


def read_puzzle_input() -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    """
    Read and parse the input file containing artifact data.

    Returns:
        Tuple containing:
            - artifact_list: List of (name, id) tuples for all artifacts
                             except the last two
            - lca_artifacts: List of (name, id) tuples for the last two
                             artifacts used in LCA calculation
    """

    with open("15.in", "r") as file:
        lines = file.readlines()

    # Parse all but the last two lines as regular artifacts
    artifact_list: List[Tuple[str, int]] = []
    for line in lines[:-3]:
        name, id_value = line.strip().split(' | ')
        artifact_list.append((name, int(id_value)))

    # Extract last 2 lines for LCA calculation
    name1, id1 = lines[-2].strip().split(" | ")
    name2, id2 = lines[-1].strip().split(" | ")
    lca_artifacts: List[Tuple[str, int]] = [
        (name1, int(id1)),
        (name2, int(id2))
    ]

    return artifact_list, lca_artifacts


def insert_bst(
        tree: Optional[Dict[str, Any]],
        id_value: int,
        code: str
        ) -> Dict[str, Any]:
    """
    Insert a new artifact into the binary search tree.

    Args:
        tree: Current tree node or None if empty
        id_value: ID of the artifact to insert
        code: Code/name of the artifact to insert

    Returns:
        Updated tree node after insertion
    """
    if tree is None:
        return {"id": id_value, "code": code, "left": None, "right": None}

    if id_value < tree["id"]:
        tree["left"] = insert_bst(tree["left"], id_value, code)
    else:
        tree["right"] = insert_bst(tree["right"], id_value, code)

    return tree


def build_bst(
        artifact_list: List[Tuple[str, int]]
        ) -> Optional[Dict[str, Any]]:
    """
    Build a binary search tree from a list of artifacts.

    Args:
        artifact_list: List of (code, id) tuples

    Returns:
        Root node of the constructed BST
    """
    tree: Optional[Dict[str, Any]] = None
    for code, id_value in artifact_list:
        tree = insert_bst(tree, id_value, code)
    return tree


def level_sums(tree: Optional[Dict[str, Any]]) -> Dict[int, int]:
    """
    Calculate the sum of artifact IDs at each level of the tree using BFS.

    Args:
        tree: Root node of the BST

    Returns:
        Dictionary mapping level numbers to the sum of IDs at that level
    """
    if not tree:
        return {}

    queue = deque([(tree, 1)])  # (node, level) pairs
    level_sums_dict: Dict[int, int] = {}

    while queue:
        node, level = queue.popleft()

        # Add current node's ID to its level sum
        if level not in level_sums_dict:
            level_sums_dict[level] = 0
        level_sums_dict[level] += node["id"]

        # Enqueue children with incremented level
        if node["left"]:
            queue.append((node["left"], level + 1))
        if node["right"]:
            queue.append((node["right"], level + 1))

    return level_sums_dict


def find_insertion_path(tree: Dict[str, Any], new_id: int) -> str:
    """
    Find the path of artifact codes that would be traversed when inserting a
    new ID.

    Args:
        tree: Root node of the BST
        new_id: ID value to be inserted

    Returns:
        String representing the path, with artifact codes joined by "-"
    """
    path: List[str] = []
    current: Optional[Dict[str, Any]] = tree

    while current:
        path.append(current["code"])  # Add current node's code to path

        if new_id < current["id"]:
            if current["left"] is None:
                break  # Found insertion point on left
            current = current["left"]
        else:
            if current["right"] is None:
                break  # Found insertion point on right
            current = current["right"]

    return "-".join(path)


def find_lca(
        tree: Dict[str, Any],
        lcas: List[Tuple[str, int]]
        ) -> Optional[str]:
    """
    Find the Lowest Common Ancestor of two artifacts in the BST.

    Args:
        tree: Root node of the BST
        lcas: List of two (name, id) tuples representing the artifacts

    Returns:
        Code of the LCA node, or None if not found
    """
    current: Optional[Dict[str, Any]] = tree
    id1, id2 = lcas[0][1], lcas[1][1]

    while current:
        if id1 < current["id"] and id2 < current["id"]:
            current = current["left"]  # Both IDs are smaller, go left
        elif id1 > current["id"] and id2 > current["id"]:
            current = current["right"]  # Both IDs are larger, go right
        else:
            # We've found the split point (LCA)
            return current["code"]

    return None  # Should not happen if input is valid


def part_one(artifacts: List[Tuple[str, int]]) -> int:
    """
    Calculate the product of the maximum level sum and the number of occupied
    levels.

    Args:
        artifacts: List of (code, id) pairs

    Returns:
        Product of maximum level sum and number of occupied levels
    """
    tree = build_bst(artifacts)
    sums = level_sums(tree)
    max_sum = max(sums.values())
    occupied_layers = len(sums)

    return max_sum * occupied_layers


def part_two(artifacts: List[Tuple[str, int]]) -> str:
    """
    Determine the insertion path for a new artifact with ID 500,000.

    Args:
        artifacts: List of (code, id) pairs

    Returns:
        String representing the insertion path
    """
    tree = build_bst(artifacts)
    if tree is None:
        return ""
    return find_insertion_path(tree, 500_000)


def part_three(
        artifacts: List[Tuple[str, int]],
        lcas: List[Tuple[str, int]]
        ) -> Optional[str]:
    """
    Find the Lowest Common Ancestor of two specified artifacts.

    Args:
        artifacts: List of (code, id) pairs for building the tree
        lcas: List of two (name, id) pairs for finding LCA

    Returns:
        Code of the Lowest Common Ancestor, or None if not found
    """
    tree = build_bst(artifacts)
    if tree is None:
        return None
    return find_lca(tree, lcas)


if __name__ == "__main__":
    artifacts, lcas = read_puzzle_input()

    # Solve and print results for all three parts
    print("Part 1:", part_one(artifacts))          # 1075663180
    print("Part 2:", part_two(artifacts))
    # lYdMTWV-OftazMD-qvMmbgl-YLQdInz-nkNnGCd-cmntISR-bWLYIBR-ENQpJsA-sKtZuhh-OaoiHzb-RFlCeDW
    print("Part 3:", part_three(artifacts, lcas))  # oMOZWrx
