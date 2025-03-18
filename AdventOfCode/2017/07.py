#!/usr/bin/env python

from collections import defaultdict
from typing import Optional, Tuple


def read_puzzle_input() -> list:
    """
    Reads the puzzle input from a file and returns it as a list of strings.

    Returns:
        list: A list of strings, where each string represents a line from the
              input file.
    """

    with open("07.in", "r") as file:
        return file.read().splitlines()


def parse_input(data: list) -> tuple[dict, dict]:
    """
    Parses the input data into a tree structure and a dictionary of weights.

    Args:
        data (list): A list of strings, where each string represents a
                     program and its children.

    Returns:
        tuple[dict, dict]: A tuple containing:
            - A dictionary representing the tree structure
              (program -> list of children).
            - A dictionary representing the weights of each program
              (program -> weight).
    """

    tree = {}
    weights = {}
    for line in data:
        parts = line.split()
        name = parts[0]
        weight = int(parts[1].strip('()'))
        children = []
        if '->' in line:
            children = [part.strip(',') for part in parts[3:]]
        tree[name] = children
        weights[name] = weight
    return tree, weights


def calculate_total_weights(node: str, tree: dict, weights: dict,
                            total_weights: dict) -> int:
    """
    Recursively calculates the total weight of a program, including its
    children.

    Args:
        node (str): The name of the program to calculate the total weight for.
        tree (dict): The tree structure (program -> list of children).
        weights (dict): The weights of each program (program -> weight).
        total_weights (dict): A dictionary to store the total weights of
                              programs (program -> total weight).

    Returns:
        int: The total weight of the program and its children.
    """

    if node in total_weights:
        return total_weights[node]
    total = weights[node]
    for child in tree[node]:
        total += calculate_total_weights(child, tree, weights, total_weights)
    total_weights[node] = total
    return total


def find_unbalanced_node(node: str, tree: dict, total_weights: dict,
                         weights: dict) -> Optional[Tuple[str, int]]:
    """
    Finds the unbalanced program in the tree and calculates the required
    weight adjustment.

    Args:
        node (str): The name of the program to start searching from.
        tree (dict): The tree structure (program -> list of children).
        total_weights (dict): The total weights of programs
                              (program -> total weight).
        weights (dict): The weights of each program (program -> weight).

    Returns:
        Optional[Tuple[str, int]]: A tuple containing:
            - The name of the unbalanced program.
            - The weight it should have to balance the tree.
            If the tree is balanced, returns None.
    """

    children = tree[node]
    if not children:
        return None

    # Group children by their total weights
    weight_counts = defaultdict(list)
    for child in children:
        weight_counts[total_weights[child]].append(child)

    # If all children have the same weight, this node is balanced
    if len(weight_counts) == 1:
        return None

    # Find the unbalanced child
    unbalanced_weight = 0
    unbalanced_node = ''
    for weight, nodes in weight_counts.items():
        if len(nodes) == 1:
            unbalanced_weight = weight
            unbalanced_node = nodes[0]
            break

    # Check if the unbalanced node's children are balanced
    if (find_unbalanced_node(
            unbalanced_node, tree, total_weights, weights) is not None):
        return find_unbalanced_node(unbalanced_node, tree,
                                    total_weights, weights)

    # Calculate the correct weight for the unbalanced node
    correct_weight = 0
    for weight in weight_counts:
        if weight != unbalanced_weight:
            correct_weight = weight
            break

    # Calculate the required adjustment
    required_weight = weights[unbalanced_node] \
        + (correct_weight - unbalanced_weight)
    return (unbalanced_node, required_weight)


def part_one(data: list) -> int:
    """
    Solves Part 1 of the puzzle: Finds the bottom program in the tree.

    Args:
        data (list): A list of strings representing the puzzle input.

    Returns:
        int: The name of the bottom program.
    """

    tree, _ = parse_input(data)
    children = set()
    all_programs = set(tree.keys())
    for node in tree:
        children.update(tree[node])
    return (all_programs - children).pop()


def part_two(data: list) -> int:
    """
    Solves Part 2 of the puzzle: Finds the unbalanced program and calculates
    the required weight adjustment.

    Args:
        data (list): A list of strings representing the puzzle input.

    Returns:
        int: The weight the unbalanced program should have to balance the tree.
             Returns -2 if the tree is already balanced.
    """

    tree, weights = parse_input(data)
    children = set()
    all_programs = set(tree.keys())

    for node in tree:
        children.update(tree[node])

    bottom_program = (all_programs - children).pop()

    total_weights = {}

    calculate_total_weights(bottom_program, tree, weights, total_weights)
    result = find_unbalanced_node(bottom_program, tree, total_weights, weights)
    if result:
        return result[1]

    return -2


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # cqmvs
    print("Part 2:", part_two(data))  # 2310
